#!/usr/bin/env python3
"""Cut a single-page Bikeshed build of SVG 2 into today's chapter pages.

Usage:

    split.py --single WORK/index.html --out OUT \
             --config config/svg2-split.json [--resources /path/to/svgwg/master] \
             [--link-resources]

(build.sh in this folder runs it with the right arguments.)

Python 3.9 or later, standard library only.

What it does, in order:

  1. Finds the chapter starts: headings carrying a page marker attribute
     (`bs-page`, the name used by Tab's unmerged Bikeshed `pagesplit` branch,
     or `data-bs-page`, which released Bikeshed keeps). Everything in <main>
     before the first marker, the Bikeshed header above <main> and the
     Bikeshed back matter after </main> (Index, References, Issues Index)
     go to the front page.
  2. Rewrites every `#id` link whose target ended up on another page into
     `page.html#id`, including the data that drives Bikeshed's "Referenced in"
     panels (dfnPanelData) and link hints (refsData).
  3. Puts back the chapter-page ids that one big document cannot hold twice:
     elements marked `data-multipage-id` get their short id back, and every
     single-page alias `<page>-<id>` gets a sibling `<id>` anchor when that id
     is not already on the page. Makes each page's `toc` and `Contents` ids.
  4. Writes a header per page like today's (title, Overview / Previous / Next
     bar, the same style sheet and script links), a per-page table of
     contents, the full table of contents on the front page, and appendix
     letters (A.1., B.2.3., ...), which Bikeshed does not produce.
  5. Copies (or links) style/, images/ and the removed-chapter stub pages.
  6. Writes fragment-links.json (which page holds each id) and
     split-report.json (what it did and anything it could not resolve).

Nothing here is specific to one laptop: every path comes from the command
line, and everything specific to SVG 2 (page order, titles, body classes,
navigation links) comes from the configuration file.
"""

import argparse
import bisect
import html
import json
import os
import re
import shutil
import sys
from collections import defaultdict
from html.parser import HTMLParser
from urllib.parse import quote, unquote

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link",
        "meta", "param", "source", "track", "wbr"}
# Elements whose end tag is never left out in Bikeshed output. Used to check
# that a chapter start is not inside an open wrapper element.
BALANCED = {"div", "section", "table", "ul", "ol", "dl", "pre", "aside",
            "figure", "details", "blockquote", "svg", "math", "nav", "main"}
HEADINGS = {"h1", "h2", "h3", "h4", "h5", "h6"}


# ---------------------------------------------------------------------------
# Reading the single page: one pass that records where every tag starts and
# ends in the original text. All later changes are made by replacing slices of
# the original text, so whatever we do not touch stays byte for byte as
# Bikeshed wrote it.
# ---------------------------------------------------------------------------

class Tag:
    __slots__ = ("kind", "name", "attrs", "start", "end", "raw", "index")

    def __init__(self, kind, name, attrs, start, end, raw, index):
        self.kind = kind      # "start" or "end"
        self.name = name
        self.attrs = attrs    # dict (start tags only)
        self.start = start    # offset of "<"
        self.end = end        # offset just after ">"
        self.raw = raw
        self.index = index

    def get(self, key, default=None):
        return self.attrs.get(key, default)


class Scanner(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.text = text
        self.line_starts = [0]
        for m in re.finditer("\n", text):
            self.line_starts.append(m.end())
        self.tags = []

    def _abs(self):
        line, col = self.getpos()
        return self.line_starts[line - 1] + col

    def _start(self, name, attrs):
        start = self._abs()
        raw = self.get_starttag_text()
        a = {}
        for k, v in attrs:
            a.setdefault(k.lower(), v if v is not None else "")
        self.tags.append(Tag("start", name.lower(), a, start, start + len(raw), raw,
                             len(self.tags)))

    def handle_starttag(self, name, attrs):
        self._start(name, attrs)

    def handle_startendtag(self, name, attrs):
        self._start(name, attrs)

    def handle_endtag(self, name):
        start = self._abs()
        end = self.text.index(">", start) + 1
        self.tags.append(Tag("end", name.lower(), {}, start, end, self.text[start:end],
                             len(self.tags)))


def scan(text):
    s = Scanner(text)
    s.feed(text)
    s.close()
    return s.tags


def matching_end(tags, i):
    """Index of the end tag closing the start tag tags[i] (same name, nesting)."""
    name = tags[i].name
    depth = 0
    for j in range(i, len(tags)):
        t = tags[j]
        if t.name != name:
            continue
        if t.kind == "start":
            depth += 1
        else:
            depth -= 1
            if depth == 0:
                return j
    raise ValueError("no end tag for <%s> at offset %d" % (name, tags[i].start))


ATTR_RE = r'(\s%s\s*=\s*)("[^"]*"|\'[^\']*\'|[^\s"\'>]+)'


def set_attr(raw, name, value):
    """Return the start tag text `raw` with attribute `name` set to `value`."""
    qv = '"%s"' % html.escape(value, quote=True).replace("&#x27;", "'")
    pat = re.compile(ATTR_RE % re.escape(name), re.I)
    if pat.search(raw):
        return pat.sub(lambda m: m.group(1) + qv, raw, count=1)
    close = "/>" if raw.endswith("/>") else ">"
    return raw[: -len(close)] + " %s=%s" % (name, qv) + close


def rename_tag(raw, new):
    return re.sub(r"^(</?)[A-Za-z0-9]+", lambda m: m.group(1) + new, raw)


def strip_tags(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s))


