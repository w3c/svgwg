#!/usr/bin/env python3
"""Convert the SVG 2 editor's draft source (master/*.html, the custom XHTML
with edit:* elements) into Bikeshed source files.

    python3 convert.py --source /path/to/svgwg --out out/

writes out/<page>.bs for every page listed in publish.xml, out/index.bs that
includes them in publish.xml order, and two side files that the measuring
script reads: out/trace-links.json and out/expected-ids.json.

What is specific to one spec (SVG 2 versus a module under specs/) lives in a
JSON configuration file, config/svg2.json by default, not in this code.

The script reads every page as an XML tree (xml.etree), never with text
patterns, and can be re-run on the current source at any time: nothing in
out/ is meant to be edited by hand.

Standard library only. Python 3.9 or later. Bikeshed is only needed to build
the output, not to run this script.
"""

import argparse
import html.entities
import io
import json
import os
import re
import sys
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import svgdefs  # noqa: E402
from svgdefs import EDIT_NS, XHTML_NS, DEFS_NS, LQUOTE, RQUOTE  # noqa: E402

SVG_NS = "http://www.w3.org/2000/svg"
MATHML_NS = "http://www.w3.org/1998/Math/MathML"
XLINK_NS = "http://www.w3.org/1999/xlink"
XML_NS = "http://www.w3.org/XML/1998/namespace"

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta",
        "param", "source", "track", "wbr"}
# Elements inside which a hidden <span id> alias may go as first child.
PHRASING_OK = {"p", "li", "dt", "dd", "td", "th", "div", "span", "b", "i", "em", "strong",
               "a", "caption", "figcaption", "section", "code", "var", "dfn", "label",
               "h2", "h3", "h4", "h5", "h6", "details", "summary", "blockquote", "nav"}
HEADINGS = {"h1", "h2", "h3", "h4", "h5", "h6"}
BLOCKS = {"p", "div", "dl", "table", "ul", "ol", "pre", "blockquote", "figure", "details",
          "section", "h1", "h2", "h3", "h4", "h5", "h6", "hr"}

# tools/publish/maturities.js
LONG_MATURITY = {"ED": "Editor’s Draft", "WG-NOTE": "Working Group Note", "WD": "Working Draft",
                 "FPWD": "First Public Working Draft", "LCWD": "Working Draft", "FPLCWD": "Working Draft",
                 "CR": "Candidate Recommendation Snapshot", "CRD": "Candidate Recommendation Draft",
                 "PR": "Proposed Recommendation", "PER": "Proposed Edited Recommendation",
                 "REC": "Recommendation", "RSCND": "Rescinded Recommendation"}

# Bikeshed's text macro pattern (bikeshed/h/dom.py replaceMacros).
MACRO_RE = re.compile(r"\[([A-Z\d-]*[A-Z][A-Z\d-]*)(\??)\]")


# -- small helpers ------------------------------------------------------------

def local(tag):
    return tag.split("}", 1)[1] if tag.startswith("{") else tag


def ns(tag):
    return tag[1:].split("}", 1)[0] if tag.startswith("{") else ""


def is_edit(el, name=None):
    return isinstance(el.tag, str) and ns(el.tag) == EDIT_NS and (name is None or local(el.tag) == name)


def is_html(el, name=None):
    return isinstance(el.tag, str) and ns(el.tag) in (XHTML_NS, "") and (name is None or local(el.tag) == name)


def text_content(el):
    out = []
    if el.text:
        out.append(el.text)
    for c in el:
        if isinstance(c.tag, str):
            out.append(text_content(c))
        if c.tail:
            out.append(c.tail)
    return "".join(out)


def classes(el):
    return (el.get("class") or "").split()


KEEP_STRAIGHT_APOSTROPHES = [True]
# Bikeshed turns an apostrophe between letters (don't, path's) into a curly
# one while parsing (bikeshed/h/parser/nodes.py curlifyApostrophes). Writing
# it as a character reference keeps today's straight apostrophe.
APOS_RE = re.compile(r"(?:(?<=\w)|^)'(?=\w)|^'(?=\s)")


def esc_text(s):
    s = s.replace("&", "&amp;").replace("<", "&lt;")
    if KEEP_STRAIGHT_APOSTROPHES[0] and "'" in s:
        s = APOS_RE.sub("&#39;", s)
    # Bikeshed's typography joins a line that ends in an em dash (or "--")
    # to the next line, with no space between ("line-ending em dashes").
    # The rule only fires on the dash followed directly by a newline, so a
    # space is put between the two: the text renders the same as today
    # (HTML folds the space and the newline into one space) and nothing
    # depends on how Bikeshed reads character references.
    s = re.sub(r"(\u2014|(?<!-)--)\n", "\\1 \n", s)
    # Bikeshed would read [FOO] as a text macro; an escaped bracket keeps the text.
    return MACRO_RE.sub(lambda m: "&#91;" + m.group(0)[1:], s)


def esc_attr(s):
    s = s.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;")
    return MACRO_RE.sub(lambda m: "&#91;" + m.group(0)[1:], s)


def attr_name(key):
    if key.startswith("{"):
        n, l = key[1:].split("}", 1)
        if n == XLINK_NS:
            return "xlink:" + l
        if n == XML_NS:
            return "xml:" + l
        if n == EDIT_NS:
            return None  # handled by the caller
        return l
    return key


def norm_ws(s):
    return re.sub(r"\s+", " ", s).strip()


def make_parser():
    parser = ET.XMLParser(target=ET.TreeBuilder(insert_comments=True))
    # The chapters use HTML entities (&nbsp; and friends) that only the DTD
    # declares. The old build's XML reader knew them; teach expat the same set.
    for name, cp in html.entities.name2codepoint.items():
        parser.entity[name] = chr(cp)
    for name, val in html.entities.html5.items():
        if name.endswith(";"):
            parser.entity.setdefault(name[:-1], val)
    return parser


def parse_xml_file(path, repairs=()):
    with io.open(path, encoding="utf-8") as f:
        data = f.read()
    for old, new in repairs:
        data = data.replace(old, new)
    parser = make_parser()
    parser.feed(data)
    return parser.close()


# -- IDL member scanner -------------------------------------------------------
# Only used to learn, for each IDL member, its kind (attribute, method, const,
# dict-member), the interface it belongs to and its argument names, so that the
# prose element carrying the old __svg__ id can become the matching Bikeshed
# <dfn>. Bikeshed itself parses the IDL properly (widlparser).

IDENT = r"[A-Za-z_][A-Za-z0-9_]*"


def _blank_comments(s):
    def rep(m):
        return re.sub(r"[^\n]", " ", m.group(0))
    s = re.sub(r"/\*.*?\*/", rep, s, flags=re.S)
    return re.sub(r"//[^\n]*", rep, s)


def _split_depth0(s, start, sep):
    """Split s on `sep` at bracket depth 0. Yields (piece, offset)."""
    depth = 0
    last = 0
    for i, ch in enumerate(s):
        if ch in "([{<":
            depth += 1
        elif ch in ")]}>":
            depth -= 1
        elif ch == sep and depth == 0:
            yield s[last:i], start + last
            last = i + 1
    yield s[last:], start + last


def _strip_ext_attrs(s):
    s2 = s.lstrip()
    off = len(s) - len(s2)
    if s2.startswith("["):
        depth = 0
        for i, ch in enumerate(s2):
            if ch == "[":
                depth += 1
            elif ch == "]":
                depth -= 1
                if depth == 0:
                    return s2[i + 1:], off + i + 1
    return s2, off


