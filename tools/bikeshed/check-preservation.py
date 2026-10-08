#!/usr/bin/env python3
"""Check that a new build of SVG 2 keeps every id and every link of a baseline.

The rule for the Bikeshed conversion: no id may disappear and no link may
land somewhere else, in both the multipage and the single-page versions.

Two commands, standard library only (html.parser, no lxml):

  extract  Read a directory of pages (multipage) plus one single-page file and
           write the baseline tables (TSV files) into an output directory.

      check-preservation.py extract \
          --multipage baseline/live-2026-10-08 \
          --single baseline/live-2026-10-08/single-page.html \
          --out baseline

  check    Read new output, compare it with the baseline tables, print what was
           lost. Exit status 1 when anything was lost, 0 otherwise.

      check-preservation.py check --baseline baseline \
          --multipage /path/to/new/multipage-dir \
          --single /path/to/new/single-page.html

Pages are named by file name. The front page is called index.html; a file
named Overview.html in a new build is read as index.html (the old build
writes Overview.html and the deploy script renames it).

What counts as an anchor: every id attribute on any element, and every name
attribute on an <a> element (HTML lets a fragment find either).

What counts as a link: every <a href> (and <area href>), plus every other
href, xlink:href or src whose target is inside the spec
(https://w3c.github.io/svgwg/svg2-draft/). Each link is resolved against the
page it sits on, giving a target page and a target fragment.

How a link is judged (check). A baseline link is first paired with a new
link (see pair_links: same page, same kind, same text once the format is
set aside, same section of the page, lined up like a text diff). Then the
two targets are looked up in the NEW build, and the link is kept when:

  - both fragments land on the same element: the same id, or an alias of
    it (Bikeshed's oldids span, class bs-old-id, or the empty marker the
    converter puts next to an element); or
  - the new link lands on a definition (a dfn) in the same section as the
    old target. That is the usual Bikeshed and CSS convention for typed
    links (decided 2026-10-08); these are listed, not hidden.
    --no-definition-landing counts them as losses.

A link that lands elsewhere in the same section is a loss, unless
--allow-same-section (then listed separately). A link that still exists but
now sits in another section of its page is a loss, unless --allow-moved.
--strict gives back the original rule: any change of fragment string is a
change, and links are paired by exact tidy text.

--losses-tsv writes one row per loss (verdict, area of the page, source,
text, old and new target), for grouping.
"""

import argparse
import csv
import difflib
import html
import os
import re
import sys
from collections import Counter, defaultdict
from html.parser import HTMLParser
from urllib.parse import unquote, urljoin, urlsplit

SPEC_BASE = "https://w3c.github.io/svgwg/svg2-draft/"
SINGLE = "single-page.html"
INDEX = "index.html"
VOID = {
    "area", "base", "br", "col", "embed", "hr", "img", "input", "link",
    "meta", "param", "source", "track", "wbr",
}
QUOTES = "‘’“”'\""


def tidy_text(s):
    s = re.sub(r"\s+", " ", s).strip()
    return s.strip(QUOTES).replace("‘", "").replace("’", "")


def page_name(filename):
    return INDEX if filename == "Overview.html" else filename


def resolve(href, source_page):
    """Return (internal, target_page, fragment, full_url)."""
    href = html.unescape(href).strip()
    url = urljoin(SPEC_BASE + source_page, href)
    parts = urlsplit(url)
    norm = url
    if parts.scheme == "http" and parts.netloc == "w3c.github.io":
        norm = "https" + url[4:]
    if norm.startswith(SPEC_BASE):
        rest = urlsplit(norm)
        path = rest.path[len(urlsplit(SPEC_BASE).path):]
        if path == "":
            path = INDEX
        # Note: a link written as "Overview.html" is NOT mapped to index.html,
        # because live has no Overview.html (404). Only file names are mapped.
        return True, path, unquote(rest.fragment), norm
    return False, "", unquote(parts.fragment), url


HEADING_TAGS = {"h1", "h2", "h3", "h4", "h5", "h6"}
ALIAS_TAGS = {"span", "g", "mrow"}