def esc(s):
    return html.escape(s, quote=True)


# ---------------------------------------------------------------------------
# Edits: (start, end, replacement) on the original text. Start tags that get
# several changes (renamed, an attribute rewritten, something inserted after)
# are collected in one TagEdit so the changes do not collide.
# ---------------------------------------------------------------------------

class TagEdit:
    def __init__(self, tag):
        self.tag = tag
        self.rename = None
        self.attrs = {}
        self.after = []   # text inserted right after the start tag

    def render(self):
        raw = self.tag.raw
        if self.rename:
            raw = rename_tag(raw, self.rename)
        for k, v in self.attrs.items():
            raw = set_attr(raw, k, v)
        return raw + "".join(self.after)


class Edits:
    def __init__(self):
        self.tag_edits = {}
        self.plain = []        # (start, end, text, order)
        self.blocked = []      # (start, end): ranges replaced as a whole

    def tag(self, tag):
        if tag.start not in self.tag_edits:
            self.tag_edits[tag.start] = TagEdit(tag)
        return self.tag_edits[tag.start]

    def replace(self, start, end, text):
        self.plain.append((start, end, text, len(self.plain)))

    def insert(self, pos, text):
        self.plain.append((pos, pos, text, len(self.plain)))

    def block(self, start, end, text):
        self.blocked.append((start, end))
        self.replace(start, end, text)

    def inside_block(self, start, end):
        for b0, b1 in self.blocked:
            if b0 <= start and end <= b1 and not (start == b0 and end == b1):
                return True
        return False

    def apply(self, text, lo, hi):
        """Return text[lo:hi] with every edit inside that range applied."""
        items = []
        for te in self.tag_edits.values():
            t = te.tag
            if lo <= t.start and t.end <= hi and not self.inside_block(t.start, t.end):
                items.append((t.start, t.end, te.render(), -1))
        for s, e, txt, order in self.plain:
            if lo <= s and e <= hi and not self.inside_block(s, e):
                items.append((s, e, txt, order))
        # at the same offset, insertions (zero width) go before a replacement
        # that starts there: they belong to what comes before
        items.sort(key=lambda x: (x[0], 0 if x[1] == x[0] else 1, x[3]))
        out, pos = [], lo
        for s, e, txt, _ in items:
            if s < pos:
                raise ValueError("overlapping edits at offset %d" % s)
            out.append(text[pos:s])
            out.append(txt)
            pos = e
        out.append(text[pos:hi])
        return "".join(out)


# ---------------------------------------------------------------------------
# The splitter
# ---------------------------------------------------------------------------