def idl_members(text):
    """Return a list of dicts: iface, name, kind, args, pos (offset of the name)."""
    t = _blank_comments(text)
    out = []
    for m in re.finditer(r"\b(partial\s+)?(interface\s+mixin|callback\s+interface|interface|dictionary|namespace)\s+(" + IDENT + r")[^{;]*\{", t):
        kind_of_block = m.group(2).split()[0]
        iface = m.group(3)
        start = m.end()
        depth = 1
        i = start
        while i < len(t) and depth:
            if t[i] == "{":
                depth += 1
            elif t[i] == "}":
                depth -= 1
            i += 1
        body = t[start:i - 1]
        for stmt, off in _split_depth0(body, start, ";"):
            s, o2 = _strip_ext_attrs(stmt)
            base = off + o2
            if not s.strip():
                continue
            mm = re.match(r"\s*const\s+.*?(" + IDENT + r")\s*=", s, re.S)
            if mm:
                out.append(dict(iface=iface, name=mm.group(1), kind="const", args=None, pos=base + mm.start(1)))
                continue
            if re.search(r"\battribute\b", s):
                names = list(re.finditer(IDENT, s))
                if names:
                    n = names[-1]
                    out.append(dict(iface=iface, name=n.group(0), kind="attribute", args=None, pos=base + n.start()))
                continue
            if "(" in s:
                mm = re.search(r"(" + IDENT + r")\s*\(", s)
                if not mm:
                    continue
                name = mm.group(1)
                if name in ("getter", "setter", "deleter", "stringifier", "static", "undefined", "any",
                            "boolean", "object", "void"):
                    continue  # an anonymous special operation, or a return type
                inner = s[mm.end():s.rfind(")")]
                args = []
                for a, _ in _split_depth0(inner, 0, ","):
                    a, _o = _strip_ext_attrs(a)
                    a = a.split("=")[0]
                    ids = re.findall(IDENT, a)
                    if ids:
                        args.append(ids[-1])
                out.append(dict(iface=iface, name=name, kind="method", args=args, pos=base + mm.start(1)))
                continue
            if kind_of_block == "dictionary":
                s0 = s.split("=")[0]
                names = list(re.finditer(IDENT, s0))
                if names:
                    n = names[-1]
                    out.append(dict(iface=iface, name=n.group(0), kind="dict-member", args=None, pos=base + n.start()))
    return out


def text_with_link_offsets(pre):
    """Text content of an IDL <pre>, plus (offset, href) for each <a href> in it."""
    parts = []
    links = []
    pos = [0]

    def walk(el):
        if el.text:
            parts.append(el.text)
            pos[0] += len(el.text)
        for c in el:
            if isinstance(c.tag, str):
                if is_html(c, "a") and c.get("href"):
                    links.append((pos[0], c.get("href")))
                walk(c)
            if c.tail:
                parts.append(c.tail)
                pos[0] += len(c.tail)
    walk(pre)
    return "".join(parts), links


# -- the spec model -----------------------------------------------------------

class Page(object):
    def __init__(self, name, kind, number, path):
        self.name = name
        self.kind = kind          # index | chapter | appendix | page
        self.number = number      # chapter number or appendix letter
        self.path = path
        self.root = None
        self.parent = {}
        self.ids = {}             # id -> element
        self.order = {}           # element -> preorder index
        self.summaries = []       # element names with an edit:elementsummary
        self.promoted = {}        # id -> dict(kind, iface, name, args) for __svg__ ids

    def load(self, repairs):
        self.root = parse_xml_file(self.path, repairs)
        i = 0
        for el in self.root.iter():
            self.order[el] = i
            i += 1
            for c in el:
                self.parent[c] = el
            if not isinstance(el.tag, str):
                continue
            if el.get("id") is not None:
                self.ids.setdefault(el.get("id"), el)
            if is_edit(el, "elementsummary"):
                self.summaries.append(el.get("name"))

    def body(self):
        for el in self.root:
            if local(el.tag) == "body":
                return el
        return self.root

    def ancestors(self, el):
        p = self.parent.get(el)
        while p is not None:
            yield p
            p = self.parent.get(p)


class Spec(object):
    def __init__(self, source, cfg):
        self.cfg = cfg
        self.master = os.path.join(source, cfg["source_dir"])
        self.publish_path = os.path.join(self.master, cfg.get("publish_xml", "publish.xml"))
        pub = ET.parse(self.publish_path).getroot()
        q = lambda n: "{%s}%s" % (DEFS_NS, n)
        self.title = (pub.findtext(q("title")) or "").strip()
        self.short_title = (pub.findtext(q("short-title")) or "").strip()
        self.maturity = (pub.findtext(q("maturity")) or "ED").strip()
        self.minimal_review_date = (pub.findtext(q("minimal-review-date")) or "").strip()
        self.versions = {}
        v = pub.find(q("versions"))
        if v is not None:
            for c in v:
                if isinstance(c.tag, str):
                    self.versions[local(c.tag)] = c.get("href")
        # publish.xml <toc href>, <elementindex href> ...: the navigation bar
        # at the top of each chapter points there
        self.nav = {}
        for key in ("toc", "elementindex", "attributeindex", "propertyindex"):
            e = pub.find(q(key))
            if e is not None and e.get("href"):
                self.nav[key] = e.get("href")
        self.def_infos = []
        for d in pub.findall(q("definitions")):
            self.def_infos.append(dict(path=os.path.normpath(os.path.join(self.master, d.get("href"))),
                                       base=d.get("base"), specid=d.get("specid"), mainspec=d.get("mainspec")))
        self.pages = []
        chap = 0
        app = 0
        for c in pub:
            if not isinstance(c.tag, str):
                continue
            kind = local(c.tag)
            if kind not in ("index", "chapter", "appendix", "page"):
                continue
            num = None
            if kind == "chapter":
                chap += 1
                num = str(chap)
            elif kind == "appendix":
                app += 1
                num = chr(64 + app)
            name = c.get("name")
            self.pages.append(Page(name, kind, num, os.path.join(self.master, name + ".html")))
        self.page_by_name = dict((p.name, p) for p in self.pages)
        repairs = cfg.get("source_repairs", {})
        for p in self.pages:
            p.load([tuple(r) for r in repairs.get(p.name + ".html", [])])
        self.defs, self.defs_by_spec = svgdefs.load(self.def_infos)
        self._analyse()

    # Which ids exist on more than one page, which ids are IDL members, where
    # each element summary lives.
    def _analyse(self):
        seen = {}
        for p in self.pages:
            for i in p.ids:
                seen.setdefault(i, []).append(p.name)
            for name in p.summaries:
                seen.setdefault("elementdef-" + name, []).append(p.name)
        reserved = set(self.cfg.get("reserved_ids", []))
        self.clashing = set(i for i, ps in seen.items() if len(ps) > 1 or i in reserved)
        self.summary_page = {}
        for p in self.pages:
            for name in p.summaries:
                self.summary_page[name] = p.name
        # IDL: member kind and interface, keyed by the __svg__ id the IDL links to.
        self.idl_by_id = {}
        self.idl_interfaces = {}  # name -> Bikeshed link type (interface, dictionary, ...)
        for p in self.pages:
            for pre in p.root.iter("{%s}pre" % XHTML_NS):
                if "idl" not in classes(pre):
                    continue
                text, links = text_with_link_offsets(pre)
                members = idl_members(text)
                for mm in re.finditer(r"\b(interface\s+mixin|interface|dictionary|callback\s+interface|callback|enum|typedef)\s+(" + IDENT + r")", _blank_comments(text)):
                    if not re.search(r"partial\s+$", _blank_comments(text)[:mm.start()][-20:]):
                        kw = mm.group(1).split()[0]
                        typ = {"interface": "interface", "dictionary": "dictionary", "callback": "callback",
                               "enum": "enum", "typedef": "typedef"}[kw]
                        if kw == "typedef":
                            continue  # the name is the last word, not the first; not linked by name here
                        self.idl_interfaces[mm.group(2)] = typ
                for off, href in links:
                    if "#__svg__" not in href:
                        continue
                    frag = href.split("#", 1)[1]
                    for mem in members:
                        if mem["pos"] == off:
                            # one prose definition can serve several interfaces
                            # (the list interfaces share __svg__SVGNameList__*)
                            self.idl_by_id.setdefault(frag, []).append(mem)
        # Prose elements carrying those ids become IDL dfns.
        for p in self.pages:
            for i, el in p.ids.items():
                if i in self.idl_by_id and local(el.tag) in ("b", "span", "dfn", "code"):
                    p.promoted[i] = self.idl_by_id[i]
        # dfn index: (page, id) -> (type, for, lt) as Bikeshed will see it.
        self._build_def_targets()
        self.dfn_index = {}
        self.dfn_attrs = {}
        for p in self.pages:
            for i, el in p.ids.items():
                info = None
                if i in p.promoted:
                    mems = p.promoted[i]
                    fors, lts = [], []
                    for mem in mems:
                        if mem["iface"] not in fors:
                            fors.append(mem["iface"])
                        lt = mem["name"]
                        if mem["kind"] == "method":
                            lt = "%s(%s)" % (mem["name"], ", ".join(mem["args"]))
                        if lt not in lts:
                            lts.append(lt)
                    info = dict(type=mems[0]["kind"], for_=fors[0], fors=fors, lt=lts[0], lts=lts)
                if info:
                    self.dfn_index[(p.name, i)] = info
            # every <dfn>, with or without id: the type and for the output will carry
            for el in p.root.iter("{%s}dfn" % XHTML_NS):
                typ = self._dfn_type(p, el)
                fors = self._dfn_fors(p, el, typ)
                self.dfn_attrs[el] = (typ, fors)
                if el.get("id") is not None and el.get("id") not in p.promoted:
                    self.dfn_index[(p.name, el.get("id"))] = dict(
                        type=typ, for_=fors[0] if fors else None, lt=self._dfn_lt(el))
        self._disambiguate_dfns()

    def _disambiguate_dfns(self):
        """Two dfns with the same type, for and text are an error in Bikeshed
        (today's source has six). The later ones get a linking text with the
        id added, so each stays a dfn and every link still lands on the one
        it pointed to. The visible text does not change. Listed in the report
        as spec defects to settle in master/."""
        self.dfn_lt_override = {}
        self.dfn_duplicates = []
        groups = {}
        for p in self.pages:
            for el in p.root.iter("{%s}dfn" % XHTML_NS):
                if el not in self.dfn_attrs:
                    continue
                typ, fors = self.dfn_attrs[el]
                key = (typ, tuple(fors), self._dfn_lt(el).lower() if typ == "dfn" else self._dfn_lt(el))
                groups.setdefault(key, []).append((p, el))
        for key, els in groups.items():
            if len(els) < 2:
                continue
            self.dfn_duplicates.append(dict(type=key[0], fors=list(key[1]), text=key[2],
                                            where=["%s#%s" % (p.name, el.get("id") or "(no id)") for p, el in els]))
            for k, (p, el) in enumerate(els[1:], 2):
                lt = "%s (%s)" % (self._dfn_lt(el), el.get("id") or "%s %d" % (p.name, k))
                self.dfn_lt_override[el] = lt
                if el.get("id") is not None and (p.name, el.get("id")) in self.dfn_index:
                    self.dfn_index[(p.name, el.get("id"))]["lt"] = lt

    def _build_def_targets(self):
        """(page, id) -> (Bikeshed dfn type, [for...]) from definitions.xml, for
        dfns whose type the source does not say."""
        t = {}

        def add(href, typ, fors):
            if not href or ":" in href.split("#")[0] or "#" not in href:
                return
            pg, frag = href.split("#", 1)
            pg = pg[:-5] if pg.endswith(".html") else pg
            if not pg:
                return
            cur = t.setdefault((pg, frag), [typ, []])
            for f in fors:
                if f not in cur[1]:
                    cur[1].append(f)

        d = self.defs
        for e in d.elements.values():
            for a in e.specific_attributes:
                add(a.href, "element-attr", [e.name])
        for cat in d.attribute_categories.values():
            for a in cat.attributes:
                add(a.href, "element-attr", [cat.name])
        for a in d.common_attributes_for_elements:
            add(a.href, "element-attr", sorted(a.elements))
        for a in d.common_attributes.values():
            add(a.href, "element-attr", [e.name for e in d.elements.values() if a.name in e.common_attribute_names])
        for p in d.properties.values():
            add(p.href, "property", [])
        for s in d.symbols.values():
            add(s.href, "type", [])
        self.def_targets = t

    def _dfn_type(self, page, el):
        """The type Bikeshed should give this dfn. The converter writes it out
        explicitly, so Bikeshed never has to guess."""
        t = el.get("data-dfn-type")
        if t:
            return t
        i = el.get("id")
        if i and (page.name, i) in self.def_targets:
            typ, fors = self.def_targets[(page.name, i)]
            if typ != "element-attr" or fors or self._with_element(page, el):
                return typ
        for a in page.ancestors(el):
            if not isinstance(a.tag, str):
                continue
            if a.get("data-dfn-type"):
                return a.get("data-dfn-type")
            cls = classes(a)
            if "propdef" in cls:
                return "property"
        txt = norm_ws(text_content(el))
        if re.match(r"^<.*>$", txt):
            return "type"
        return "dfn"

    def _with_element(self, page, el):
        for a in page.ancestors(el):
            if is_edit(a, "with"):
                return a.get("element")
        return None

    def _dfn_fors(self, page, el, typ):
        for e in [el] + list(page.ancestors(el)):
            if not isinstance(e.tag, str):
                continue
            for k in ("data-dfn-for", "dfn-for"):
                if e.get(k):
                    return [x.strip() for x in e.get(k).split(",") if x.strip()]
        i = el.get("id")
        if i and (page.name, i) in self.def_targets and self.def_targets[(page.name, i)][0] == typ:
            fors = self.def_targets[(page.name, i)][1]
            if fors:
                return fors
        if typ == "element-attr":
            w = self._with_element(page, el)
            if w:
                return [w]
        return []

    def _dfn_lt(self, el):
        lt = el.get("data-lt") or el.get("lt")
        if lt:
            return lt.split("|")[0].strip()
        return norm_ws(text_content(el))