class PageParser(HTMLParser):
    """Collects anchors and links, and a light copy of the element tree.

    The tree is kept as flat lists indexed by element number (the order of
    the start tags): tag, parent, class, and the children of each element
    in order, where a run of non-blank text is noted as -1. That is enough to
    say which element a fragment lands on, and which heading's section it
    sits in.
    """

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []  # list of [tag, id_or_None, element_number]
        self.anchors = []  # (value, attr, tag, line, ancestor_id)
        self.links = []  # dicts
        self.open_links = []  # indices into self.links for open <a>
        self.el_tag = []
        self.el_parent = []
        self.el_class = []
        self.el_dfn = []  # True for a definition: <dfn>, or any element with data-dfn-type
        self.el_children = []
        self.el_section = []  # element number of the heading whose section holds it
        self.id_el = {}  # anchor value -> element number (first one wins, as in browsers)
        self.last_heading = -1
        self.section_name = ""  # id naming the section we are in (see _start)
        self.head_name = {}  # heading element -> that name

    def nearest_id(self):
        for tag, ident, _ in reversed(self.stack):
            if ident:
                return ident
        return ""

    def _start(self, tag, attrs, selfclosing):
        tag = tag.lower()
        a = {}
        for k, v in attrs:
            a[k.lower()] = v if v is not None else ""
        line = self.getpos()[0]
        ancestor = self.nearest_id()
        num = len(self.el_tag)
        parent = self.stack[-1][2] if self.stack else -1
        self.el_tag.append(tag)
        self.el_parent.append(parent)
        self.el_class.append(a.get("class", ""))
        self.el_dfn.append(tag == "dfn" or "data-dfn-type" in a)
        self.el_children.append([])
        if parent >= 0:
            self.el_children[parent].append(num)
        if tag in HEADING_TAGS:
            self.last_heading = num
            # a heading with no id of its own (the old single page's chapter
            # <h1>) is named by its closest ancestor with an id
            self.section_name = a.get("id") or ancestor
            self.head_name[num] = self.section_name
        self.el_section.append(self.last_heading)
        if "id" in a:
            self.anchors.append((a["id"], "id", tag, line, ancestor))
            self.id_el.setdefault(a["id"], num)
        if tag == "a" and "name" in a:
            self.anchors.append((a["name"], "name", tag, line, ancestor))
            self.id_el.setdefault(a["name"], num)
        a_link = None
        for attr in ("href", "xlink:href", "src"):
            if attr not in a:
                continue
            internal, tpage, frag, url = resolve(a[attr], self.page)
            is_anchor_link = tag in ("a", "area") and attr in ("href", "xlink:href")
            if not is_anchor_link and not internal:
                continue
            self.links.append({
                "kind": "%s@%s" % (tag, attr),
                "source_id": ancestor,
                "own_id": a.get("id") or a.get("name") or "",
                "section_id": self.section_name,
                "el": num,
                "line": line,
                "raw": a[attr],
                "internal": internal,
                "page": tpage,
                "fragment": frag,
                "url": url,
                "text": "",
            })
            if is_anchor_link and a_link is None:
                a_link = len(self.links) - 1
        if not selfclosing and tag not in VOID:
            self.stack.append([tag, a.get("id"), num])
            if tag == "a":
                self.open_links.append(a_link)

    def handle_starttag(self, tag, attrs):
        self._start(tag, attrs, False)

    def handle_startendtag(self, tag, attrs):
        self._start(tag, attrs, True)

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag in VOID:
            return
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                break
        if tag == "a" and self.open_links:
            self.open_links.pop()

    def handle_data(self, data):
        for idx in self.open_links:
            if idx is not None:
                self.links[idx]["text"] += data
        if data.strip() and self.stack:
            kids = self.el_children[self.stack[-1][2]]
            if not kids or kids[-1] != -1:
                kids.append(-1)


class Doc(object):
    """Where each fragment of one page lands."""

    def __init__(self, p):
        self.tag = p.el_tag
        self.parent = p.el_parent
        self.cls = p.el_class
        self.dfn = p.el_dfn
        self.head_name = p.head_name
        self.children = p.el_children
        self.section = p.el_section
        self.id_el = p.id_el

    def is_alias(self, n):
        """An empty marker element whose only job is to carry an extra id:
        Bikeshed's oldids span (class bs-old-id), or the empty <span>, <g> or
        <mrow> the converter writes next to an element for the same reason."""
        if self.tag[n] not in ALIAS_TAGS or self.children[n]:
            return False
        c = self.cls[n].split()
        return c == ["bs-old-id"] or (not c and self.tag[n] != "span")

    def _blank_before(self, n):
        """True when nothing but secno spans, empty self-links (Bikeshed adds
        both) and other markers come before n."""
        par = self.parent[n]
        if par < 0:
            return False
        for k in self.children[par]:
            if k == n:
                return True
            if k == -1:
                return False
            c = self.cls[k].split()
            if not (self.is_alias(k) or "secno" in c
                    or (self.tag[k] == "a" and "self-link" in c and not self.children[k])):
                return False
        return True

    def _next_element(self, n):
        """The element right after n, skipping other markers; None when text
        or nothing comes first."""
        par = self.parent[n]
        if par < 0:
            return None
        kids = self.children[par]
        i = kids.index(n) + 1
        while i < len(kids):
            k = kids[i]
            if k == -1:
                return None
            if not self.is_alias(k):
                return k
            i += 1
        return None

    def spot(self, frag):
        """The set of elements a fragment lands on, or None when absent.

        A real element: itself. A marker (see is_alias): the element it marks,
        which is its parent when it is the first thing inside it (that is
        where Bikeshed's oldids puts it), and the element right after it when
        it sits just before one (the converter does that where a span cannot
        go inside). When both apply, both count, because both are the same
        spot on screen.
        """
        n = self.id_el.get(frag)
        if n is None:
            return None
        if not self.is_alias(n):
            return frozenset([n])
        out = set()
        if self._blank_before(n):
            p = self.parent[n]
            out.add(p)
            # Bikeshed wraps the text of an IDL dfn in <code>: the marker then
            # sits in the <code>, which is the first thing in the dfn.
            while self.tag[p] in ("code", "span") and self._blank_before(p):
                p = self.parent[p]
                out.add(p)
        nxt = self._next_element(n)
        if nxt is not None:
            out.add(nxt)
        if not out:
            out.add(self.parent[n])
        return frozenset(out)

    def section_of(self, spot):
        return {self.section[n] for n in spot}

    def is_definition(self, spot):
        return any(self.dfn[n] for n in spot)