class Splitter:
    def __init__(self, single_path, config):
        self.cfg = config
        with open(single_path, encoding="utf-8") as f:
            self.text = f.read()
        self.tags = scan(self.text)
        self.report = defaultdict(list)
        self.edits = Edits()

    # -- 1. find the regions and the chapter starts -------------------------

    def locate(self):
        t = self.tags
        first = {}
        for tag in t:
            key = (tag.kind, tag.name)
            if key not in first:
                first[key] = tag
        self.html_tag = first[("start", "html")]
        self.head_open = first[("start", "head")]
        self.body_open = first[("start", "body")]
        # Bikeshed leaves out </head>, </body> and </html>
        self.head_end = first[("end", "head")].start if ("end", "head") in first \
            else self.body_open.start
        body_close = [x for x in t if x.kind == "end" and x.name == "body"]
        self.body_close_start = body_close[-1].start if body_close else len(self.text)
        main_i = first[("start", "main")].index
        self.main_open = t[main_i]
        self.main_close = t[matching_end(t, main_i)]

        # Bikeshed's table of contents, replaced by ours
        self.toc_nav = None
        for x in t:
            if x.kind == "start" and x.name == "nav" and x.get("id") == "toc":
                self.toc_nav = (x, t[matching_end(t, x.index)])
                break

        markers = self.cfg.get("page_marker_attributes", ["bs-page", "data-bs-page"])
        names = [p["name"] for p in self.cfg["pages"]]
        self.chapter_starts = []   # (name, tag index of the heading)
        for x in t[main_i + 1:self.main_close.index]:
            if x.kind != "start":
                continue
            for m in markers:
                if m in x.attrs:
                    self.chapter_starts.append((x.attrs[m], x.index))
                    break
        found = [n for n, _ in self.chapter_starts]
        if found != names:
            missing = [n for n in names if n not in found]
            extra = [n for n in found if n not in names]
            raise SystemExit("page markers do not match the config: missing %s, "
                             "unexpected %s, order %s" % (missing, extra, found))

        # every chapter start must sit directly in <main>: no wrapper left open
        depth = 0
        stack_at = {}
        starts = {i for _, i in self.chapter_starts}
        for x in t[main_i + 1:self.main_close.index]:
            if x.index in starts:
                stack_at[x.index] = depth
            if x.name in BALANCED:
                depth += 1 if x.kind == "start" else -1
        for name, i in self.chapter_starts:
            if stack_at[i] != 0:
                raise SystemExit("chapter %s starts inside an open element (depth %d); "
                                 "the converter must put the marked heading directly "
                                 "in <main>" % (name, stack_at[i]))

        # page regions in the original text: list of (lo, hi) slices
        self.pages = []
        fp = self.cfg["front_page"]
        self.front = {"name": "index", "file": fp["file"], "href": fp.get("href", fp["file"]),
                      "prefix": fp.get("single_page_prefix", "index"), "front": True}
        bounds = [t[i].start for _, i in self.chapter_starts] + [self.main_close.start]
        for k, (name, i) in enumerate(self.chapter_starts):
            pc = self.cfg["pages"][k]
            self.pages.append({"name": name, "file": name + ".html", "href": name + ".html",
                               "prefix": name, "front": False, "cfg": pc,
                               "slices": [(bounds[k], bounds[k + 1])],
                               "heading": i, "appendix": bool(pc.get("appendix"))})

        # front page: Bikeshed header (body start to <main>, minus its ToC),
        # the part of <main> before the first chapter, then the back matter
        # after </main> without the scripts.
        lo = self.body_open.end
        front_slices = []
        if self.toc_nav:
            front_slices.append((lo, self.toc_nav[0].start))
            self.front_toc_pos = len(front_slices)
            front_slices.append((self.toc_nav[1].end, self.main_open.start))
        else:
            self.front_toc_pos = 1
            front_slices.append((lo, self.main_open.start))
        front_slices.append((self.main_open.end, bounds[0]))
        self.scripts = []
        back = []
        pos = self.main_close.end
        k = self.main_close.index + 1
        while k < len(t) and t[k].start < self.body_close_start:
            x = t[k]
            if x.kind == "start" and x.name == "script":
                e = t[matching_end(t, k)]
                back.append((pos, x.start))
                self.scripts.append(self.text[x.start:e.end])
                pos = e.end
                k = e.index + 1
                continue
            k += 1
        back.append((pos, self.body_close_start))
        self.back_slices = back
        self.front["slices"] = front_slices
        self.all_pages = [self.front] + self.pages
        self.by_name = {p["name"]: p for p in self.all_pages}

    # -- ids: which page holds what -----------------------------------------

    def page_of_offset(self, off):
        for p in self.all_pages:
            for lo, hi in p["slices"]:
                if lo <= off < hi:
                    return p
        if self.cfg.get("back_matter_page", "index") == "index":
            for lo, hi in self.back_slices:
                if lo <= off < hi:
                    return self.front
        return None

    def collect_ids(self):
        if self.cfg.get("back_matter_page", "index") == "index":
            self.front["slices"] = self.front["slices"] + self.back_slices
        self.id_tag = {}            # id -> Tag
        self.id_page = {}           # id -> page dict (original ids)
        self.page_ids = defaultdict(set)
        dropped = set()
        if self.toc_nav:
            dropped = set(range(self.toc_nav[0].index, self.toc_nav[1].index + 1))
        for x in self.tags:
            if x.kind != "start" or "id" not in x.attrs or x.index in dropped:
                continue
            p = self.page_of_offset(x.start)
            if p is None:
                continue
            i = x.attrs["id"]
            if i in self.id_tag:
                self.report["duplicate id in single page"].append(i)
                continue
            self.id_tag[i] = x
            self.id_page[i] = p
            self.page_ids[p["name"]].add(i)
        self.id_offsets = sorted((t.start, i) for i, t in self.id_tag.items())

    # -- 3. put back the chapter-page ids ------------------------------------

    def restore_ids(self):
        """Alias map: id written in the single page -> (page, id to use)."""
        self.alias = {}
        self.restored = []
        ed = self.edits
        # a. elements the converter marked with data-multipage-id
        for i, x in list(self.id_tag.items()):
            short = x.get("data-multipage-id")
            if short is None:
                continue
            p = self.id_page[i]
            if short in self.page_ids[p["name"]]:
                self.report["data-multipage-id already on page"].append("%s#%s" % (p["file"], short))
                continue
            if x.name in HEADINGS:
                te = ed.tag(x)
                te.attrs["id"] = short
                te.after.insert(0, '<span class="bs-old-id" id="%s"></span>' % esc(i))
            else:
                ed.tag(x).after.insert(0, '<span class="bs-old-id" id="%s"></span>' % esc(short))
            self.page_ids[p["name"]].add(short)
            self.alias[i] = (p, short)
            self.restored.append((p["file"], short, "data-multipage-id", i))
        # b. single-page aliases "<page>-<id>" written as bs-old-id spans
        for i, x in list(self.id_tag.items()):
            p = self.id_page[i]
            pre = p["prefix"] + "-"
            if not i.startswith(pre) or i in self.alias:
                continue
            short = i[len(pre):]
            if short in self.page_ids[p["name"]]:
                self.alias[i] = (p, short)
                continue
            if x.name == "span" and "bs-old-id" in x.get("class", "").split():
                end = self.tags[matching_end(self.tags, x.index)]
                ed.insert(end.end, '<span class="bs-old-id" id="%s"></span>' % esc(short))
                self.page_ids[p["name"]].add(short)
                self.alias[i] = (p, short)
                self.restored.append((p["file"], short, "single-page alias", i))
            else:
                self.report["info: page-prefixed id that is not a single-page alias (left as is)"].append(
                    "%s#%s" % (p["file"], i))

    # -- 2. links -------------------------------------------------------------

    def target(self, frag):
        """(page, id) for a fragment of the single page, or None."""
        if frag in self.alias:
            return self.alias[frag]
        if frag in self.id_page:
            return (self.id_page[frag], frag)
        return None

    def href_for(self, frag, from_page, qualify=False, raw=None):
        tg = self.target(frag)
        if tg is None:
            return None
        page, ident = tg
        if not page["front"] and ident == self.tags[page["heading"]].get("id"):
            # the chapter heading itself: the live pages link to the page
            # with no fragment ("conform.html")
            return page["href"]
        if raw is not None and ident == frag:
            hash_part = raw
        else:
            hash_part = "#" + quote(ident, safe="!$&'()*+,;=:@/?-._~")
        if page is from_page and not qualify:
            return hash_part
        return page["href"] + hash_part

    def rewrite_links(self):
        self.link_changes = defaultdict(int)
        self.href_map = defaultdict(dict)   # page name -> {old href: new href}
        for x in self.tags:
            if x.kind != "start" or x.name not in ("a", "area") or "href" not in x.attrs:
                continue
            href = x.attrs["href"]
            if not href.startswith("#") or len(href) < 2:
                continue
            p = self.page_of_offset(x.start)
            if p is None:
                continue
            frag = unquote(href[1:])
            new = self.href_for(frag, p, raw=href)
            if new is None:
                self.report["link to an id that exists nowhere"].append(
                    "%s: %s" % (p["file"], href))
                continue
            if new != href:
                self.edits.tag(x).attrs["href"] = new
                self.href_map[p["name"]][href] = new
                self.link_changes[p["name"]] += 1

    # -- 4. headings, numbering, tables of contents -----------------------------

    def read_bikeshed_toc(self):
        """Headings as Bikeshed listed them: (level, id, secno, content html)."""
        entries = []
        if not self.toc_nav:
            raise SystemExit("no <nav id=toc> in the single page")
        t = self.tags
        depth = 0
        k = self.toc_nav[0].index
        while k <= self.toc_nav[1].index:
            x = t[k]
            if x.name == "ol":
                depth += 1 if x.kind == "start" else -1
            if x.kind == "start" and x.name == "a" and x.get("href", "").startswith("#"):
                e = t[matching_end(t, k)]
                inner = self.text[x.end:e.start]
                m = re.match(r'\s*(?:<span class="secno">([^<]*)</span>)?\s*'
                             r'<span class="content">(.*)</span>\s*$', inner, re.S)
                secno, content = (m.group(1) or "", m.group(2)) if m else ("", inner)
                entries.append({"level": depth, "id": unquote(x.attrs["href"][1:]),
                                "secno": secno.strip(), "content": content})
                k = e.index
            k += 1
        return entries

    def number_headings(self):
        """Give every page its ToC entries and the live section numbers."""
        entries = self.read_bikeshed_toc()
        chapter_ids = {}
        for p in self.pages:
            chapter_ids[self.tags[p["heading"]].get("id")] = p
        letters = self.cfg.get("appendix_letters", "ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        appendix_n = 0
        current = None
        counters = []
        self.heading_title = {}   # original heading id -> (secno, text) for panels
        for p in self.all_pages:
            p["toc"] = []
        for e in entries:
            if e["level"] == 1:
                current = chapter_ids.get(e["id"])
                if current is None:
                    # a top-level entry that is not a chapter (Bikeshed's Index,
                    # References, ...): front page, unnumbered
                    self.front["toc"].append(dict(e, number=""))
                    continue
                if current["appendix"]:
                    current["letter"] = letters[appendix_n]
                    appendix_n += 1
                    current["number"] = current["letter"]
                else:
                    current["number"] = e["secno"].rstrip(".")
                current["toc_content"] = e["content"]
                counters = []
                continue
            if current is None:
                self.front["toc"].append(dict(e, number=""))
                continue
            rel = e["level"] - 1   # 1 for a section directly under the chapter
            if current["appendix"]:
                counters = counters[:rel]
                while len(counters) < rel:
                    counters.append(0)
                counters[rel - 1] += 1
                number = current["letter"] + "." + ".".join(str(c) for c in counters) + "."
                self.insert_secno(e["id"], number)
            else:
                number = (e["secno"].rstrip(".") + ".") if e["secno"] else ""
            entry = dict(e, number=number, rel=rel)
            current["toc"].append(entry)
            self.heading_title[e["id"]] = (number, strip_tags(e["content"]).strip())

    def insert_secno(self, ident, number):
        x = self.id_tag.get(ident)
        if x is None or x.name not in HEADINGS:
            self.report["appendix ToC entry without heading"].append(ident)
            return
        self.edits.tag(x).after.append('<span class="secno">%s </span>' % esc(number))

    def toc_list(self, entries, page, cls, base_level):
        """Nested <ol> for entries (each with 'rel'), links qualified with the page."""
        out = []
        stack = []
        for e in entries:
            lvl = e["rel"] - base_level + 1
            while len(stack) > lvl:
                out.append("</li></ol>")
                stack.pop()
            if len(stack) == lvl:
                out.append("</li>")
            while len(stack) < lvl:
                out.append('<ol class="%s">' % cls)
                stack.append(1)
            href = self.href_for(e["id"], page, qualify=True) or ("#" + e["id"])
            num = '<span class="secno">%s</span> ' % esc(e["number"]) if e["number"] else ""
            out.append('<li><a href="%s">%s%s</a>' % (esc(href), num, e["content"]))
        while stack:
            out.append("</li></ol>")
            stack.pop()
        return "".join(out)

    def full_toc(self):
        fp = self.cfg["front_page"]
        parts = ['<nav id="toc" data-never-rename="">\n  <h2 id="%s">%s</h2>\n  <ol class="toc">'
                 % (esc(fp.get("toc_heading_id", "fulltoc")),
                    esc(fp.get("toc_heading_text", "Table of Contents")))]
        for p in self.pages:
            if p["appendix"]:
                head = '<li><a href="%s">%s</a>' % (esc(p["href"]), p["toc_content"])
            else:
                head = '<li><span class="secno">%s.</span> <a href="%s">%s</a>' % (
                    esc(p["number"]), esc(p["href"]), p["toc_content"])
            parts.append(head)
            if p["toc"]:
                parts.append(self.toc_list(p["toc"], self.front, "toc", 1))
            parts.append("</li>")
        parts.append("</ol>\n</nav>\n")
        # Bikeshed's own lowercase "contents" id, kept so nothing that
        # pointed at it is lost
        return "".join(parts).replace("</h2>", '<span id="contents"></span></h2>', 1)

    def header_html(self, k):
        """h1, navigation bar and per-page table of contents of chapter page k."""
        p = self.pages[k]
        nav = self.cfg["nav"]
        h = self.tags[p["heading"]]
        hend = self.tags[matching_end(self.tags, h.index)]
        inner = self.text[h.end:hend.start]
        if p["cfg"].get("h1"):
            h1 = p["cfg"]["h1"]
        elif p["appendix"]:
            h1 = strip_tags(p["toc_content"]).strip()
        else:
            h1 = self.cfg.get("chapter_h1_format", "Chapter {number}: {text}").format(
                number=p["number"], text=strip_tags(p["toc_content"]).strip())
        # The live <h1> has no id, except where the source gave the chapter
        # heading one (mimereg.html: id="mimereg"). Use that id if the
        # converter carried it as a short (unprefixed) old id; keep every
        # other id, including the converter's "chapter-<name>", as an empty
        # span inside the heading.
        hid = h.get("id")
        spans = re.findall(r'<span class="bs-old-id" id="([^"]*)"></span>', inner)
        own = [i for i in spans if not i.startswith(p["prefix"] + "-")]
        h1_id = own[0] if own else None
        keep = [i for i in ([hid] if hid else []) + spans if i != h1_id]
        old_spans = "".join('<span class="bs-old-id" id="%s"></span>' % esc(i) for i in keep)
        out = ['<h1 id="%s">%s%s</h1>' % (esc(h1_id), old_spans, esc(h1)) if h1_id else
               "<h1>%s%s</h1>" % (old_spans, esc(h1))]
        links = ['<a href="%s">%s</a>' % (esc(self.front["href"]), esc(nav["overview_text"]))]
        if k > 0:
            links.append('<a href="%s">%s</a>' % (esc(self.pages[k - 1]["href"]),
                                                   esc(nav["previous_text"])))
        elif nav.get("first_previous_is_front_page", True):
            links.append('<a href="%s">%s</a>' % (esc(self.front["href"]),
                                                   esc(nav["previous_text"])))
        if k + 1 < len(self.pages):
            links.append('<a href="%s">%s</a>' % (esc(self.pages[k + 1]["href"]),
                                                   esc(nav["next_text"])))
        for text, href in nav.get("fixed_links", []):
            links.append('<a href="%s">%s</a>' % (esc(href), esc(text)))
        out.append('<nav id="toc"><div class="%s">%s</div>' % (
            esc(nav.get("header_class", "header")), nav.get("separator", " | ").join(links)))
        if p["toc"]:
            cls = "toc appendix-toc" if p["appendix"] else "toc"
            out.append('<h2 id="%s" class="contents">%s</h2>' % (
                esc(nav.get("contents_id", "Contents")), esc(nav.get("contents_text", "Contents"))))
            out.append('<ol class="%s"><li>%s</li></ol>' % (cls, self.toc_list(p["toc"], p, cls, 1)))
        out.append("</nav>\n")
        return "".join(out), (h.start, hend.end)

    def promote(self, p):
        """On a chapter page, h3 becomes h2 and so on, as on the live pages."""
        lo, hi = p["slices"][0]
        for x in self.tags:
            if x.start < lo:
                continue
            if x.start >= hi:
                break
            if x.name in HEADINGS and int(x.name[1]) > 2 and x.index != p["heading"]:
                new = "h%d" % (int(x.name[1]) - 1)
                if x.kind == "start":
                    self.edits.tag(x).rename = new
                else:
                    self.edits.replace(x.start, x.end, rename_tag(x.raw, new))

    # -- 2b. Bikeshed's script data ------------------------------------------

    DATA_RE = re.compile(r"(let (dfnPanelData|refsData) = \{\n)(.*?)(\n\};)", re.S)

    def parse_data(self, body):
        data = {}
        for line in body.split("\n"):
            line = line.strip()
            if not line:
                continue
            m = re.match(r'^("(?:[^"\\]|\\.)*"): (\{.*\}),?$', line)
            if not m:
                raise ValueError("unexpected line in Bikeshed data: %r" % line[:120])
            data[json.loads(m.group(1))] = json.loads(m.group(2))
        return data

    def dump_data(self, data):
        return "\n".join("%s: %s," % (json.dumps(k), json.dumps(v, separators=(",", ":")))
                         for k, v in data.items())

    def heading_before(self, off):
        """Original id of the closest heading that starts before offset off."""
        k = bisect.bisect_right(self.heading_offsets, (off, "￿")) - 1
        return self.heading_offsets[k][1] if k >= 0 else None

    def page_scripts(self, p):
        out = []
        for s in self.scripts:
            m = self.DATA_RE.search(s)
            if not m:
                out.append(s)
                continue
            kind = m.group(2)
            data = self.parse_data(m.group(3))
            new = self.panel_data(data, p) if kind == "dfnPanelData" else self.hint_data(data, p)
            s2 = s[:m.start(3)] + self.dump_data(new) + s[m.end(3):]
            if kind == "dfnPanelData":
                old = "mk.a({ href: `#${ref.id}` },"
                if old in s2:
                    s2 = s2.replace(old, "mk.a({ href: ref.url || `#${ref.id}` },")
                else:
                    self.report["dfn panel script not patched (Bikeshed changed?)"].append(p["file"])
            out.append(s2)
        return out

    def panel_data(self, data, p):
        new = {}
        for key, v in data.items():
            tg = self.target(v["dfnID"])
            if tg is None:
                self.report["dfn panel for an id that exists nowhere"].append(v["dfnID"])
                continue
            if tg[0] is not p:
                continue
            v = json.loads(json.dumps(v))
            v["dfnID"] = tg[1]
            key = tg[1] if key == v.get("dfnID") or key in self.alias else key
            if not v.get("external") and v.get("url", "").startswith("#"):
                v["url"] = self.href_for(unquote(v["url"][1:]), p) or v["url"]
            for sec in v.get("refSections", []):
                for r in sec["refs"]:
                    rt = self.target(r["id"])
                    if rt is None:
                        self.report["panel reference to an id that exists nowhere"].append(r["id"])
                        continue
                    if rt[0] is not p:
                        r["url"] = self.href_for(r["id"], p)
                    elif rt[1] != r["id"]:
                        r["url"] = "#" + rt[1]
                if sec["refs"]:
                    first = self.id_tag.get(sec["refs"][0]["id"])
                    hid = self.heading_before(first.start) if first else None
                    ht = self.renumbered.get(hid)
                    if ht:
                        sec["title"] = ht
            new[key] = v
        return new

    def hint_data(self, data, p):
        used = self.used_hrefs[p["name"]]
        hmap = self.href_map[p["name"]]
        new = {}
        for key, v in data.items():
            # key is "<url>" or "<refhint-key>_<url>"
            url = v.get("url", "")
            prefix = key[: len(key) - len(url)] if url and key.endswith(url) else ""
            new_url = hmap.get(url, url)
            if url.startswith("#") and new_url == url:
                h = self.href_for(unquote(url[1:]), p, raw=url)
                new_url = h or url
            new_key = prefix + new_url
            if new_key not in used and key not in used:
                continue
            v = json.loads(json.dumps(v))
            v["url"] = new_url
            new[new_key] = v
        return new

    def collect_used_hrefs(self):
        self.used_hrefs = defaultdict(set)
        for x in self.tags:
            if x.kind != "start" or x.name != "a" or "href" not in x.attrs:
                continue
            p = self.page_of_offset(x.start)
            if p is None:
                continue
            href = self.href_map[p["name"]].get(x.attrs["href"], x.attrs["href"])
            self.used_hrefs[p["name"]].add(href)
            if "data-refhint-key" in x.attrs:
                self.used_hrefs[p["name"]].add(x.attrs["data-refhint-key"] + "_" + href)

    # -- page assembly ----------------------------------------------------------

    def head_html(self, p):
        head = self.text[self.head_open.end:self.head_end]
        fp = self.cfg["front_page"]
        if p["front"]:
            title = fp["title"]
        else:
            title = p["cfg"]["title"] + self.cfg.get("title_suffix", "")
        head = re.sub(r"<title>.*?</title>", lambda m: "<title>%s</title>" % esc(title),
                      head, count=1, flags=re.S)
        if not (p["front"] and fp.get("keep_canonical_link", True)):
            head = re.sub(r'[ \t]*<link[^>]*rel="?canonical"?[^>]*>\n?', "", head)
        extra = list(fp.get("head_extra", [])) if p["front"] else []
        extra += self.cfg.get("head_extra", [])
        return head + "".join("  %s\n" % e for e in extra)

    def body_tag(self, p):
        cls = self.cfg["front_page"]["body_class"] if p["front"] else p["cfg"].get("body_class")
        raw = self.body_open.raw
        return set_attr(raw, "class", cls) if cls else raw

    def build(self):
        self.locate()
        self.collect_ids()
        self.restore_ids()
        self.rewrite_links()
        self.collect_used_hrefs()
        self.heading_offsets = sorted((t.start, i) for i, t in self.id_tag.items()
                                      if t.name in HEADINGS)
        self.number_headings()
        self.renumbered = {}
        for p in self.pages:
            if p["appendix"]:
                for e in p["toc"]:
                    self.renumbered[e["id"]] = "%s %s" % (e["number"], strip_tags(e["content"]).strip())
        if self.cfg.get("promote_headings"):
            for p in self.pages:
                self.promote(p)
        for ident in self.cfg.get("drop_headings", []):
            x = self.id_tag.get(ident)
            if x is None or x.name not in HEADINGS:
                self.report["drop_headings: no heading with this id"].append(ident)
                continue
            e = self.tags[matching_end(self.tags, x.index)]
            self.edits.block(x.start, e.end, '<span id="%s"></span>' % esc(ident))
        headers = []
        for k, p in enumerate(self.pages):
            hdr, rng = self.header_html(k)
            self.edits.block(rng[0], rng[1], hdr)
            headers.append(hdr)

        files = {}
        html_open = self.html_tag.raw
        doctype = "<!doctype html>\n"
        for p in self.all_pages:
            body = []
            for n, (lo, hi) in enumerate(p["slices"]):
                if p["front"] and n == self.front_toc_pos:
                    body.append(self.full_toc())
                body.append(self.edits.apply(self.text, lo, hi))
            if p["front"]:
                content = "".join(body)
            else:
                h = "".join(body)
                # the header (h1, nav) stays outside <main>, as pagesplit's
                # template does
                cut = h.find("</nav>\n") + len("</nav>\n")
                content = h[:cut] + "<main>\n" + h[cut:] + "\n</main>\n"
            end_extra = "".join("%s\n" % e for e in self.cfg.get("body_end_extra", []))
            scripts = "\n".join(self.page_scripts(p))
            files[p["file"]] = "".join([
                doctype, html_open, "\n<head>", self.head_html(p), "</head>\n",
                self.body_tag(p), "\n", content, end_extra, scripts, "\n</body>\n</html>\n"])
        return files

    def fragment_links(self, files):
        ids = {}
        for fn, text in files.items():
            for x in scan(text):
                if x.kind == "start" and "id" in x.attrs:
                    ids.setdefault(x.attrs["id"], fn)
        aliases = {}
        for i, (p, short) in sorted(self.alias.items()):
            aliases[i] = "%s#%s" % (p["file"], short)
        return {"ids": dict(sorted(ids.items())), "single_page_aliases": aliases}


def verify(files):
    """Every local link in the output must land on an id of the page it names."""
    ids = {}
    problems = defaultdict(list)
    parsed = {}
    for fn, text in files.items():
        tags = scan(text)
        parsed[fn] = tags
        seen = set()
        for x in tags:
            if x.kind == "start" and "id" in x.attrs:
                i = x.attrs["id"]
                if i in seen:
                    problems["duplicate id on a page"].append("%s#%s" % (fn, i))
                seen.add(i)
        ids[fn] = seen
    names = set(files)
    for fn, tags in parsed.items():
        for x in tags:
            if x.kind != "start" or x.name not in ("a", "area") or "href" not in x.attrs:
                continue
            href = x.attrs["href"]
            if re.match(r"^[a-z][a-z0-9+.-]*:", href, re.I) or href.startswith("//"):
                continue
            page, _, frag = href.partition("#")
            if page in ("", ):
                page = fn
            elif page == "./":
                page = "index.html"
            if page not in names:
                continue
            frag = unquote(frag)
            if frag and frag not in ids[page]:
                problems["link to a missing fragment"].append("%s: %s" % (fn, href))
    # the data behind "Referenced in" panels and link hints
    data_re = re.compile(r"let (dfnPanelData|refsData) = \{\n(.*?)\n\};", re.S)
    for fn, text in files.items():
        for m in data_re.finditer(text):
            for line in m.group(2).split("\n"):
                lm = re.match(r'^("(?:[^"\\]|\\.)*"): (\{.*\}),?$', line.strip())
                if not lm:
                    continue
                key, v = json.loads(lm.group(1)), json.loads(lm.group(2))
                if m.group(1) == "dfnPanelData":
                    if v["dfnID"] not in ids[fn]:
                        problems["panel for a dfn not on its page"].append("%s: %s" % (fn, v["dfnID"]))
                    for sec in v.get("refSections", []):
                        for r in sec["refs"]:
                            href = r.get("url", "#" + r["id"])
                            page, _, frag = href.partition("#")
                            page = fn if page == "" else ("index.html" if page == "./" else page)
                            if unquote(frag) not in ids.get(page, set()):
                                problems["panel reference to a missing fragment"].append(
                                    "%s: %s" % (fn, href))
                else:
                    url = v.get("url", "")
                    if re.match(r"^[a-z][a-z0-9+.-]*:", url, re.I):
                        continue
                    page, _, frag = url.partition("#")
                    page = fn if page == "" else ("index.html" if page == "./" else page)
                    if page in ids and unquote(frag) not in ids[page]:
                        problems["link hint to a missing fragment"].append("%s: %s" % (fn, url))
    return problems


def copy_resources(cfg, src, out, link):
    done, missing = [], []
    for name in cfg.get("resources", []):
        s = os.path.join(src, name)
        d = os.path.join(out, name)
        if not os.path.exists(s):
            missing.append(name)
            continue
        if os.path.lexists(d):
            if os.path.isdir(d) and not os.path.islink(d):
                shutil.rmtree(d)
            else:
                os.remove(d)
        if link:
            os.symlink(os.path.abspath(s), d)
        elif os.path.isdir(s):
            shutil.copytree(s, d)
        else:
            shutil.copy2(s, d)
        done.append(name)
    return done, missing


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--single", required=True, help="single-page Bikeshed output")
    ap.add_argument("--out", required=True, help="directory for the chapter pages")
    ap.add_argument("--config", required=True, help="JSON file with the spec-specific data")
    ap.add_argument("--resources", help="directory holding style/, images/ and stub pages "
                    "(for SVG 2: master/ of the svgwg checkout)")
    ap.add_argument("--link-resources", action="store_true",
                    help="make symbolic links to the resources instead of copying them")
    args = ap.parse_args()
    with open(args.config, encoding="utf-8") as f:
        cfg = json.load(f)
    sp = Splitter(args.single, cfg)
    files = sp.build()
    os.makedirs(args.out, exist_ok=True)
    for fn, text in files.items():
        with open(os.path.join(args.out, fn), "w", encoding="utf-8") as f:
            f.write(text)
    res_done, res_missing = ([], [])
    if args.resources:
        res_done, res_missing = copy_resources(cfg, args.resources, args.out, args.link_resources)
    else:
        sp.report["resources not copied (no --resources)"].append("")
    with open(os.path.join(args.out, "fragment-links.json"), "w", encoding="utf-8") as f:
        json.dump(sp.fragment_links(files), f, indent=1, ensure_ascii=False)
        f.write("\n")
    problems = verify(files)
    report = {
        "pages": list(files),
        "links_rewritten_per_page": dict(sp.link_changes),
        "ids_restored": [{"page": a, "id": b, "how": c, "single_page_id": d}
                         for a, b, c, d in sp.restored],
        "resources_copied": res_done,
        "resources_missing": res_missing,
        "notes": {k: v for k, v in sp.report.items()},
        "problems_after_split": {k: v for k, v in problems.items()},
    }
    with open(os.path.join(args.out, "split-report.json"), "w", encoding="utf-8") as f:
        json.dump(report, f, indent=1, ensure_ascii=False)
        f.write("\n")
    print("wrote %d pages to %s" % (len(files), args.out))
    print("links rewritten: %d; ids restored: %d" % (sum(sp.link_changes.values()),
                                                    len(sp.restored)))
    for k, v in list(sp.report.items()) + list(problems.items()):
        print("%s: %d" % (k, len(v)))
        for item in v[:10]:
            print("   ", item)
    if res_missing:
        print("resources missing in --resources:", ", ".join(res_missing))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