# -- per-page conversion ------------------------------------------------------

class Ctx(object):
    """What the resolver needs to know about one <a> (see svgdefs.Resolver)."""

    def __init__(self, page, el):
        self.page = page
        self.el = el

    def where(self):
        return "%s.html" % self.page.name

    def with_element(self):
        for a in self.page.ancestors(self.el):
            if is_edit(a, "with"):
                return a.get("element")
        return None

    def closest_interface(self):
        # definitions.js findClosestInterfaceDefinition: previous siblings,
        # then the parent, then its previous siblings, and so on.
        n = self.el
        while n is not None:
            if isinstance(n.tag, str) and local(n.tag) in ("h2", "h3", "h4", "h5", "h6"):
                m = re.match(r"^Interface (\S+)$", text_content(n))
                if m:
                    return m.group(1)
            par = self.page.parent.get(n)
            if par is None:
                return None
            sibs = [c for c in par]
            idx = sibs.index(n)
            n = sibs[idx - 1] if idx > 0 else par
        return None

    def page_has_id(self, i):
        return i in self.page.ids

    def edit_format(self):
        return self.el.get("{%s}format" % EDIT_NS)

    def in_proptable_th(self):
        par = self.page.parent.get(self.el)
        if par is None or local(par.tag) != "th":
            return False
        for a in self.page.ancestors(self.el):
            if local(a.tag) == "table":
                return a.get("class") == "proptable"
        return False


