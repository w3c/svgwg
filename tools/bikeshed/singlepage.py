#!/usr/bin/env python3
"""Make single-page.html from Bikeshed's index.html.

    python3 singlepage.py OUT_DIR

reads OUT_DIR/index.html and OUT_DIR/single-page-nav.json (written by
convert.py) and writes OUT_DIR/single-page.html. index.html is not changed:
it stays the input of the page splitter.

What it adds is what today's single-page.html has and Bikeshed does not
make: at the top of every chapter, the chapter's own navigation bar
(Overview, Previous, Next, Elements, Attributes, Properties) and its own
table of contents, with today's ids (<page>-toc on the bar, <page>-Contents
on the "Contents" heading); and the appendix section numbers ("K.1.").
It also removes the headings Bikeshed writes that today's page does not
have (config single_page_drop_headings: the "IDL Index" heading), keeping
their ids on an empty span.
The text of each entry is copied from the heading Bikeshed wrote, so the
numbers are Bikeshed's (or, in appendices, the ones added here).

The splitter does the same for each chapter page of the multipage version;
here every id carries the page prefix, as on today's single page, and
data-multipage-id says which short id the chapter page uses.

Standard library only. Python 3.9 or later.
"""

import json
import os
import re
import sys

CHAPTER_RE = re.compile(r'<h2\b[^>]*\bdata-bs-page="([^"]+)"[^>]*>.*?</h2>', re.S)
HEADING_RE = re.compile(r'<h([2-6])\b([^>]*)>(.*?)</h\1>', re.S)


def attr(attrs, name):
    m = re.search(r'(?<![\w-])%s="([^"]*)"' % name, attrs)
    return m.group(1) if m else None


def entry_html(inner):
    """secno and content of a Bikeshed heading, made safe for a link: no ids,
    no nested links, no self-link, no alias spans."""
    secno = ""
    m = re.search(r'<span class="secno">(.*?)</span>', inner, re.S)
    if m:
        secno = m.group(1).strip()
        if secno and not secno.endswith("."):
            secno += "."
    m = re.search(r'<span class="content">(.*)</span>', inner, re.S)
    content = m.group(1) if m else inner
    content = re.sub(r'<a class="self-link"[^>]*></a>', "", content)
    content = re.sub(r'<span class="bs-old-id"[^>]*></span>', "", content)
    content = re.sub(r'<a\b[^>]*>|</a>', "", content)
    content = re.sub(r'<dfn\b[^>]*>', "<span>", content).replace("</dfn>", "</span>")
    content = re.sub(r'\s+(?<![\w-])id="[^"]*"', "", content)
    content = re.sub(r'\s+', " ", content).strip()
    return ('<span class="secno">%s</span> %s' % (secno, content)) if secno else content


def chapter_toc(body, chapter_level=2):
    """Nested <ol class="toc"> for the headings of one chapter, as today."""
    items = []
    for m in HEADING_RE.finditer(body):
        level, attrs, inner = int(m.group(1)), m.group(2), m.group(3)
        hid = attr(attrs, "id")
        cls = (attr(attrs, "class") or "").split()
        if level <= chapter_level or not hid or "no-toc" in cls:
            continue
        items.append((level, hid, entry_html(inner)))
    if not items:
        return ""
    out = ['<ol class="toc"><li><ol class="toc">']
    stack = [chapter_level + 1]
    first = True
    for level, hid, text in items:
        while level > stack[-1]:
            out.append('<ol class="toc">')
            stack.append(stack[-1] + 1)
            first = True
        while level < stack[-1]:
            out.append("</li></ol>")
            stack.pop()
        if not first:
            out.append("</li>")
        out.append('<li><a href="#%s">%s</a>' % (hid, text))
        first = False
    while len(stack) > 1:
        out.append("</li></ol>")
        stack.pop()
    out.append("</li></ol></li></ol>")
    return "".join(out)


