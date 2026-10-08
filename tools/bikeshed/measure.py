#!/usr/bin/env python3
"""Check a converted build against the old one: are all ids still there, are
there as many links, and does every link land where it landed before?

    python3 measure.py --old-build /path/to/svgwg/build/publish --out out/ [--report out/measure.json]

--old-build is the output folder of the old tool (tools/build.py writes it to
build/publish in the svgwg checkout). --out is the folder convert.py wrote,
after Bikeshed has built out/index.html. Build with --trace-links so the
landing check has something to follow.

What it compares, for each converted page P:

ids    1. every id in the old page P.html must exist in the new output, either
          as the same id or (for the ids that appear on several pages) as
          'P-id', which the page splitter turns back into 'id';
       2. every id of the old single-page.html inside chapter P ('P-id')
          must exist in the new output.
links  3. number of <a href> in the old page P.html versus in chapter P of the
          new output, leaving out heading self-links, the per-page table of
          contents and the navigation bar, and counting IDL blocks apart;
       4. landing: each link the converter wrote is found again by its
          data-svgtrace number, and its final href is compared with where the
          old link pointed. exact = same id; section = a different id in the
          same section; elsewhere = another section; unresolved = Bikeshed left
          no href; lost = the link is not in the output.

Standard library only.
"""

import argparse
import html.parser
import io
import json
import os
import re
import sys

HEADINGS = {"h1", "h2", "h3", "h4", "h5", "h6"}
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}


BACK_MATTER = {"index", "references", "issues-index", "property-index", "w3c-conformance", "conformance"}
TEXT_BLOCKS = {"p", "li", "dt", "dd", "td", "th", "caption", "pre", "h1", "h2", "h3", "h4", "h5", "h6",
               "div", "figcaption", "blockquote", "summary"}


def norm_text(t):
    t = re.sub(r"\s+", " ", t).strip()
    # section numbers differ by design ("10.2." today, "3.2." in a partial build)
    t = re.sub(r"^(Chapter \d+: |Appendix [A-Z]: |([A-Z]|\d+)(\.\d+)+\.? |\d+\. )", "", t)
    # Decided 2026-10-08: Bikeshed's curly apostrophe is accepted,
    # so a straight and a curly apostrophe count as the same character.
    return t.replace("\u2019", "'")


class Scan(html.parser.HTMLParser):
    """One pass over a page: ids in order with their section, every <a href>
    with flags saying whether it sits in an IDL block, a self-link, the
    old table of contents, and which chapter of the new output it is in."""

    def __init__(self, chapter=None):
        html.parser.HTMLParser.__init__(self, convert_charrefs=True)
        self.ids = {}            # id -> dict(pos, section, chapter, tag)
        self.links = []          # dict(href, idl, selflink, toc, chapter, trace)
        self.trace = {}          # data-svgtrace -> href (None if unresolved)
        self.section = None
        self.chapter = chapter
        self.pos = 0
        self.in_idl = 0
        self.stack = []          # open elements, for nav#toc and pre.idl tracking
        self.toc_depth = None
        self.blocks = []         # (chapter, text) of each innermost text block
        self.buf = []            # text buffers of the open text blocks
        self.open_a = None
        self.skip = 0            # inside an element whose text is Bikeshed's or the old tool's decoration

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self.pos += 1
        cls = (a.get("class") or "").split()
        if tag in HEADINGS and a.get("id"):
            self.section = a["id"]
        if a.get("data-bs-page"):
            self.chapter = a["data-bs-page"]
        elif tag == "h2" and self.chapter is not None and a.get("id") in BACK_MATTER:
            self.chapter = None  # Bikeshed's own back matter (index, references)
        if a.get("id") is not None:
            self.ids.setdefault(a["id"], dict(pos=self.pos, section=self.section, chapter=self.chapter, tag=tag))
        if tag == "a":
            if a.get("data-svgtrace") is not None:
                self.trace[a["data-svgtrace"]] = a.get("href")
            if a.get("href") is not None:
                self.links.append(dict(href=a["href"], idl=self.in_idl > 0, selflink="self-link" in cls,
                                       toc=self.toc_depth is not None, chapter=self.chapter, text=[]))
                self.open_a = self.links[-1]
        if tag in VOID:
            return
        deco = "secno" in cls or "self-link" in cls or (tag == "nav" and a.get("id") == "toc") or "bs-old-id" in cls
        if deco:
            self.skip += 1
        if tag in TEXT_BLOCKS:
            self.buf.append([])
        self.stack.append((tag, a.get("id"), "idl" in cls and tag == "pre", deco))
        if tag == "pre" and "idl" in cls:
            self.in_idl += 1
        if tag == "nav" and a.get("id") == "toc" and self.toc_depth is None:
            self.toc_depth = len(self.stack)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID and self.stack and self.stack[-1][0] == tag:
            self._pop()

    def handle_data(self, data):
        if self.open_a is not None:
            self.open_a["text"].append(data)
        if self.skip or not self.buf:
            return
        self.buf[-1].append(data)

    def _pop(self):
        tag, i, idl, deco = self.stack.pop()
        if deco:
            self.skip -= 1
        if tag in TEXT_BLOCKS and self.buf:
            t = norm_text("".join(self.buf.pop()))
            if t:
                self.blocks.append((self.chapter, t))
        if tag in TEXT_BLOCKS or tag in ("ul", "ol", "dl", "table"):
            if self.buf:
                self.buf[-1].append(" ")  # a nested block ends: a line break, not glued text
        if idl:
            self.in_idl -= 1
        if self.toc_depth is not None and len(self.stack) < self.toc_depth:
            self.toc_depth = None

    def handle_endtag(self, tag):
        if tag == "a":
            self.open_a = None
        # pop up to the matching element (Bikeshed omits some end tags)
        for k in range(len(self.stack) - 1, -1, -1):
            if self.stack[k][0] == tag:
                while len(self.stack) > k:
                    self._pop()
                return