class Converter(object):
    def __init__(self, spec, out_dir, build_pages, trace=False):
        self.spec = spec
        self.cfg = spec.cfg
        self.out_dir = out_dir
        self.build_pages = build_pages      # page names included in index.bs
        self.trace = trace
        self.trace_rows = []
        self.warnings = []
        self.resolver = svgdefs.Resolver(spec.defs, self.warnings)
        self.host_rewrites = [(re.compile(a), b) for a, b in self.cfg.get("host_rewrites", [])]
        self.stats = {}

    # ---- ids --------------------------------------------------------------

    def new_id(self, page, i):
        """The id the element gets in the Bikeshed source."""
        if i in self.spec.clashing:
            return page.name + "-" + i
        return i

    def single_page_alias(self, page, i):
        """The extra id that keeps today's single-page.html#page-id links."""
        if not self.cfg.get("single_page_aliases", True):
            return None
        if i in self.spec.clashing:
            return None  # the new id already is the single-page id
        return page.name + "-" + i

    def anchor_for(self, cur_page, target_page, frag):
        """href value for an old (page, id) target in the single Bikeshed document."""
        if target_page not in self.build_pages:
            base = self.cfg["published_base"]
            pg = self.spec.page_by_name.get(target_page)
            path = "" if pg is not None and pg.kind == "index" else target_page + ".html"
            return base + path + ("#" + frag if frag else "")
        if not frag:
            return "#chapter-" + target_page
        return "#" + self.new_id(self.spec.page_by_name[target_page], frag)

    def spec_relative(self, href):
        """processing.js resolveSpecRelativeLink: '[SVG2]path#frag' -> URL."""
        m = re.match(r"^\[(\S+)\]([^#]*)(#.*)?", href)
        if not m:
            return href
        bases = dict((d["specid"], d["base"]) for d in self.spec.def_infos if d.get("specid"))
        base = bases.get(m.group(1))
        if base is None:
            self.warnings.append(("-", "unknown spec [%s]" % m.group(1)))
            return href
        path = m.group(2)
        if base.endswith("/") and path.startswith("/"):
            path = path[1:]
        elif not base.endswith("/") and path and not path.startswith("/"):
            path = "/" + path
        self.bump("links: [SPECID] hrefs resolved")
        return base + path + (m.group(3) or "")

    def split_local(self, page, href):
        """('page', 'frag') when href points into this spec, else None."""
        if href.startswith("#"):
            return page.name, href[1:]
        m = re.match(r"^([A-Za-z0-9_.-]+)\.html(?:#(.*))?$", href)
        if m and m.group(1) in self.spec.page_by_name:
            return m.group(1), m.group(2)
        if href in ("./", "index.html", "Overview.html"):
            idx = [p for p in self.spec.pages if p.kind == "index"]
            if idx:
                return idx[0].name, None
        return None

    def rewrite_external(self, href):
        for rx, rep in self.host_rewrites:
            href2 = rx.sub(rep, href)
            if href2 != href:
                self.bump("external hrefs: host rewritten")
                return href2
        return href

    def bump(self, key, n=1):
        self.stats[key] = self.stats.get(key, 0) + n

    def fill_template(self, v):
        """{{maturity}}, {{date}}, {{latest}} ... in edit:href and edit:datetime."""
        vals = dict(maturity=self.spec.maturity, date="[ISODATE]")
        for k, u in self.spec.versions.items():
            vals[k] = u or ""
        return re.sub(r"\{\{(\w+)\}\}", lambda m: vals.get(m.group(1), m.group(0)), v)

    # ---- the front page ---------------------------------------------------

    def front_matter(self, page):
        """The front page (Overview.html) in two parts: what goes before the
        table of contents (written into Bikeshed's header.include, with
        'Local Boilerplate: header yes', so the head, the W3C status text,
        the patent and process links stay word for word as today), and what
        comes after it (Acknowledgments), which opens <main>."""
        body = page.body()
        before, after = [], []
        cur = before
        if body.text:
            cur.append(esc_text(body.text))
        first = True
        for c in body:
            if isinstance(c.tag, str) and local(c.tag) == "nav" and c.get("id") == "toc":
                # Bikeshed fills this nav with its own table of contents and
                # heading (id="contents"). Today's heading id goes on an
                # alias as the first thing in it, next to that heading.
                ids = []
                for h in c.iter():
                    if h is not c and isinstance(h.tag, str) and h.get("id"):
                        for i in (self.new_id(page, h.get("id")), self.single_page_alias(page, h.get("id"))):
                            if i:
                                ids.append('<span class="bs-old-id" id="%s"></span>' % esc_attr(i))
                cur.append('<nav data-fill-with="table-of-contents" id="%s">%s</nav>' % (
                    esc_attr(c.get("id")), "".join(ids)))
                self.bump("front matter: table of contents nav")
                cur = after
            else:
                html_c = self.node_html(page, c)
                if first and isinstance(c.tag, str) and "head" in classes(c):
                    # the single page wraps the front page in
                    # <div id="chapter-Overview">: keep that id too
                    html_c = re.sub(r"^(<div[^>]*>)", r'\1<span class="bs-old-id" id="chapter-%s"></span>'
                                    % page.name, html_c, count=1)
                    first = False
                cur.append(html_c)
            if c.tail:
                cur.append(esc_text(c.tail))
        return "".join(before).strip() + "\n", "".join(after).strip() + "\n"

    def header_include(self, page):
        """Bikeshed header.include: today's <head> links, then the front page
        up to the table of contents, then <main>."""
        before, after = self.front_matter(page)
        head = "\n".join(self.cfg.get("head_html", []))
        cls = self.spec.page_by_name[page.name].body().get("class")
        body_open = '<body class="h-entry%s">' % ((" " + esc_attr(cls)) if cls else "")
        return ("<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n" + head + "\n</head>\n"
                + body_open + "\n" + before + "<main>\n"), after

    # ---- links ------------------------------------------------------------

    def typed_attrs(self, target, link_kind, name):
        """Bikeshed link attributes when a typed link lands on the same id
        (or, for the kinds the policy allows, in the same section); else None."""
        tp, frag = target
        if tp not in self.build_pages or not frag:
            return None
        info = self.spec.dfn_index.get((tp, frag))
        if info:
            attrs = [("data-link-type", info["type"])]
            if info["for_"]:
                attrs.append(("data-link-for", info["for_"]))
            attrs.append(("data-lt", info["lt"]))
            return attrs, "exact"
        policy = self.cfg.get("typed_link_policy", {})
        if link_kind == "element" and policy.get("element") == "section":
            sp = self.spec.summary_page.get(name)
            if sp and sp == tp and sp in self.build_pages:
                return [("data-link-type", "element"), ("data-lt", name)], "section"
        if link_kind == "interface" and policy.get("interface") == "section":
            if name in self.spec.idl_interfaces:
                return [("data-link-type", self.spec.idl_interfaces[name]), ("data-lt", name)], "section"
        return None

    def emit_a(self, page, href, inner_html, extra_attrs=(), kind=None, name=None, handwritten=False):
        """One <a>, typed when allowed, explicit href otherwise."""
        if href and href.startswith("["):
            href = self.spec_relative(href)
        target = self.split_local(page, href) if href else None
        attrs = list(extra_attrs)
        trace = None
        if target is not None:
            typed = None
            if not handwritten or self.cfg.get("type_handwritten_links", True):
                typed = self.typed_attrs(target, kind, name)
            if typed:
                attrs = typed[0] + attrs
                form = "typed-" + typed[1]
            else:
                attrs = [("href", self.anchor_for(page.name, target[0], target[1]))] + attrs
                form = "explicit"
            trace = dict(page=page.name, old_page=target[0], old_id=target[1], form=form,
                         kind=kind or "handwritten", name=name,
                         written_href=attrs[0][1] if form == "explicit" else None)
            self.bump("links: %s %s" % ("hand-written" if handwritten else "shorthand", form))
        else:
            ext = self.rewrite_external(href) if href else href
            attrs = [("href", ext)] + attrs
            self.bump("links: %s external/resource" % ("hand-written" if handwritten else "shorthand"))
        if trace is not None and self.trace:
            trace["n"] = len(self.trace_rows)
            self.trace_rows.append(trace)
            attrs.append(("data-svgtrace", str(trace["n"])))
        a = "<a" + "".join(' %s="%s"' % (k, esc_attr(v)) for k, v in attrs if v is not None) + ">"
        return a + inner_html + "</a>"

    def emit_link(self, page, link):
        """A svgdefs.Link (the old build's answer) as Bikeshed source."""
        if link.kind == "error":
            self.bump("links: unresolved in old build too")
            return '<span class="xxx">%s</span>' % esc_text(link.text)
        if link.markup is not None:
            inner = self.children_html(page, link.markup)
        else:
            inner = esc_text(link.text)
        extra = []
        if link.a_class:
            extra.append(("class", link.a_class))
        if link.title:
            extra.append(("title", link.title))
        a = self.emit_a(page, link.href, inner, extra, kind=link.kind, name=link.name)
        if link.wrap:
            q1, q2 = (LQUOTE, RQUOTE) if link.quotes else ("", "")
            return '<span class="%s">%s%s%s</span>' % (link.wrap, q1, a, q2)
        return a

    # ---- generated content (from definitions.xml) -------------------------

    def gen_element_summary(self, page, name):
        d = self.spec.defs
        e = d.elements[name]
        R = self.resolver
        L = lambda thing, **kw: self.emit_link(page, svgdefs.format_thing(thing, **kw))

        # Categories (processing.js formatElementCategories)
        cats = [e.categories[k] for k in sorted(e.categories)]
        cat_html = "None" if not cats else "".join(
            svgdefs.comma_list([L(c, capitalize=(i == 0)) for i, c in enumerate(cats)]))

        # Content model (formatContentModel)
        if e.content_model_description is not None:
            cm = self.children_html(page, e.content_model_description)
        else:
            intro = {"any": "Any elements or character data.", "text": "Character data."}.get(e.content_model)
            if intro is None and e.content_model not in ("textoranyof", "anyof", "oneormoreof"):
                intro = "Empty."
            if e.content_model in ("textoranyof", "anyof", "oneormoreof"):
                intro = {"textoranyof": "Any number of the following elements or character data, in any order:",
                         "anyof": "Any number of the following elements, in any order:",
                         "oneormoreof": "One or more of the following elements, in any order:"}[e.content_model]
                lis = []
                for cn in sorted(e.element_categories):
                    cat = d.element_categories.get(cn)
                    if not cat:
                        lis.append('<li><span class="xxx">@@ unknown element category "%s"</span></li>' % esc_text(cn))
                        continue
                    members = svgdefs.comma_list([self.emit_link(page, R.element(x, Ctx(page, page.root))) for x in cat.elements])
                    lis.append('<li>%s<span class="expanding"> — %s</span></li>' % (
                        self.emit_a(page, cat.href, esc_text(cat.name + " elements"), kind="elementcategory", name=cat.name),
                        "".join(members)))
                singles = []
                for x in sorted(e.elements):
                    if x not in d.elements:
                        singles.append('<span class="xxx">@@ unknown element "%s"</span>' % esc_text(x))
                    else:
                        singles.append(self.emit_link(page, R.element(x, Ctx(page, page.root), omit_quotes=True)))
                cm = esc_text(intro) + '<ul class="no-bullets">%s</ul>' % "".join(lis) + "".join(svgdefs.comma_list(singles))
            else:
                cm = esc_text(intro)

        # Attributes (formatElementAttributes)
        lis = []
        for cn in e.attribute_categories:
            cat = d.attribute_categories.get(cn)
            if not cat:
                continue
            names = cat.common_attribute_names + [a.name for a in cat.attributes]
            items = [self.emit_link(page, R.element_attribute(name, a, Ctx(page, page.root))) for a in names]
            lis.append('<li>%s<span class="expanding"> — %s</span></li>' % (
                self.emit_a(page, cat.href, esc_text(cat.name + " attributes"), kind="attributecategory", name=cat.name),
                "".join(svgdefs.comma_list(items))))
        for an in e.common_attribute_names:
            lis.append("<li>%s</li>" % self.emit_link(page, R.element_attribute(name, an, Ctx(page, page.root))))
        for a in e.specific_attributes:
            lis.append("<li>%s</li>" % L(a))
        attrs_html = '<ul class="no-bullets">%s</ul>' % "".join(lis)

        geo = ""
        if e.geometry_properties:
            geo = '<dt>Geometry properties:</dt><dd><ul class="no-bullets">%s</ul></dd>' % "".join(
                "<li>%s</li>" % L(d.properties[pn]) for pn in e.geometry_properties)
        ifaces = '<ul class="no-bullets">%s</ul>' % "".join(
            "<li>%s</li>" % self.emit_link(page, R.interface(i, Ctx(page, page.root))) for i in e.interfaces)

        did = "elementdef-" + name
        nid = self.new_id(page, did)
        alias = self.single_page_alias(page, did)
        oldids = ' oldids="%s"' % esc_attr(alias) if alias else ""
        mp = ' data-multipage-id="%s"' % did if nid != did else ""
        self.bump("generated: element summaries")
        return ('<div class="element-summary"><div class="element-summary-name"><span class="element-name">'
                '%s<dfn data-dfn-type="element" data-export="" id="%s"%s%s>%s</dfn>%s</span></div><dl>'
                '<dt>Categories:</dt><dd>%s</dd>'
                '<dt>Content model:</dt><dd>%s</dd>'
                '<dt>Attributes:</dt><dd>%s</dd>%s'
                '<dt>DOM Interfaces:</dt><dd>%s</dd></dl></div>') % (
            LQUOTE, esc_attr(nid), oldids, mp, esc_text(name), RQUOTE, cat_html, cm, attrs_html, geo, ifaces)

    def gen_element_category(self, page, name):
        cat = self.spec.defs.element_categories[name]
        items = [self.emit_link(page, self.resolver.element(x, Ctx(page, page.root))) for x in sorted(cat.elements)]
        self.bump("generated: element category lists")
        return "".join(svgdefs.english_list(items))

    def gen_attribute_category(self, page, name, omit_quotes):
        d = self.spec.defs
        cat = d.attribute_categories[name]
        things = []
        for n in cat.presentation_attribute_names:
            things.append(d.presentation_attributes.get(n))
        for n in cat.common_attribute_names:
            things.append(d.common_attributes.get(n))
        things.extend(cat.attributes)
        # processing.js:777 sorts with a[0] - b[0] on strings, which keeps the
        # original order. Mirrored on purpose: same text as today.
        items = []
        for t in things:
            if t is None:
                items.append('<span class="xxx">@@ unknown attribute</span>')
            else:
                items.append(self.emit_link(page, svgdefs.format_thing(t, omit_quotes=omit_quotes)))
        self.bump("generated: attribute category lists")
        return "".join(svgdefs.english_list(items))

    def gen_elements_with_attribute_category(self, page, name, omit_quotes):
        d = self.spec.defs
        els = sorted([e for e in d.elements.values() if name in e.attribute_categories], key=lambda e: e.name)
        return "".join(svgdefs.english_list([self.emit_link(page, svgdefs.format_thing(e, omit_quotes=omit_quotes)) for e in els]))

    def gen_attribute_table(self, page):
        d = self.spec.defs
        rows = []
        for e in d.elements.values():
            for a in e.specific_attributes:
                rows.append((",".join([a.name, e.name]), a, [e], a.animatable))
        for cat in d.attribute_categories.values():
            els = sorted([e for e in d.elements.values() if cat.name in e.attribute_categories], key=lambda e: e.name)
            for a in cat.attributes:
                rows.append((",".join([a.name] + [e.name for e in els]), a, els, a.animatable))
        for a in d.common_attributes_for_elements:
            names = sorted(a.elements)
            rows.append((",".join([a.name] + names), a, [d.elements[n] for n in names], a.animatable))
        for a in d.common_attributes.values():
            # processing.js:713-726: indexOf(a) on a list of names never matches,
            # and firstIndexOfAny is used as a boolean. Mirrored.
            els = sorted([e for e in d.elements.values() if a.name in e.common_attribute_names], key=lambda e: e.name)
            rows.append((",".join([a.name] + [e.name for e in els]), a, els, a.animatable))
        rows.sort(key=lambda r: r[0])
        out = ['<table class="proptable attrtable"><thead><tr><th>Attribute</th><th>Elements on which the attribute may be specified</th><th title="Animatable">%s</th></tr></thead><tbody>' % self.emit_link(page, self.resolver.term("Anim.", Ctx(page, page.root)))]
        for _, a, els, anim in rows:
            out.append("<tr><th>%s</th><td>%s</td><td>%s</td></tr>" % (
                self.emit_link(page, svgdefs.format_thing(a, omit_quotes=True)),
                "".join(svgdefs.comma_list([self.emit_link(page, svgdefs.format_thing(e, omit_quotes=True)) for e in els])),
                "✓" if anim else ""))
        out.append("</tbody></table>")
        self.bump("generated: attribute table")
        return "".join(out)

    def gen_element_index(self, page):
        d = self.spec.defs
        items = ["<li>%s</li>" % self.emit_link(page, svgdefs.format_thing(d.elements[n])) for n in sorted(d.elements)]
        return '<ul class="element-index">%s</ul>' % "".join(items)

    def gen_idl_index(self, page):
        d = self.spec.defs
        names = sorted(n for n, i in d.interfaces.items() if ":" not in (i.href or ""))
        return "<ul>%s</ul>" % "".join("<li>%s</li>" % self.emit_link(page, svgdefs.format_thing(d.interfaces[n])) for n in names)

    # ---- the tree walk ----------------------------------------------------

    def children_html(self, page, el):
        out = []
        if el.text:
            out.append(esc_text(el.text))
        for c in el:
            out.append(self.node_html(page, c))
            if c.tail:
                out.append(esc_text(c.tail))
        return "".join(out)

    def id_markup(self, page, el, tag, attrs):
        """Rewrite the id attribute; return (attrs, oldids_value, alias_span)."""
        i = el.get("id")
        if i is None:
            return attrs, None, None
        nid = self.new_id(page, i)
        attrs = [(k, (nid if k == "id" else v)) for k, v in attrs]
        if nid != i:
            attrs.append(("data-multipage-id", i))
            self.bump("ids: clashing, renamed to single-page form")
        alias = self.single_page_alias(page, i)
        if not alias:
            return attrs, None, None
        if tag in ("h2", "h3", "h4", "h5", "h6", "dfn") or set(classes(el)) & {"issue", "example"}:
            return attrs, alias, None
        return attrs, None, '<span id="%s" class="bs-old-id"></span>' % esc_attr(alias)

    def open_tag(self, tag, attrs):
        return "<" + tag + "".join(' %s="%s"' % (k, esc_attr(v)) for k, v in attrs) + ">"

    def node_html(self, page, el):
        if el.tag is ET.Comment:
            return "<!--%s-->" % el.text
        if not isinstance(el.tag, str):
            return ""
        if is_edit(el):
            return self.edit_html(page, el)
        tag = local(el.tag)
        n = ns(el.tag)
        foreign = n in (SVG_NS, MATHML_NS)

        if not foreign and tag == "a":
            return self.a_html(page, el)
        if not foreign and tag == "pre" and "idl" in classes(el):
            return self.idl_html(page, el)

        attrs = []
        renames = self.cfg.get("class_renames", {})
        for k, v in el.attrib.items():
            name = attr_name(k)
            if name is None:
                # edit:href="...{{maturity}}..." and edit:datetime="{{date}}"
                # on the front page: the old build fills in the template.
                if ns(k) == EDIT_NS and local(k) in ("href", "datetime"):
                    attrs.append((local(k), self.fill_template(v)))
                    self.bump("front matter: edit:%s filled in" % local(k))
                continue
            if name == "class" and renames:
                new_v = " ".join(renames.get(c, c) for c in v.split())
                if new_v != v:
                    self.bump("classes renamed so Bikeshed leaves the element alone")
                v = new_v
            attrs.append((name, v))

        # formatQuotes (processing.js:1062-1078)
        inner_override = None
        before = after = ""
        if not foreign:
            txt = text_content(el)
            if len(txt) >= 2 and txt[0] == "'" and txt[-1] == "'":
                cls = el.get("class") or ""
                if "property" in cls:
                    inner_override = esc_text(txt[1:-1])
                    before, after = LQUOTE, RQUOTE
                elif re.search(r"(element|attr)-name", cls):
                    inner_override = esc_text(LQUOTE + txt[1:-1] + RQUOTE)

        # data-issue -> id issueN, as processing.js addIssueIDs does
        if not foreign and el.get("data-issue"):
            # processing.js addIssueIDs: any element with data-issue gets id issueN
            el.set("id", "issue" + el.get("data-issue"))
            page.ids.setdefault(el.get("id"), el)
            attrs = [(k, v) for k, v in attrs if k != "id"] + [("id", el.get("id"))]

        # IDL member prose: <b id=__svg__I__m> becomes the member's dfn
        if el.get("id") in page.promoted:
            info = self.spec.dfn_index[(page.name, el.get("id"))]
            tag = "dfn"
            attrs = [(k, v) for k, v in attrs if k != "class"] + [
                ("data-dfn-type", info["type"]), ("data-dfn-for", ", ".join(info["fors"])),
                ("data-lt", "|".join(info["lts"]))]
            if el.get("class"):
                attrs.append(("class", el.get("class")))
            self.bump("ids: IDL member prose turned into dfn")

        # every dfn carries its type (and for) explicitly
        if not foreign and tag == "dfn" and el in self.spec.dfn_attrs and el.get("id") not in page.promoted:
            typ, fors = self.spec.dfn_attrs[el]
            attrs = [(k, v) for k, v in attrs if k not in ("data-dfn-type", "data-dfn-for")]
            attrs.append(("data-dfn-type", typ))
            if fors:
                attrs.append(("data-dfn-for", ", ".join(fors)))
            if typ == "dfn" and el.get("data-export") is None and el.get("export") is None:
                # Bikeshed's default for plain dfns is "not exported" already;
                # saying so explicitly only silences its lint.
                attrs.append(("data-noexport", ""))
            if el in self.spec.dfn_lt_override:
                attrs = [(k, v) for k, v in attrs if k not in ("data-lt", "lt")]
                attrs.append(("data-lt", self.spec.dfn_lt_override[el]))
                self.bump("dfns: duplicate linking text, later copy given a distinct data-lt")
            if typ != el.get("data-dfn-type"):
                self.bump("dfns: type written out by the converter")

        # headings move down one level: the chapter title becomes the h2
        shift = self.cfg.get("heading_shift", 1)
        if page.kind == "index":
            # The front page keeps its levels (Abstract, Status and
            # Acknowledgments are h2 as in Bikeshed's own boilerplate), and
            # stays out of the numbering and the table of contents as today.
            shift = 0
            if not foreign and tag in HEADINGS and tag != "h1":
                cls = [c for c in (el.get("class") or "").split()]
                for c in ("no-num", "no-toc"):
                    if c not in cls:
                        cls.append(c)
                attrs = [(k, v) for k, v in attrs if k != "class"] + [("class", " ".join(cls))]
        if not foreign and tag in HEADINGS and tag != "h1" and shift:
            tag = "h%d" % min(6, int(tag[1]) + shift)

        alias_span = None
        oldids = None
        if not foreign:
            attrs, oldids, alias_span = self.id_markup(page, el, tag, attrs)
        elif el.get("id") is not None:
            alias = self.single_page_alias(page, el.get("id"))
            if alias:
                # An HTML <span> cannot sit inside SVG or MathML; an empty
                # element of the same language carries the alias instead.
                empty = "g" if n == SVG_NS else "mrow"
                before = '<%s id="%s"></%s>' % (empty, esc_attr(alias), empty)
                self.bump("ids: inside inline SVG/MathML, alias as an empty sibling")
        if oldids:
            attrs.append(("oldids", oldids))

        # A var whose text has a comma cannot go in 'Ignored Vars'; Bikeshed's
        # documented per-element switch is the ignore attribute.
        if not foreign and tag == "var" and "," in text_content(el) and el.get("ignore") is None:
            attrs.append(("ignore", ""))
            self.bump("vars: ignore attribute (text with a comma)")

        inner = inner_override if inner_override is not None else self.children_html(page, el)
        # The old build gives every annotation that has an id a self-link
        # (publish.js); Bikeshed only does that for issues and examples.
        if (not foreign and "annotation" in classes(el) and el.get("id")
                and not set(classes(el)) & {"issue", "example"}):
            inner = '<a class="self-link" href="#%s"></a>' % esc_attr(self.new_id(page, el.get("id"))) + inner
            self.bump("self-links written for annotations")
        if foreign:
            return before + self.open_tag(tag, attrs) + inner + "</%s>" % tag
        if tag in VOID:
            s = self.open_tag(tag, attrs)
            return (alias_span or "") + s
        if alias_span:
            if tag in PHRASING_OK or tag == "pre":
                return before + self.open_tag(tag, attrs) + alias_span + inner + "</%s>" % tag + after
            if tag == "tr":
                # put it into the first cell
                m = re.match(r"(\s*<t[dh][^>]*>)", inner)
                if m:
                    inner = m.group(1) + alias_span + inner[m.end():]
                    return self.open_tag(tag, attrs) + inner + "</tr>"
            return before + alias_span + self.open_tag(tag, attrs) + inner + "</%s>" % tag + after
        return before + self.open_tag(tag, attrs) + inner + "</%s>" % tag + after

    def a_html(self, page, el):
        href = el.get("href")
        if href is None and el.get("{%s}href" % EDIT_NS):
            # front page: <a edit:href="https://www.w3.org/standards/types#{{maturity}}">
            href = self.fill_template(el.get("{%s}href" % EDIT_NS))
            self.bump("front matter: edit:href filled in")
        if href is None and (el.text or len(el)):
            link = self.resolver.resolve(text_content(el), Ctx(page, el))
            return self.emit_link(page, link)
        attrs = []
        for k, v in el.attrib.items():
            name = attr_name(k)
            if name is None or name == "href":
                continue
            attrs.append((name, v))
        attrs, oldids, alias = self.id_markup(page, el, "a", attrs)
        inner = (alias or "") + self.children_html(page, el)
        if href is None:
            return self.open_tag("a", attrs) + inner + "</a>"
        return self.emit_a(page, href, inner, attrs, handwritten=True)

    def idl_html(self, page, el):
        # Bikeshed parses the IDL text itself and makes its own links, so only
        # the text goes in. The old hand links inside are counted, not kept.
        text, links = text_with_link_offsets(el)
        untyped = sum(1 for a in el.iter("{%s}a" % XHTML_NS) if a.get("href") is None)
        self.bump("idl: blocks", 1)
        self.bump("idl: links inside IDL left to Bikeshed", untyped + len(links))
        attrs = [("class", el.get("class"))]
        if el.get("{%s}excludefromidl" % EDIT_NS):
            # The old build adds class "extract" (processing.js:915-920), and
            # Bikeshed leaves pre.idl.extract out of its IDL index
            # (boilerplate.py addIDLSection), which is what the old complete
            # IDL appendix did. Not data-no-idl: that drops the IDL markup too.
            attrs = [("class", (el.get("class") or "") + " extract")]
            self.bump("idl: blocks marked edit:excludefromidl (class extract)")
        if el.get("id"):
            attrs.append(("id", self.new_id(page, el.get("id"))))
        # ids written inside the IDL (<b id=...>) would vanish with the markup:
        # keep them, and their single-page form, as empty spans just before.
        spans = []
        for inner in el.iter():
            if inner is el or not isinstance(inner.tag, str) or inner.get("id") is None:
                continue
            for i in (self.new_id(page, inner.get("id")), self.single_page_alias(page, inner.get("id"))):
                if i:
                    spans.append('<span id="%s" class="bs-old-id"></span>' % esc_attr(i))
            self.bump("ids: inside IDL blocks, kept as spans before the block")
        return "".join(spans) + self.open_tag("pre", attrs) + esc_text(text) + "</pre>"

    def rel(self, href):
        """Path from the output folder to a source file (examples, includes)."""
        first = href.split("/")[0]
        if first in self.cfg.get("link_resources", []):
            return href  # the folder is linked into the output folder
        return os.path.relpath(os.path.join(self.spec.master, href), self.out_dir)

    def edit_html(self, page, el):
        name = local(el.tag)
        if name == "with":
            inner = self.children_html(page, el)
            has_heading = any(isinstance(c.tag, str) and local(c.tag) in HEADINGS for c in el.iter())
            block = any(isinstance(c.tag, str) and local(c.tag) in BLOCKS for c in el)
            self.bump("edit:with")
            if has_heading or not self.cfg.get("edit_with_to_link_for_hint", True):
                return inner
            wrap = "div" if block else "span"
            return '<%s link-for-hint="%s">%s</%s>' % (wrap, esc_attr(el.get("element")), inner, wrap)
        if name == "elementsummary":
            return self.gen_element_summary(page, el.get("name"))
        if name == "elementcategory":
            return self.gen_element_category(page, el.get("name"))
        if name == "attributecategory":
            return self.gen_attribute_category(page, el.get("name"), el.get("omitquotes") == "yes")
        if name == "elementswithattributecategory":
            return self.gen_elements_with_attribute_category(page, el.get("name"), el.get("omitquotes") == "yes")
        if name == "attributetable":
            return self.gen_attribute_table(page)
        if name == "elementindex":
            return self.gen_element_index(page)
        if name == "idlindex":
            return self.gen_idl_index(page)
        if name == "completeidl":
            self.bump("generated: complete IDL (Bikeshed IDL index)")
            # today's single-page.html has the ids of the IDL copies on this
            # page as idl-<id>; keep those as empty spans
            spans = []
            for p in self.spec.pages:
                for pre in p.root.iter("{%s}pre" % XHTML_NS):
                    if "idl" not in classes(pre) or pre.get("{%s}excludefromidl" % EDIT_NS):
                        continue
                    for inner in pre.iter():
                        if inner is not pre and isinstance(inner.tag, str) and inner.get("id"):
                            alias = self.single_page_alias(page, inner.get("id"))
                            if alias:
                                spans.append('<span id="%s" class="bs-old-id"></span>' % esc_attr(alias))
            return "".join(spans) + '<div data-fill-with="idl-index"></div>'
        if name == "example":
            href = el.get("href")
            desc = el.get("description")
            nm = el.get("name") or ""
            parts = ['<div class="example"><pre class="include-code xml">path: %s</pre>' % esc_text(self.rel(href))]
            if el.get("image") == "yes":
                img = re.sub(r"\.svg$", ".png", href)
                alt = "Example " + nm + ((" — " + desc) if desc else "")
                parts.append('<div class="figure"><img alt="%s" src="%s"><p class="caption">Example %s</p></div>' % (
                    esc_attr(alt), esc_attr(img), esc_text(nm)))
            if el.get("link") == "yes":
                parts.append('<p class="view-as-svg"><a href="%s">View this example as SVG (SVG-enabled browsers only)</a></p>' % esc_attr(href))
                self.bump("links: generated example 'view as SVG'")
            parts.append("</div>")
            self.bump("generated: examples")
            return "".join(parts)
        if name == "includefile":
            self.bump("generated: included files")
            return '<pre class="include-code">path: %s</pre>' % esc_text(self.rel(el.get("href")))
        if name in ("whenmaturity",):
            if el.get("maturity") == self.spec.maturity:
                return self.children_html(page, el)
            return ""
        if name == "whenpublished":
            return self.children_html(page, el) if self.spec.maturity != "ED" else ""
        if name == "fulltoc":
            return ""  # Bikeshed writes the table of contents
        # Front page (Overview.html), as the old build fills it in
        # (tools/publish/processing.js doLongMaturity ... doCopyright).
        if name == "maturity":
            return esc_text(LONG_MATURITY.get(self.spec.maturity, self.spec.maturity))
        if name == "date":
            return "[DATE]"  # Bikeshed text macro: the build date
        if name in ("thisversion", "latestversion", "history"):
            v = self.spec.versions
            if name == "thisversion":
                ed = self.spec.maturity == "ED"
                if el.get("single-page") is not None:
                    actual = "single-page.html"
                    visible = v.get("cvs-single") if ed else v.get("this-single")
                else:
                    actual = visible = v.get("cvs") if ed else v.get("this")
            elif name == "latestversion":
                actual = visible = v.get("latest")
            else:
                actual = visible = v.get("historyURL")
            return '<a class="url" href="%s">%s</a>' % (esc_attr(actual or ""), esc_text(visible or ""))
        if name == "includelatesteditorsdraft":
            if self.spec.maturity == "ED":
                return ""
            cvs = self.spec.versions.get("cvs") or ""
            return ("<dt>Latest editor&#39;s draft:</dt><dd><a class=\"url\" href=\"%s\">%s</a></dd>"
                    % (esc_attr(cvs), esc_text(cvs)))
        if name == "copyright":
            return self.cfg.get("copyright_html", "")
        if name == "minimalreviewdate":
            return esc_text(self.spec.minimal_review_date)
        self.warnings.append(("%s.html" % page.name, "edit:%s not converted" % name))
        self.bump("edit:%s not converted" % name)
        return ""

    # ---- one page ---------------------------------------------------------

    def single_page_bs(self, page):
        """A module under specs/: one page, its own headings start at h2, and
        the front matter (div.head, abstract, status, table of contents) is
        Bikeshed's job, so it is left out."""
        body = page.body()
        drop_ids = set(self.cfg.get("frontmatter_drop_sections", []))
        out = []
        dropping = False
        for c in body:
            if isinstance(c.tag, str):
                tag = local(c.tag)
                if "head" in classes(c) and tag == "div":
                    continue
                h2s = [c] if tag == "h2" else list(c.iter("{%s}h2" % XHTML_NS))
                if h2s:
                    # a front-matter section runs until the next h2 that is
                    # not front matter, wherever that h2 sits
                    if all(h.get("id") in drop_ids for h in h2s):
                        dropping = True
                        continue
                    dropping = False
            if dropping:
                continue
            out.append(self.node_html(page, c))
            if c.tail:
                out.append(esc_text(c.tail))
        return "".join(out).strip() + "\n"

    def page_bs(self, page):
        if self.cfg.get("page_mode") == "single":
            return self.single_page_bs(page)
        body = page.body()
        out = []
        h1 = None
        for c in body:
            if isinstance(c.tag, str) and local(c.tag) == "h1":
                h1 = c
                break
        title = norm_ws(text_content(h1)) if h1 is not None else page.name
        if page.kind == "appendix":
            title = "Appendix %s: %s" % (page.number, title)
        old = []
        if h1 is not None and h1.get("id"):
            # mimereg.html has <h1 id="mimereg">: keep it, and its single-page form
            old = [self.new_id(page, h1.get("id")), self.single_page_alias(page, h1.get("id"))]
        oldids = ' oldids="%s"' % ", ".join(i for i in old if i) if old else ""
        out.append('<h2 id="chapter-%s" data-bs-page="%s"%s>%s</h2>\n' % (page.name, page.name, oldids, esc_text(title)))
        started = h1 is None
        if body.text and started:
            out.append(esc_text(body.text))
        for c in body:
            if c is h1:
                started = True
                if c.tail:
                    out.append(esc_text(c.tail))
                continue
            if not started:
                continue
            out.append(self.node_html(page, c))
            if c.tail:
                out.append(esc_text(c.tail))
        return "".join(out).rstrip() + "\n"