def parse_page(path, page):
    p = PageParser()
    p.page = page
    with open(path, encoding="utf-8", errors="replace") as f:
        p.feed(f.read())
    p.close()
    for l in p.links:
        l["text"] = re.sub(r"\s+", " ", l["text"]).strip()
        l["tidy"] = tidy_text(l["text"])
    return p.anchors, p.links, Doc(p)


def read_set(multipage_dir, single_file):
    """Return {'multi': {page: (anchors, links)}, 'single': {page: ...}}."""
    multi = {}
    if multipage_dir:
        for fn in sorted(os.listdir(multipage_dir)):
            if not fn.endswith(".html") or fn == SINGLE:
                continue
            multi[page_name(fn)] = parse_page(os.path.join(multipage_dir, fn), page_name(fn))
    single = {}
    if single_file:
        single[SINGLE] = parse_page(single_file, SINGLE)
    return {"multi": multi, "single": single}


def anchor_sets(pages):
    return {p: {a[0] for a in anchors} for p, (anchors, _, _d) in pages.items()}


def annotate_links(pages, all_anchor_sets, known_pages):
    """Add 'exists' and 'seq' to every link."""
    for page, (_, links, _d) in pages.items():
        seen = Counter()
        for l in links:
            key = (l["kind"], l["tidy"])
            l["seq"] = seen[key]
            seen[key] += 1
            if not l["internal"]:
                l["exists"] = "external"
            elif l["page"] not in known_pages:
                l["exists"] = "page-not-in-set"
            elif l["fragment"] == "":
                l["exists"] = "yes"
            elif l["fragment"] in all_anchor_sets.get(l["page"], set()):
                l["exists"] = "yes"
            else:
                l["exists"] = "NO"


def annotate(data):
    sets = {}
    sets.update(anchor_sets(data["multi"]))
    sets.update(anchor_sets(data["single"]))
    known = set(data["multi"]) | set(data["single"])
    annotate_links(data["multi"], sets, known)
    annotate_links(data["single"], sets, known)
    return sets


def write_tsv(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n", quoting=csv.QUOTE_MINIMAL)
        w.writerow(header)
        for r in rows:
            w.writerow(r)


def read_tsv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter="\t"))


# <link href> and <script src> load style sheets and scripts; readers do not
# follow them, so they are not compared unless --strict.
HEAD_RESOURCE_KINDS = ("link@href", "script@src")

LINK_HEADER = ["source_page", "kind", "tidy_text", "seq", "source_id", "line",
               "link_text", "raw_href", "internal", "target_page",
               "target_fragment", "target_exists", "url", "source_section", "own_id"]


def link_rows(pages):
    for page, (_, links, _d) in pages.items():
        for l in links:
            yield [page, l["kind"], l["tidy"], l["seq"], l["source_id"], l["line"],
                   l["text"], l["raw"], "1" if l["internal"] else "0", l["page"],
                   l["fragment"], l["exists"], l["url"], l["section_id"], l["own_id"]]


def cmd_extract(args):
    data = read_set(args.multipage, args.single)
    annotate(data)
    os.makedirs(args.out, exist_ok=True)
    for label, pages in (("multipage", data["multi"]), ("single-page", data["single"])):
        ids, dups, counts = [], [], []
        for page, (anchors, links, _d) in pages.items():
            c = Counter(a[0] for a in anchors)
            for value, attr, tag, line, anc in anchors:
                ids.append([page, value, attr, tag, line, anc])
            for value, n in sorted(c.items()):
                if n > 1:
                    ctx = ["%s %s line %d in #%s" % (tag, attr, line, anc or "-")
                           for v, attr, tag, line, anc in anchors if v == value]
                    dups.append([page, value, n, " | ".join(ctx)])
            counts.append([page, len(anchors), len(c), sum(1 for v in c.values() if v > 1),
                           len(links), sum(1 for l in links if l["internal"]),
                           sum(1 for l in links if l["exists"] == "NO")])
        write_tsv(os.path.join(args.out, label + "-ids.tsv"),
                  ["page", "anchor", "attr", "tag", "line", "ancestor_id"], ids)
        write_tsv(os.path.join(args.out, label + "-duplicate-ids.tsv"),
                  ["page", "anchor", "occurrences", "contexts"], dups)
        write_tsv(os.path.join(args.out, label + "-links.tsv"), LINK_HEADER, link_rows(pages))
        if label == "multipage":
            where = defaultdict(list)
            for page, (anchors, _, _d) in pages.items():
                for v in sorted({a[0] for a in anchors}):
                    where[v].append(page)
            write_tsv(os.path.join(args.out, "multipage-ids-on-several-pages.tsv"),
                      ["anchor", "page_count", "pages"],
                      sorted(([v, len(ps), " ".join(ps)] for v, ps in where.items()
                              if len(ps) > 1), key=lambda r: (-r[1], r[0])))
        write_tsv(os.path.join(args.out, label + "-page-counts.tsv"),
                  ["page", "anchor_attrs", "distinct_anchors", "duplicated_anchors",
                   "links", "internal_links", "broken_internal_links"], counts)
        broken = [r for r in link_rows(pages) if r[11] == "NO"]
        write_tsv(os.path.join(args.out, label + "-broken-links.tsv"), LINK_HEADER, broken)
    print("baseline written to", args.out)
    return 0