def number_appendix(body, letter, numbers, chapter_level=2):
    """Bikeshed does not number the sections of an appendix; today's pages
    say "K.1.", "K.2.3.". Adds that number to each heading that would be in
    the table of contents (the splitter does the same on the chapter pages)."""
    counters = []

    def rep(m):
        level, attrs, inner = int(m.group(1)), m.group(2), m.group(3)
        cls = (attr(attrs, "class") or "").split()
        if level <= chapter_level or not attr(attrs, "id") or "no-toc" in cls or 'class="secno"' in inner:
            return m.group(0)
        rel = level - chapter_level
        del counters[rel:]
        while len(counters) < rel:
            counters.append(0)
        counters[rel - 1] += 1
        number = "%s.%s." % (letter, ".".join(str(c) for c in counters))
        numbers[attr(attrs, "id")] = number
        return '<h%d%s><span class="secno">%s </span>%s</h%d>' % (level, attrs, number, inner, level)

    return HEADING_RE.sub(rep, body)


def nav_html(nav, name, toc_html):
    pages = nav["pages"]
    i = pages.index(name)
    links = []
    if nav.get("toc"):
        links.append('<a href="./">Overview</a>')
    if i > 0:
        links.append('<a href="#chapter-%s">Previous</a>' % pages[i - 1])
    elif nav.get("index"):
        links.append('<a href="./">Previous</a>')
    if i + 1 < len(pages):
        links.append('<a href="#chapter-%s">Next</a>' % pages[i + 1])
    for key, label in (("elements", "Elements"), ("attributes", "Attributes"),
                       ("properties", "Properties")):
        if nav.get(key):
            links.append('<a href="#chapter-%s">%s</a>' % (nav[key], label))
    contents = ""
    if toc_html:
        contents = ('<h3 id="%s-Contents" class="contents no-num no-toc" data-multipage-id="Contents">'
                    'Contents</h3>%s' % (name, toc_html))
    return ('<nav id="%s-toc" class="chapter-toc" data-multipage-id="toc">'
            '<div class="header">%s</div>%s</nav>' % (name, " · ".join(links), contents))


def main(argv):
    out = argv[1] if len(argv) > 1 else "."
    with open(os.path.join(out, "index.html"), encoding="utf-8") as f:
        doc = f.read()
    with open(os.path.join(out, "single-page-nav.json"), encoding="utf-8") as f:
        nav = json.load(f)
    chapters = list(CHAPTER_RE.finditer(doc))
    pieces, last = [], 0
    numbers = {}  # heading id -> appendix section number
    for k, m in enumerate(chapters):
        name = m.group(1)
        end = chapters[k + 1].start() if k + 1 < len(chapters) else doc.find("</main>", m.end())
        if end < 0:
            end = len(doc)
        pieces.append(doc[last:m.end()])
        body = doc[m.end():end]
        letter = nav.get("appendix_letters", {}).get(name)
        if letter:
            body = number_appendix(body, letter, numbers)
        if name in nav["pages"]:
            pieces.append(nav_html(nav, name, chapter_toc(body)))
        pieces.append(body)
        last = end
    pieces.append(doc[last:])
    result = "".join(pieces)
    # headings Bikeshed writes that today's page does not have
    for hid in nav.get("drop_headings", []):
        result, n = re.subn(r'<h([2-6])\b[^>]*(?<![\w-])id="%s"[^>]*>.*?</h\1>' % re.escape(hid),
                            '<span class="bs-old-id" id="%s"></span>' % hid, result, count=1, flags=re.S)
        # Bikeshed leaves out optional end tags: stop at this entry's </a>
        result = re.sub(r'<li><a href="#%s">(?:(?!</a>).)*</a>(?:\s*</li>)?' % re.escape(hid), "", result,
                        count=1, flags=re.S)
    # the same numbers in Bikeshed's full table of contents
    i = result.find('<nav data-fill-with="table-of-contents"')
    j = result.find("</nav>", i)
    if i >= 0 and j > i:
        toc = re.sub(r'(<a href="#([^"]+)">)<span class="secno"></span>',
                     lambda m: (m.group(1) + '<span class="secno">%s</span>' % numbers[m.group(2)])
                     if m.group(2) in numbers else m.group(0), result[i:j])
        result = result[:i] + toc + result[j:]
    with open(os.path.join(out, "single-page.html"), "w", encoding="utf-8") as f:
        f.write(result)
    print("single-page.html: %d chapter navigation bars added" % len(chapters))


if __name__ == "__main__":
    main(sys.argv)