# -- front matter and index.bs ------------------------------------------------

def overview_metadata(spec, cfg):
    """Editors and abstract read from the index page (Overview.html)."""
    idx = [p for p in spec.pages if p.kind == "index"]
    editors, former, abstract = [], [], ""
    if not idx:
        return editors, former, abstract
    root = idx[0].root
    mode = None
    for el in root.iter():
        if not isinstance(el.tag, str):
            continue
        if local(el.tag) == "dt":
            t = norm_ws(text_content(el))
            mode = "former" if t.startswith("Former Editor") else ("editor" if t.startswith("Editor") else None)
        elif local(el.tag) == "dd" and mode:
            t = norm_ws(text_content(el))
            m = re.match(r"^(.*?),\s*(.*?)\s*<(.*)>$", t)
            if m:
                # bare address: Bikeshed adds the mailto: itself
                line = "%s, %s, %s" % (m.group(1), m.group(2).replace(",", ""), m.group(3))
            else:
                line = t
            if el.get("data-editor-id"):
                line += ", w3cid " + el.get("data-editor-id")
            (former if mode == "former" else editors).append(line)
    for h in root.iter("{%s}h2" % XHTML_NS):
        if h.get("id") == "abstract":
            par = idx[0].parent[h]
            sibs = list(par)
            texts = []
            for s in sibs[sibs.index(h) + 1:]:
                if isinstance(s.tag, str) and local(s.tag) in HEADINGS:
                    break
                if isinstance(s.tag, str):
                    texts.append(norm_ws(text_content(s)))
            abstract = " ".join(t for t in texts if t)
    return editors, former, abstract