def match_text(s):
    """Link text as used to pair an old link with a new one. More forgiving
    than tidy_text: only the format may differ, not the words. Removes
    every quote mark, a leading section sign, and a leading section number
    ("10.2.", "10.2", "B.1." all go; "A path" stays, because a lone capital
    only counts as a number when a dot follows it)."""
    s = re.sub(r"\s+", " ", s or "").strip().lstrip("§").strip()
    for q in QUOTES + "«»":
        s = s.replace(q, "")
    s = re.sub(r"^(?:\d+|[A-Z](?=\.))(?:\.\d+)*\.?\s+(?=\S)", "", s)
    return re.sub(r"\s+", " ", s).strip()


class Lander(object):
    """Says where a (page, fragment) lands in the NEW set of pages.

    Both the old link and the new link are looked up in the new build: the
    old fragment is still there as an id or an alias marker (the id check
    makes sure of that), so the question "does the new link go to the same
    place as the old one" becomes "do the two fragments land on the same
    element of the new page"."""

    def __init__(self, pages):
        self.docs = {p: d for p, (_a, _l, d) in pages.items()}

    def spot(self, page, frag):
        """('page', frozenset of element numbers), ('top', page) for a link to
        the top of a page, ('absent', ...) when the page or fragment is not in
        the new set, or None for a page outside the set (images, style)."""
        d = self.docs.get(page)
        if d is None:
            return None
        if frag == "":
            return ("top", page)
        sp = d.spot(frag)
        if sp is None:
            return ("absent", page, frag)
        return (page, sp)

    def key(self, page, frag):
        """One hashable value per landing spot, for lining links up."""
        sp = self.spot(page, frag)
        if sp is None or sp[0] in ("top", "absent"):
            return (page, frag)
        return (page, min(sp[1]))

    def section(self, sp):
        return self.docs[sp[0]].section_of(sp[1])

    def is_definition(self, sp):
        return self.docs[sp[0]].is_definition(sp[1])


def link_target(d, baseline, lander):
    if baseline:
        if d["internal"] != "1":
            return d["url"]
        return lander.key(d["target_page"], d["target_fragment"])
    if not d["internal"]:
        return d["url"]
    return lander.key(d["page"], d["fragment"])


def lands_alike(lander, r, n, test):
    """Does baseline row r and new link n land on the same element (test
    "element") or in the same section (test "section") of the new build?"""
    if r["internal"] != "1" or not n["internal"]:
        return r["internal"] != "1" and not n["internal"] and r["url"] == n["url"]
    a = lander.spot(r["target_page"], r["target_fragment"])
    b = lander.spot(n["page"], n["fragment"])
    if a is None or b is None or a[0] in ("top", "absent") or b[0] in ("top", "absent"):
        return (r["target_page"], r["target_fragment"]) == (n["page"], n["fragment"])
    if a[0] != b[0]:
        return False
    if a[1] & b[1]:
        return True
    return test == "section" and bool(lander.section(a) & lander.section(b))


