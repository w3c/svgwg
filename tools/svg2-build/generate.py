#!/usr/bin/env python3
"""Put together the Bikeshed source of SVG 2 for one build.

    python3 generate.py --root /path/to/svgwg --out build/bikeshed/work

reads master/index.bs and the page files it includes (master/<page>.bs),
fills every data-svg-fill placeholder with the content generated from
definitions.xml, and writes into the output folder:

- index.bs, with every page copied in, ready for Bikeshed;
- header.include, the front page up to the table of contents;
- single-page-nav.json, for singlepage.py;
- links to the images/ and style/ folders.

A placeholder is an empty element in a page file:

    <div data-svg-fill="element-summary" data-name="rect"></div>
    <span data-svg-fill="element-category" data-name="graphics"></span>

The kinds are listed in convert.FILL_KINDS. The generated content links to
the definitions of this spec the way convert.py does, so the model of the
spec it needs (which ids exist on which page, which dfns they are) is read
from the page files themselves.

The pages are copied in rather than included with <pre class=include>,
because Bikeshed runs its Markdown reader on included files whatever the
metadata says (bikeshed/includes.py), which would change the text.

Standard library only. Python 3.9 or later.
"""

import argparse
import html.parser
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import convert  # noqa: E402
import svgdefs  # noqa: E402

INCLUDE_RE = re.compile(r"^<pre class=include>path: ([\w.-]+)\.bs</pre>$", re.M)
FILL_RE = re.compile(r'<(div|span) data-svg-fill="([^"]+)"([^>]*)></\1>')


class Page(object):
    """What convert.Converter needs to know about one page."""

    def __init__(self, name, kind, number):
        self.name = name
        self.kind = kind          # index | chapter | appendix
        self.number = number
        self.root = None
        self.parent = {}
        self.ids = {}             # source id -> tag name
        self.promoted = {}
        self.summaries = []       # element names with a summary placeholder
        self.text = ""


class PageScanner(html.parser.HTMLParser):
    """Collects ids, dfns, IDL blocks and placeholders of one page file."""

    def __init__(self, page, model):
        html.parser.HTMLParser.__init__(self, convert_charrefs=True)
        self.page = page
        self.model = model
        self.dfns = []            # open dfns: [attrs, text parts]
        self.idl = None           # text parts of the open IDL block

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if d.get("id"):
            # a clashing id is written in its single-page form; the source
            # id is in data-multipage-id
            old = d.get("data-multipage-id") or d["id"]
            self.page.ids.setdefault(old, tag)
            if d.get("data-multipage-id"):
                self.model.clashing.add(old)
        if tag == "dfn":
            self.dfns.append([d, []])
        elif tag == "pre" and "idl" in (d.get("class") or "").split():
            self.idl = []
        if d.get("data-svg-fill") == "element-summary":
            self.page.summaries.append(d.get("data-name"))

    def handle_data(self, data):
        for _, parts in self.dfns:
            parts.append(data)
        if self.idl is not None:
            self.idl.append(data)

    def handle_endtag(self, tag):
        if tag == "dfn" and self.dfns:
            d, parts = self.dfns.pop()
            self.model.add_dfn(self.page, d, "".join(parts))
        elif tag == "pre" and self.idl is not None:
            self.model.idl_interfaces.update(convert.idl_definition_types("".join(self.idl)))
            self.idl = None


def unescape_shorthands(s):
    """Text as the reader sees it: drop the backslashes convert.py puts
    before what Bikeshed would read as a shorthand."""
    return re.sub(r"\\(?=['\[{])", "", s)


class Model(object):
    """The parts of convert.Spec that the generated content depends on,
    read from the page files instead of the old source."""

    def __init__(self, root, cfg, src_dir, page_names, split_cfg):
        self.cfg = cfg
        self.master = src_dir
        self.maturity = cfg["source"].get("maturity", "ED")
        self.versions = {}
        self.clashing = set(cfg.get("reserved_ids", []))
        self.dfn_index = {}
        self.dfn_attrs = {}
        self.dfn_lt_override = {}
        self.idl_interfaces = {}
        self.def_infos = []
        for d in cfg["source"]["definitions"]:
            self.def_infos.append(dict(path=os.path.normpath(os.path.join(root, d["href"])),
                                       base=d.get("base"), specid=d.get("specid"),
                                       mainspec=d.get("mainspec")))
        appendix = dict((p["name"], p.get("appendix", False)) for p in split_cfg["pages"])
        front = cfg["source"]["front_page"]
        self.pages = [Page(front, "index", None)]
        chap, app = 0, 0
        for n in page_names:
            if appendix.get(n):
                app += 1
                self.pages.append(Page(n, "appendix", chr(64 + app)))
            else:
                chap += 1
                self.pages.append(Page(n, "chapter", str(chap)))
        self.page_by_name = dict((p.name, p) for p in self.pages)
        self.defs, self.defs_by_spec = svgdefs.load(self.def_infos)

    def scan(self, page, text):
        page.text = text
        s = PageScanner(page, self)
        s.feed(text)
        s.close()

    def add_dfn(self, page, d, text):
        if not d.get("id"):
            return
        old = d.get("data-multipage-id") or d["id"]
        fors = [x.strip() for x in (d.get("data-dfn-for") or "").split(",") if x.strip()]
        lt = d.get("data-lt") or d.get("lt")
        lt = lt.split("|")[0].strip() if lt else convert.norm_ws(unescape_shorthands(text))
        self.dfn_index[(page.name, old)] = dict(type=d.get("data-dfn-type") or "dfn",
                                                for_=fors[0] if fors else None, lt=lt)

    def finish(self):
        """After every page is scanned: an element summary on more than one
        page has a clashing id too (convert.Spec._analyse)."""
        seen = {}
        self.summary_page = {}
        for p in self.pages:
            for name in p.summaries:
                seen.setdefault(name, []).append(p.name)
                self.summary_page[name] = p.name
        for name, ps in seen.items():
            if len(ps) > 1:
                self.clashing.add("elementdef-" + name)