def scan(path, chapter=None):
    s = Scan(chapter)
    with io.open(path, encoding="utf-8") as f:
        s.feed(f.read())
    s.close()
    return s


def single_page_chapter_ids(path, page):
    """ids inside <div id="chapter-PAGE"> of the old single-page.html."""
    s = Scan()
    with io.open(path, encoding="utf-8") as f:
        data = f.read()
    start = data.find('id="chapter-%s"' % page)
    if start < 0:
        return set()
    start = data.rfind("<", 0, start)
    end = data.find('<hr class="chapter-divider"', start)
    end = len(data) if end < 0 else end
    s.feed(data[start:end])
    return set(s.ids) - {"chapter-" + page}


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--old-build", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--report")
    a = ap.parse_args()

    expected = json.load(io.open(os.path.join(a.out, "expected-ids.json"), encoding="utf-8"))
    trace = json.load(io.open(os.path.join(a.out, "trace-links.json"), encoding="utf-8"))
    conv = json.load(io.open(os.path.join(a.out, "convert-report.json"), encoding="utf-8"))
    single_mode = conv.get("page_mode") == "single"
    new = scan(os.path.join(a.out, "index.html"), conv["pages"][0] if single_mode else None)
    new_ids = new.ids
    single = os.path.join(a.old_build, "single-page.html")
    report = {"pages": {}}

    for page in conv["pages"]:
        r = {}
        old = scan(os.path.join(a.old_build, page + ".html"))
        # 1. multipage ids
        old_ids = set(old.ids)
        same, renamed, missing = [], [], []
        for i in sorted(old_ids):
            if i in new_ids:
                same.append(i)
            elif (page + "-" + i) in new_ids:
                renamed.append(i)
            else:
                missing.append(i)
        r["old_page_ids"] = len(old_ids)
        r["old_page_ids_same"] = len(same)
        r["old_page_ids_in_single_page_form"] = renamed
        r["old_page_ids_missing"] = missing
        # source ids (what the source files themselves carry, plus elementdef-*)
        src = expected.get(page, {})
        src_missing = [i for i, v in sorted(src.items()) if v["new"] not in new_ids]
        alias_missing = [i for i, v in sorted(src.items()) if v.get("alias") and v["alias"] not in new_ids]
        r["source_ids"] = len(src)
        r["source_ids_missing"] = src_missing
        r["source_ids_without_single_page_alias"] = alias_missing
        # 2. single-page ids
        if os.path.exists(single):
            sp = single_page_chapter_ids(single, page)
            r["old_single_page_ids"] = len(sp)
            r["old_single_page_ids_missing"] = sorted(i for i in sp if i not in new_ids)
        # 3. link counts
        def count(links, chapter=None):
            c = dict(prose=0, idl=0)
            for l in links:
                if l["selflink"] or l["toc"]:
                    continue
                if chapter is not None and l["chapter"] != chapter:
                    continue
                c["idl" if l["idl"] else "prose"] += 1
            return c
        r["old_links"] = count(old.links)
        r["new_links"] = count(new.links, page)
        # IDL blocks: Bikeshed rewrites them; check every name linked in an old
        # IDL block is still linked in the new one (by link text).
        from collections import Counter as _C
        oi = _C("".join(l["text"]).strip() for l in old.links if l["idl"] and not l["selflink"])
        ni = _C("".join(l["text"]).strip() for l in new.links if l["idl"] and not l["selflink"] and l["chapter"] == page)
        r["idl_link_texts_lost"] = sorted((oi - ni).elements())
        # 5. text, block by block (innermost block elements, whitespace folded)
        from collections import Counter
        ob = Counter(t for _, t in old.blocks)
        nb = Counter(t for c, t in new.blocks if c == page)
        only_old = list((ob - nb).elements())
        only_new = list((nb - ob).elements())
        r["text_blocks_old"] = sum(ob.values())
        r["text_blocks_new"] = sum(nb.values())
        r["text_blocks_only_old"] = only_old
        r["text_blocks_only_new"] = only_new
        report["pages"][page] = r

    # 4. landing
    land = {}
    bad = []
    for row in trace:
        n = str(row["n"])
        exp_page, exp_id = row["old_page"], row["old_id"]
        if exp_page in expected:
            if exp_id:
                info = expected[exp_page].get(exp_id)
                exp_new = info["new"] if info else exp_id
            else:
                exp_new = "chapter-" + exp_page
            exp_href = "#" + exp_new
        else:
            exp_href = None
        if n not in new.trace:
            res = "lost"
        else:
            href = new.trace[n]
            if href is None:
                res = "unresolved"
            elif exp_href is None:
                # target page not in this build: the converter wrote an absolute URL
                res = "exact" if href == row.get("written_href") else "elsewhere"
            elif href == exp_href:
                res = "exact"
            elif href.startswith("#") and href[1:] in new_ids and exp_href[1:] in new_ids:
                res = "section" if new_ids[href[1:]]["section"] == new_ids[exp_href[1:]]["section"] else "elsewhere"
            elif exp_href[1:] not in new_ids:
                res = "target missing (already broken today?)"
            else:
                res = "elsewhere"
        key = (row["page"], row["form"], res)
        land[key] = land.get(key, 0) + 1
        if res not in ("exact", "section"):
            bad.append(dict(row, result=res, new_href=new.trace.get(n), expected=exp_href))
    report["landing"] = [dict(page=k[0], form=k[1], result=k[2], count=v) for k, v in sorted(land.items())]
    report["landing_problems"] = bad

    # print a summary
    for page, r in report["pages"].items():
        print("== %s" % page)
        print("  source ids: %d, missing in output: %d %s" % (r["source_ids"], len(r["source_ids_missing"]), r["source_ids_missing"][:10]))
        print("  source ids without single-page alias: %d %s" % (len(r["source_ids_without_single_page_alias"]), r["source_ids_without_single_page_alias"][:10]))
        print("  old page ids: %d, same: %d, in single-page form (splitter restores): %d, missing: %d %s" % (
            r["old_page_ids"], r["old_page_ids_same"], len(r["old_page_ids_in_single_page_form"]),
            len(r["old_page_ids_missing"]), r["old_page_ids_missing"][:15]))
        if "old_single_page_ids" in r:
            print("  old single-page ids: %d, missing: %d %s" % (r["old_single_page_ids"], len(r["old_single_page_ids_missing"]), r["old_single_page_ids_missing"][:15]))
        print("  links old: prose %(prose)d, idl %(idl)d" % r["old_links"], "| new: prose %(prose)d, idl %(idl)d" % r["new_links"])
        print("  idl link texts linked before, not now: %d %s" % (len(r["idl_link_texts_lost"]), r["idl_link_texts_lost"][:10]))
        print("  text blocks old %d, new %d, only in old %d, only in new %d" % (
            r["text_blocks_old"], r["text_blocks_new"], len(r["text_blocks_only_old"]), len(r["text_blocks_only_new"])))
    print("== landing (page, form, result: count)")
    for l in report["landing"]:
        print("  %-10s %-16s %-30s %d" % (l["page"], l["form"], l["result"], l["count"]))
    if a.report:
        with io.open(a.report, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=1)


if __name__ == "__main__":
    sys.exit(main())