def pair_links(base_links, pages, lander, base_ids, strict=False):
    """Pair each baseline link (by row index) with a new link, or with None.
    Returns (pairing, how) where how[i] is "text", "target" or "moved".

    Context. Every link sits in a section of its page: the last heading
    before it, named by its id (a heading without an id is named by its
    closest ancestor with an id; text before any heading has the name "").
    The baseline table records that name. It is looked up in the new build;
    a new link's section is the nearest heading before it that the baseline
    knows (see new_ctx). An old link and a new link are "in the same place"
    when those agree. Without this,
    a link that disappeared from the front page would be hidden by an extra
    link with the same text anywhere else on the single page.

    Links are grouped by (source page, kind, link text as given by
    match_text). Then, in this order, each step only looking at links the
    earlier steps left unpaired:

    1. Same group, same section: the old and new lists are lined up with
       difflib, the way a text diff lines up two files, comparing where
       each link lands. One link added or removed in the middle of a page
       does not make every later link with the same text look changed.
    2. Same group, same section: links that land on the same element.
    3. Same page and kind, same section, any text: a new link that lands on
       the same element and whose text is close (difflib ratio 0.5 or more,
       or one text contains the other). This catches a table of contents
       entry whose numbering or wording format changed. Listed in its own
       section of the report.
    4. Same group, same section: links that land in the same section.
    5. Same group, same section: what is left, in page order. Those pairs
       show as "lands elsewhere", which is what they are.
    6. Steps 2, 4 and 5 again without the section condition. These links
       still exist but now sit in another part of the page; they are
       reported as "moved" (a loss unless --allow-moved).

    A baseline table without the source_section column (made by an older
    version of this script) skips the section condition.

    In strict mode only step 1 runs, with the old tidy_text grouping, no
    section condition, and a difflib "replace" block paired by position
    (the original behaviour).
    """
    def mt(x):
        return tidy_text(x) if strict else match_text(x)

    has_ctx = (not strict) and bool(base_links) and "source_section" in base_links[0]
    known = {}  # page -> {heading element -> nearest heading at or before it known to the baseline}
    if has_ctx:
        for page, d in lander.docs.items():
            ids = base_ids.get(page, set())
            k = set(n for n, nm in d.head_name.items() if nm in ids)
            for i in ids:
                sp = d.spot(i)
                if sp:
                    k.update(n for n in sp if d.tag[n] in HEADING_TAGS)
            m, cur = {}, -1
            for n in range(len(d.tag)):
                if d.tag[n] in HEADING_TAGS:
                    if n in k:
                        cur = n
                    m[n] = cur
            m[-1] = -1
            known[page] = m
    old_cache = {}

    def old_ctx(r):
        """The section of a baseline link, as a set of elements of the new
        page (the elements its section name lands on), or {-1} for text
        before any heading, or the bare name when the new page lacks it."""
        if not has_ctx:
            return None
        key = (r["source_page"], r.get("source_section") or "")
        if key not in old_cache:
            d = lander.docs.get(key[0])
            sp = d.spot(key[1]) if (d is not None and key[1]) else None
            if not key[1]:
                old_cache[key] = frozenset([-1])
            elif sp:
                old_cache[key] = frozenset(sp)
            else:
                old_cache[key] = frozenset([("absent", key[1])])
        return old_cache[key]

    def new_ctx(page, l):
        """The section of a new link: the nearest heading before it that the
        baseline knows (by its id or an alias on it). Headings that only the
        new build has, such as Bikeshed's "IDL Index" or "Table of Contents",
        do not start a section of their own."""
        if not has_ctx:
            return None
        d = lander.docs.get(page)
        return known[page].get(d.section[l["el"]], -1)

    set_cache = {}

    def ctx_set(page, h):
        """Elements of the new page that stand for heading h: itself and
        whatever its name (its id, or its closest ancestor's) lands on."""
        if h == -1:
            return frozenset([-1])
        key = (page, h)
        if key not in set_cache:
            d = lander.docs[page]
            sp = d.spot(d.head_name.get(h, "")) or frozenset()
            set_cache[key] = frozenset(sp) | {h}
        return set_cache[key]

    new_page = {}
    for page, (_, links, _d) in pages.items():
        for l in links:
            new_page[id(l)] = page

    def same_place(r, l):
        if not has_ctx:
            return True
        pg = new_page[id(l)]
        return bool(ctx_set(pg, new_ctx(pg, l)) & old_ctx(r))

    base_groups = defaultdict(list)
    for i, r in enumerate(base_links):
        base_groups[(r["source_page"], r["kind"], mt(r["link_text"]))].append(i)
    new_groups = defaultdict(list)
    for page, (_, links, _d) in pages.items():
        for l in links:
            new_groups[(page, l["kind"], mt(l["text"]))].append(l)
    pairing, how, used = {}, {}, set()

    def take(i, n, kind):
        pairing[i] = n
        how[i] = kind
        used.add(id(n))

    # step 1
    for key, idxs in base_groups.items():
        news = new_groups.get(key, [])
        sub_old = defaultdict(list)
        for i in idxs:
            sub_old[old_ctx(base_links[i])].append(i)
        for c, sidx in sub_old.items():
            if c is None:
                snews = news
            else:
                snews = [n for n in news if same_place(base_links[sidx[0]], n)]
            if not snews:
                continue
            a = [link_target(base_links[i], True, lander) for i in sidx]
            b = [link_target(n, False, lander) for n in snews]
            sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
            for op, i1, i2, j1, j2 in sm.get_opcodes():
                if op == "equal" or (op == "replace" and strict):  # strict: old behaviour
                    for k in range(i2 - i1):
                        j = j1 + k
                        if j < j2:
                            take(sidx[i1 + k], snews[j], "text")
    if strict:
        return pairing, how

    def in_group(test, ctx, kind="text"):
        for key, idxs in base_groups.items():
            free = [n for n in new_groups.get(key, []) if id(n) not in used]
            if not free:
                continue
            for i in idxs:
                if i in pairing:
                    continue
                r = base_links[i]
                for n in free:
                    if id(n) in used:
                        continue
                    if ctx and not same_place(r, n):
                        continue
                    if test is None or lands_alike(lander, r, n, test):
                        take(i, n, kind)
                        break

    in_group("element", True)  # step 2
    # step 3
    leftovers = defaultdict(list)  # (page, kind, page landed, element) -> new links
    for page, (_, links, _d) in pages.items():
        for l in links:
            if id(l) in used or not l["internal"]:
                continue
            sp = lander.spot(l["page"], l["fragment"])
            if sp is None or sp[0] in ("top", "absent"):
                continue
            for n in sp[1]:
                leftovers[(page, l["kind"], sp[0], n)].append(l)
    for i, r in enumerate(base_links):
        if i in pairing or r["internal"] != "1":
            continue
        sp = lander.spot(r["target_page"], r["target_fragment"])
        if sp is None or sp[0] in ("top", "absent"):
            continue
        t_old = match_text(r["link_text"])
        best = None
        for n in sorted(sp[1]):
            for l in leftovers.get((r["source_page"], r["kind"], sp[0], n), []):
                if id(l) in used or not same_place(r, l):
                    continue
                t_new = match_text(l["text"])
                close = (t_old == t_new or (t_old and t_new and (t_old in t_new or t_new in t_old))
                         or difflib.SequenceMatcher(None, t_old, t_new).ratio() >= 0.5)
                if close and (best is None or l["line"] < best["line"]):
                    best = l
        if best is not None:
            take(i, best, "target")
    in_group("section", True)  # step 4
    in_group(None, True)  # step 5
    if has_ctx:  # step 6
        in_group("element", False, "moved")
        in_group("section", False, "moved")
        in_group(None, False, "moved")
    return pairing, how


