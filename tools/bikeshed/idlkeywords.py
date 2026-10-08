#!/usr/bin/env python3
"""Link IDL keywords that Bikeshed leaves as plain text.

    python3 idlkeywords.py OUT_DIR [--config CONFIG]

Edits OUT_DIR/index.html in place. Runs after Bikeshed and before
singlepage.py and the splitter, so both versions get the links.

Why: an unnamed special operation such as
    setter undefined (unsigned long index, SVGNumber newItem);
has no name to link, and Bikeshed writes the keyword as plain coloured
text (<c- b>setter</c->). Today's SVG 2 links that keyword to the prose
that defines it (types.html#__svg__SVGNameList__setter). This puts the
link back, for every keyword listed in the config (idl_keyword_links:
keyword -> target id), inside IDL blocks only, and only where the keyword
is not already inside a link.

To be removed once Bikeshed links these keywords itself
(https://github.com/speced/bikeshed/issues/670).

Standard library only. Python 3.9 or later.
"""

import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
IDL_BLOCK_RE = re.compile(r'(<pre\b[^>]*\bclass="[^"]*\bidl\b[^"]*"[^>]*>)(.*?)(</pre>)', re.S)


def link_keywords(block, links):
    """Wrap <c- b>KEYWORD</c-> in a link, unless it already sits in an <a>."""
    count = 0
    out, pos = [], 0
    for m in re.finditer(r'<c- b>(%s)</c->' % "|".join(map(re.escape, links)), block):
        before = block[:m.start()]
        if before.rfind("<a ") > before.rfind("</a>"):
            continue  # already inside a link
        out.append(block[pos:m.start()])
        out.append('<a href="#%s">%s</a>' % (links[m.group(1)], m.group(0)))
        pos = m.end()
        count += 1
    out.append(block[pos:])
    return "".join(out), count


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("out", nargs="?", default=".")
    ap.add_argument("--config", default=os.path.join(HERE, "config", "svg2.json"))
    args = ap.parse_args(argv[1:])
    with open(args.config, encoding="utf-8") as f:
        links = json.load(f).get("idl_keyword_links", {})
    path = os.path.join(args.out, "index.html")
    if not links:
        print("idlkeywords: no idl_keyword_links in config, nothing to do")
        return 0
    with open(path, encoding="utf-8") as f:
        doc = f.read()
    missing = [t for t in links.values() if not re.search(r'(?<![\w-])id="%s"' % re.escape(t), doc)]
    if missing:
        print("idlkeywords: target id not in index.html: %s" % ", ".join(missing), file=sys.stderr)
        return 1
    total = 0

    def fix(m):
        nonlocal total
        body, n = link_keywords(m.group(2), links)
        total += n
        return m.group(1) + body + m.group(3)

    doc = IDL_BLOCK_RE.sub(fix, doc)
    with open(path, "w", encoding="utf-8") as f:
        f.write(doc)
    print("idlkeywords: %d IDL keywords linked (%s)" % (total, ", ".join(sorted(links))))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