def fill_page(conv, page):
    def rep(m):
        attrs = dict(re.findall(r'([\w-]+)(?:="([^"]*)")?', m.group(3)))
        return conv.fill(page, m.group(2), attrs.get("data-name"), "data-omit-quotes" in attrs)
    return FILL_RE.sub(rep, page.text)


def single_page_nav(cfg, model, page_names):
    nav = dict(cfg["source"]["single_page_nav"])
    nav["pages"] = page_names
    nav["appendix_letters"] = dict((p.name, p.number) for p in model.pages if p.kind == "appendix")
    nav["drop_headings"] = cfg.get("single_page_drop_headings", [])
    return nav


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--root", default=os.path.normpath(os.path.join(HERE, "..", "..")),
                    help="svgwg checkout (default: the one holding this script)")
    ap.add_argument("--config", default=os.path.join(HERE, "config", "svg2.json"))
    ap.add_argument("--split-config", default=os.path.join(HERE, "config", "svg2-split.json"))
    ap.add_argument("--src", help="folder of index.bs and the page files (default: ROOT/master)")
    ap.add_argument("--out", required=True)
    ap.add_argument("--no-shorthands", action="store_true",
                    help="write generated links in their long form (only for comparing builds)")
    args = ap.parse_args(argv)

    root = os.path.abspath(args.root)
    with io.open(args.config, encoding="utf-8") as f:
        cfg = json.load(f)
    with io.open(args.split_config, encoding="utf-8") as f:
        split_cfg = json.load(f)
    src = os.path.abspath(args.src or os.path.join(root, cfg["source"]["dir"]))
    out = os.path.abspath(args.out)
    os.makedirs(out, exist_ok=True)
    convert.KEEP_STRAIGHT_APOSTROPHES[0] = cfg.get("keep_straight_apostrophes", True)
    convert.SHORTHANDS[0] = not args.no_shorthands

    with io.open(os.path.join(src, "index.bs"), encoding="utf-8") as f:
        index = f.read()
    page_names = INCLUDE_RE.findall(index)
    expected = [p["name"] for p in split_cfg["pages"]]
    if page_names != expected:
        sys.exit("generate.py: the pages included by index.bs (%s) are not the pages of %s (%s)"
                 % (", ".join(page_names), os.path.basename(args.split_config), ", ".join(expected)))

    model = Model(root, cfg, src, page_names, split_cfg)
    for n in page_names:
        with io.open(os.path.join(src, n + ".bs"), encoding="utf-8") as f:
            model.scan(model.page_by_name[n], f.read())
    model.finish()

    conv = convert.Converter(model, out, set(page_names))
    filled = {}
    for n in page_names:
        filled[n] = fill_page(conv, model.page_by_name[n])

    def inline(m):
        return "<!-- page: %s.bs -->\n%s" % (m.group(1), filled[m.group(1)])
    with io.open(os.path.join(out, "index.bs"), "w", encoding="utf-8") as f:
        f.write(INCLUDE_RE.sub(lambda m: inline(m), index))

    header = os.path.join(src, "header.include")
    if os.path.exists(header):
        # the front page up to the table of contents ('Local Boilerplate: header yes')
        with io.open(header, encoding="utf-8") as f:
            text = f.read()
        with io.open(os.path.join(out, "header.include"), "w", encoding="utf-8") as f:
            f.write(text)
    for res in cfg.get("link_resources", []):
        dst = os.path.join(out, res)
        if not os.path.lexists(dst):
            os.symlink(os.path.join(src, res), dst)
    with io.open(os.path.join(out, "single-page-nav.json"), "w", encoding="utf-8") as f:
        json.dump(single_page_nav(cfg, model, page_names), f, indent=1)

    for k in sorted(conv.stats):
        print("%6d  %s" % (conv.stats[k], k))
    for w in conv.warnings:
        print("warning: %s: %s" % w)
    return 0


if __name__ == "__main__":
    sys.exit(main())