def single_use_vars(spec, page_names):
    """<var> names used once in the whole document. Bikeshed warns about
    each one (it suspects a typo); the text is today's, so list them in
    'Ignored Vars' instead."""
    count = {}
    for n in page_names:
        for v in spec.page_by_name[n].root.iter("{%s}var" % XHTML_NS):
            t = norm_ws(text_content(v))
            count[t] = count.get(t, 0) + 1
    return sorted(t for t, c in count.items() if c == 1 and "," not in t and t)


def index_bs(spec, cfg, page_names, inline_dir=None, front_main=None):
    editors, former, abstract = overview_metadata(spec, cfg)
    md = []
    md.append("Title: " + spec.title)
    if front_main is not None:
        md.append("Local Boilerplate: header yes")
        if spec.versions.get("latest"):
            # today's pages point their canonical link at the latest TR version
            md.append("Canonical URL: " + spec.versions["latest"])
    iv = single_use_vars(spec, page_names)
    if iv:
        md.append("Ignored Vars: " + ", ".join(iv))
    for k, v in cfg.get("metadata", {}).items():
        md.append("%s: %s" % (k, v))
    md.append("Status: " + spec.maturity)
    if spec.versions.get("cvs"):
        md.append("ED: " + spec.versions["cvs"])
    if spec.versions.get("latest"):
        md.append("TR: " + spec.versions["latest"])
    for e in editors:
        md.append("Editor: " + e)
    for e in former:
        md.append("Former Editor: " + e)
    if abstract:
        md.append("Abstract: " + abstract)
    lines = ["<pre class=metadata>"] + md + ["</pre>", ""]
    if cfg.get("anchors"):
        # Pin links Bikeshed would otherwise resolve through its own data
        # to the targets today's spec uses (config "anchors").
        lines += ["<pre class=anchors>"] + cfg["anchors"] + ["</pre>", ""]
    if cfg.get("extra_css"):
        lines += ["<style>"] + cfg["extra_css"] + ["</style>", ""]
    if front_main:
        lines += ["<!-- front page, after the table of contents (Overview.html) -->", front_main]
    for n in page_names:
        if inline_dir:
            # Bikeshed runs its Markdown parser on every included file, even
            # with 'Markup Shorthands: markdown-block no' (includes.py:84), so
            # a line starting with '1. ' or '- ', or a blank line inside a <p>,
            # would change the text. The page files are therefore copied in,
            # not included. Only the main document honours markdown-block no.
            with io.open(os.path.join(inline_dir, n + ".bs"), encoding="utf-8") as f:
                lines.append("<!-- page: %s.bs -->" % n)
                lines.append(f.read())
        else:
            lines.append('<pre class=include>path: %s.bs</pre>' % n)
    lines += cfg.get("body_end_html", [])
    lines.append("")
    return "\n".join(lines)