def area_of(r):
    """Rough place of a baseline link on its page, for grouping losses."""
    sid = r["source_id"] or ""
    if r["kind"] != "a@href":
        return "head (%s)" % r["kind"]
    if sid == "toc" or sid.endswith("-toc") or sid.endswith("-Contents"):
        return "table of contents" if sid in ("toc",) else "chapter table of contents"
    if sid.startswith("chapter-Overview") or sid.startswith("Overview-"):
        return "front page"
    if sid.startswith("chapter-") or "-" in sid or sid:
        return "chapter text"
    return "outside any id"


LOSS_HEADER = ["verdict", "area", "source_page", "source_id", "kind", "link_text", "seq",
               "old_target", "new_target"]


def cmd_check(args):
    data = read_set(args.multipage, args.single)
    new_sets = annotate(data)
    losses = 0
    report = []
    loss_rows = []

    def section(title, rows):
        report.append("== %s: %d" % (title, len(rows)))
        for r in rows[: args.limit]:
            report.append("   " + r)
        if len(rows) > args.limit:
            report.append("   ... %d more" % (len(rows) - args.limit))

    summary = []
    for label, pages, check_this in (("multipage", data["multi"], args.multipage),
                                     ("single-page", data["single"], args.single)):
        if not check_this:
            continue
        lander = Lander(pages)
        base_ids = read_tsv(os.path.join(args.baseline, label + "-ids.tsv"))
        base_pairs = {(r["page"], r["anchor"]) for r in base_ids}
        # every baseline page has to exist, including pages with no anchor
        base_counts = read_tsv(os.path.join(args.baseline, label + "-page-counts.tsv"))
        missing_pages = sorted({r["page"] for r in base_counts} - set(pages))
        missing_ids = sorted((p, a) for p, a in base_pairs
                             if a not in new_sets.get(p, set()))
        section("%s: baseline pages missing" % label, missing_pages)
        section("%s: baseline (page, id) missing" % label,
                ["%s#%s" % pa for pa in missing_ids])
        for p, a in missing_ids:
            loss_rows.append(["id missing", "-", p, "", "", "", "", "%s#%s" % (p, a), ""])

        base_links = read_tsv(os.path.join(args.baseline, label + "-links.tsv"))
        base_id_sets = defaultdict(set)
        for r in base_ids:
            base_id_sets[r["page"]].add(r["anchor"])
        pairing, how = pair_links(base_links, pages, lander, base_id_sets, strict=args.strict)
        changed, vanished, dangling, still_broken, ext_changed = [], [], [], [], []
        old_gone, same_section, same_section_ok, by_target = [], [], [], []
        on_definition, moved, moved_ok = [], [], []
        self_links = []
        head_resources = []
        same_elem = 0
        for i, r in enumerate(base_links):
            where = "%s (in #%s) %s %r #%s" % (r["source_page"], r["source_id"] or "-",
                                             r["kind"], r["link_text"][:60], r["seq"])
            old_t = "%s#%s" % (r["target_page"], r["target_fragment"])
            if not args.strict and r["kind"] in HEAD_RESOURCE_KINDS:
                # Style sheets and scripts are not links a reader follows.
                # Decided 2026-10-08: the Bikeshed version uses Bikeshed's
                # W3C style and drops the old SVG 2 style sheets and scripts.
                head_resources.append("%s -> %s" % (where, r["raw_href"]))
                continue

            def lose(verdict, n=None):
                loss_rows.append([verdict, area_of(r), r["source_page"], r["source_id"], r["kind"],
                                  r["link_text"], r["seq"],
                                  old_t if r["internal"] == "1" else r["url"],
                                  "" if n is None else ("%s#%s" % (n["page"], n["fragment"])
                                                        if n["internal"] else n["url"])])

            n = pairing.get(i)
            if r["internal"] != "1":
                if n is None or n["url"] != r["url"]:
                    ext_changed.append("%s: %s -> %s" % (where, r["url"],
                                                         n["url"] if n else "(no link)"))
                    if args.strict_external:
                        lose("external changed", n)
                continue
            if ((n is None or how.get(i) == "moved") and not args.strict
                    and not args.keep_self_links
                    and r.get("own_id") and r["own_id"] == r["target_fragment"]
                    and r["target_page"] == r["source_page"]
                    and r["target_fragment"] in new_sets.get(r["source_page"], set())):
                # A link that points at its own id (SVG 2 IDL member names).
                # Decided 2026-10-08: follow Bikeshed, which makes the
                # name the definition itself. Kept as long as the id survives.
                # On the single page the pairing may match it to a link with
                # the same text in another section ("moved"); that match is
                # wrong, the original link is simply gone.
                self_links.append("%s -> %s (pointed at itself; id kept)" % (where, old_t))
                continue
            if n is None:
                vanished.append("%s -> %s (link not found)" % (where, old_t))
                lose("vanished")
                continue
            if how.get(i) == "moved":
                if args.allow_moved:
                    moved_ok.append("%s -> now in another section of the page, line %s"
                                    % (where, n["line"]))
                else:
                    moved.append("%s -> now in another section of the page, line %s"
                                 % (where, n["line"]))
                    lose("moved to another section", n)
                    continue
            if how.get(i) == "target":
                by_target.append("%s %r -> %s#%s" % (where, n["text"][:60], n["page"],
                                                     n["fragment"]))
            new_t = "%s#%s" % (n["page"] or n["url"], n["fragment"])
            arrow = "%s: %s -> %s" % (where, old_t, new_t)
            same_string = (n["page"], n["fragment"]) == (r["target_page"], r["target_fragment"])
            if args.strict or not n["internal"]:
                if not same_string:
                    changed.append(arrow)
                    lose("changed", n)
                    continue
            elif not same_string:
                old_sp = lander.spot(r["target_page"], r["target_fragment"])
                new_sp = lander.spot(n["page"], n["fragment"])
                if old_sp is None or new_sp is None:
                    changed.append(arrow + " (outside the set, strings differ)")
                    lose("changed", n)
                    continue
                if old_sp[0] == "absent":
                    old_gone.append(arrow + " (old id not in the new build)")
                    lose("old target id gone", n)
                    continue
                if new_sp[0] == "absent":
                    dangling.append(arrow + " (new target does not exist)")
                    lose("new target missing", n)
                    continue
                if old_sp[0] == "top" or new_sp[0] == "top" or old_sp[0] != new_sp[0]:
                    changed.append(arrow + " (other page or page top)")
                    lose("changed: other page", n)
                    continue
                if old_sp[1] & new_sp[1]:
                    same_elem += 1
                    continue
                if lander.section(old_sp) & lander.section(new_sp):
                    if lander.is_definition(new_sp) and not args.no_definition_landing:
                        on_definition.append(arrow)
                    elif args.allow_same_section:
                        same_section_ok.append(arrow)
                    else:
                        same_section.append(arrow)
                        lose("changed: same section", n)
                    continue
                changed.append(arrow)
                lose("changed: elsewhere", n)
                continue
            if r["target_exists"] == "yes" and n["exists"] == "NO":
                dangling.append("%s -> %s#%s (target id gone)" % (where, n["page"],
                                                                  n["fragment"]))
                lose("dangling", n)
            elif r["target_exists"] == "NO" and n["exists"] == "NO":
                still_broken.append("%s -> %s#%s" % (where, n["page"], n["fragment"]))
        if label == "multipage" and os.path.isdir(os.path.join(args.multipage, "images")):
            res_missing = sorted({"%s (from %s)" % (l["page"], page)
                                  for page, (_, links, _d) in pages.items() for l in links
                                  if l["exists"] == "page-not-in-set"
                                  and not os.path.exists(os.path.join(args.multipage,
                                                                      l["page"]))})
            section("multipage: images/style files linked but absent from the new "
                    "directory (not counted as loss)", res_missing)
        section("%s: links whose target changed (lands elsewhere)" % label, changed)
        section("%s: links whose old target id is not in the new build" % label, old_gone)
        section("%s: links that land in the same section but not on the same element "
                "(counted as loss; --allow-same-section to accept)" % label, same_section)
        section("%s: links that land on the definition (a dfn) in the same section as "
                "before, the usual Bikeshed and CSS convention for typed links (not counted "
                "as loss, listed for review; --no-definition-landing to count them)" % label,
                on_definition)
        section("%s: links that land in the same section, accepted by "
                "--allow-same-section (not counted as loss)" % label, same_section_ok)
        section("%s: links that pointed at their own id, replaced by Bikeshed's "
                "definition; the id is kept (not counted as loss; --keep-self-links to "
                "count them)" % label, self_links)
        section("%s: style sheet and script references, not compared (--strict to "
                "compare them)" % label, head_resources)
        section("%s: links that vanished (no matching link found)" % label, vanished)
        section("%s: links found only in another section of the page (counted as loss; "
                "--allow-moved to accept)" % label, moved)
        section("%s: links found only in another section of the page, accepted by "
                "--allow-moved (not counted as loss)" % label, moved_ok)
        section("%s: links that point to nothing in the new build" % label, dangling)
        section("%s: links paired by where they land because their text format changed "
                "(not a loss, listed for review)" % label, by_target)
        section("%s: links already broken in the baseline, still broken (not a loss)" % label,
                still_broken)
        section("%s: external links changed (%s)" % (
            label, "counted as loss" if args.strict_external else "not counted as loss"),
            ext_changed)
        loss = (len(missing_pages) + len(missing_ids) + len(changed) + len(old_gone)
                + len(same_section) + len(vanished) + len(dangling) + len(moved)
                + (len(ext_changed) if args.strict_external else 0))
        losses += loss
        summary.append("%s: %d baseline anchors, %d missing; %d baseline links "
                       "(%d internal); %d changed, %d old id gone, %d same section%s, "
                       "%d vanished, %d self-links dropped, %d moved, %d dangling; %d land on the same element under another "
                       "fragment; %d on the definition in the same section; "
                       "%d paired by target; %d external changed; "
                       "%d already broken; %d style sheet and script references not compared; LOSSES %d"
                       % (label, len(base_pairs), len(missing_ids), len(base_links),
                          sum(1 for r in base_links if r["internal"] == "1"),
                          len(changed), len(old_gone),
                          len(same_section) + len(same_section_ok),
                          " (accepted)" if args.allow_same_section else "",
                          len(vanished), len(self_links), len(moved) + len(moved_ok), len(dangling), same_elem,
                          len(on_definition),
                          len(by_target),
                          len(ext_changed), len(still_broken), len(head_resources), loss))
        if args.strict:
            summary[-1] += " [strict: fragment strings compared]"
    groups = Counter((r[0], r[1]) for r in loss_rows)
    print("\n".join(report))
    print("\n== LOSSES BY VERDICT AND AREA")
    for (v, a), c in sorted(groups.items(), key=lambda x: -x[1]):
        print("%7d  %s / %s" % (c, v, a))
    print("\n== SUMMARY")
    print("\n".join(summary))
    print("TOTAL LOSSES:", losses)
    if args.losses_tsv:
        write_tsv(args.losses_tsv, LOSS_HEADER, loss_rows)
    return 1 if losses else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    e = sub.add_parser("extract")
    e.add_argument("--multipage", required=True)
    e.add_argument("--single", required=True)
    e.add_argument("--out", required=True)
    c = sub.add_parser("check")
    c.add_argument("--baseline", required=True, help="directory with the baseline TSV files")
    c.add_argument("--multipage", help="directory of new multipage output")
    c.add_argument("--single", help="new single-page file")
    c.add_argument("--limit", type=int, default=50, help="rows shown per section")
    c.add_argument("--strict-external", action="store_true",
                   help="count changed external links as losses too")
    c.add_argument("--strict", action="store_true",
                   help="old behaviour: a link is changed whenever its fragment string "
                        "differs, even when it lands on the same element; text paired "
                        "as tidy_text only, no pairing by target")
    c.add_argument("--allow-same-section", action="store_true",
                   help="accept a link that lands inside the same smallest section as "
                        "before (listed separately, not counted as loss)")
    c.add_argument("--no-definition-landing", action="store_true",
                   help="count a link that now lands on the definition (dfn) in the same "
                        "section as a loss (by default it is preserved and listed)")
    c.add_argument("--allow-moved", action="store_true",
                   help="accept a link that still exists and lands in the same place but "
                        "now sits in another section of its page")
    c.add_argument("--keep-self-links", action="store_true",
                   help="count a lost link that pointed at its own id as a loss "
                        "(by default accepted when the id survives)")
    c.add_argument("--losses-tsv", help="write every loss, one row each, to this TSV file")
    args = ap.parse_args()
    if args.cmd == "check" and not (args.multipage or args.single):
        ap.error("check needs --multipage and/or --single")
    return cmd_extract(args) if args.cmd == "extract" else cmd_check(args)


if __name__ == "__main__":
    sys.exit(main())