def expected_ids(spec, conv, page_names):
    """For the measuring script: every id each converted page had in the source,
    and the id it should have in the Bikeshed output."""
    out = {}
    for n in page_names:
        p = spec.page_by_name[n]
        ids = {}
        for i in p.ids:
            ids[i] = dict(new=conv.new_id(p, i), alias=conv.single_page_alias(p, i))
        for s in p.summaries:
            i = "elementdef-" + s
            ids[i] = dict(new=conv.new_id(p, i), alias=conv.single_page_alias(p, i), generated=True)
        out[n] = ids
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--source", default=os.environ.get("SVGWG", "."),
                    help="svgwg checkout (default: $SVGWG or the current folder)")
    ap.add_argument("--config", default=os.path.join(HERE, "config", "svg2.json"))
    ap.add_argument("--out", default=os.path.join(HERE, "out"))
    ap.add_argument("--pages", default="",
                    help="comma-separated page names to include in index.bs (default: all chapters and appendices)")
    ap.add_argument("--assemble", choices=["inline", "include"], default="inline",
                    help="copy the page files into index.bs (default), or use <pre class=include>")
    ap.add_argument("--trace-links", action="store_true",
                    help="mark every in-spec link with data-svgtrace so measure.py can check where it lands")
    args = ap.parse_args(argv)

    with io.open(args.config, encoding="utf-8") as f:
        cfg = json.load(f)
    KEEP_STRAIGHT_APOSTROPHES[0] = cfg.get("keep_straight_apostrophes", True)
    spec = Spec(os.path.abspath(args.source), cfg)
    os.makedirs(args.out, exist_ok=True)
    out_dir = os.path.abspath(args.out)

    skip = set(cfg.get("skip_pages", []))
    all_pages = [p.name for p in spec.pages if p.name not in skip]
    wanted = set(n for n in args.pages.split(",") if n)
    page_names = [n for n in all_pages if n in wanted] if wanted else all_pages
    unknown = wanted - set(all_pages)
    if unknown:
        ap.error("unknown pages: " + ", ".join(sorted(unknown)))
    conv = Converter(spec, out_dir, set(page_names), trace=args.trace_links)

    for n in page_names:
        p = spec.page_by_name[n]
        with io.open(os.path.join(out_dir, n + ".bs"), "w", encoding="utf-8") as f:
            f.write(conv.page_bs(p))
    front_main = None
    idx = [p for p in spec.pages if p.kind == "index"]
    if cfg.get("front_matter") == "header_include" and idx:
        header, front_main = conv.header_include(idx[0])
        with io.open(os.path.join(out_dir, "header.include"), "w", encoding="utf-8") as f:
            f.write(header)
    with io.open(os.path.join(out_dir, "index.bs"), "w", encoding="utf-8") as f:
        f.write(index_bs(spec, cfg, page_names, inline_dir=out_dir if args.assemble == "inline" else None,
                         front_main=front_main))

    # Folders the generated pages point into (images, style) are linked, not copied.
    for res in cfg.get("link_resources", []):
        dst = os.path.join(out_dir, res)
        if not os.path.lexists(dst):
            os.symlink(os.path.join(spec.master, res), dst)

    # For singlepage.py: which pages the chapter navigation bars name.
    def page_of(href):
        n = (href or "").split("#")[0]
        n = n[:-5] if n.endswith(".html") else n
        return n if n in spec.page_by_name else None
    nav = dict(pages=page_names,
               index=[p.name for p in spec.pages if p.kind == "index"],
               elements=page_of(spec.nav.get("elementindex")),
               attributes=page_of(spec.nav.get("attributeindex")),
               properties=page_of(spec.nav.get("propertyindex")),
               toc=bool(spec.nav.get("toc")),
               appendix_letters=dict((p.name, p.number) for p in spec.pages if p.kind == "appendix"),
               drop_headings=cfg.get("single_page_drop_headings", []))
    with io.open(os.path.join(out_dir, "single-page-nav.json"), "w", encoding="utf-8") as f:
        json.dump(nav, f, indent=1)
    with io.open(os.path.join(out_dir, "trace-links.json"), "w", encoding="utf-8") as f:
        json.dump(conv.trace_rows, f, indent=0)
    with io.open(os.path.join(out_dir, "expected-ids.json"), "w", encoding="utf-8") as f:
        json.dump(expected_ids(spec, conv, page_names), f, indent=1, sort_keys=True)
    with io.open(os.path.join(out_dir, "convert-report.json"), "w", encoding="utf-8") as f:
        json.dump(dict(stats=conv.stats, warnings=conv.warnings, pages=page_names,
                       page_mode=cfg.get("page_mode", "chapters"),
                       clashing_ids=sorted(spec.clashing), duplicate_dfns=spec.dfn_duplicates),
                  f, indent=1, sort_keys=True)
    for k in sorted(conv.stats):
        print("%6d  %s" % (conv.stats[k], k))
    for w in conv.warnings:
        print("warning: %s: %s" % w)


if __name__ == "__main__":
    main()
