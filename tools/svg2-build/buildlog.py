#!/usr/bin/env python3
"""Group a Bikeshed build log into categories, per source file.

    python3 buildlog.py out/build.log [--json out/build-log.json]

Bikeshed prints one message per problem, with colour codes and the line in
the included file. This strips the colours, keeps the file name, and folds
each message into a category (the message with names and numbers taken out),
so two builds can be compared by category rather than by raw line count.

Standard library only.
"""

import argparse
import json
import re
import sys

ANSI = re.compile(r"\x1b\[[0-9;]*m")
LOC = re.compile(r"^LINE ~?([0-9:]+)(?: of file '([^']+)'(?: \(included by a block on [0-9:]+\))?)?:\s*")

# Message shape -> category name. First match wins.
CATEGORIES = [
    (r"^No '([\w-]+)' refs found for", r"link error: no \1 dfn found"),
    (r"^Multiple possible '([\w-]+)' (local )?refs", r"link error: several \1 dfns match"),
    (r"^Multiple local '([\w-]+)' <dfn>s have the same", r"duplicate dfn: \1"),
    (r"definitions need to specify what they're for", "dfn without for"),
    (r"^Couldn't find target", "dfn without for (detail)"),
    (r"is only used once", "lint: var used only once"),
    (r"Line starts with tabs|Line starts with spaces", "lint: mixed indentation"),
    (r"^Unexported dfn", "lint: unexported dfn not used locally"),
    (r"^Multiple elements have the same ID", "duplicate id"),
    (r"^Found unmatched text macro", "text macro"),
    (r"isn't indented enough", "indentation"),
    (r"Security Considerations", "boilerplate: no security/privacy section"),
    (r"^IDL", "idl"),
    (r"WebIDL|widl|IDL", "idl"),
    (r"^Include-code", "include"),
    (r"^Couldn't find include", "include"),
    (r"still open|unclosed|Unclosed", "markup not closed"),
    (r"^Image doesn't exist|^Couldn't find image", "image"),
]


def categorise(msg):
    for rx, name in CATEGORIES:
        m = re.search(rx, msg)
        if m:
            return m.expand(name) if "\\" in name else name
    return "other: " + re.sub(r"'[^']*'", "'…'", msg)[:80]


def page_map(index_path):
    """Line ranges of index.bs that came from each page file (convert.py
    writes a '<!-- page: NAME.bs -->' line before each inlined page)."""
    starts = []
    try:
        with open(index_path, encoding="utf-8") as f:
            for i, l in enumerate(f, 1):
                m = re.match(r"<!-- page: (\S+) -->", l)
                if m:
                    starts.append((i, m.group(1)))
    except IOError:
        pass
    return starts


def parse(path, index_path=None):
    starts = page_map(index_path) if index_path else []
    rows = []
    with open(path, encoding="utf-8", errors="replace") as f:
        lines = [ANSI.sub("", l.rstrip("\n")) for l in f]
    for l in lines:
        if not l.strip() or l[0].isspace() or l[0] in '<"'  or "Successfully generated" in l:
            continue
        if l.startswith("Add a 'for' attribute") or l.startswith("If this is not a typo") or l.startswith("(Possible"):
            continue
        fname = "-"
        line = ""
        m = LOC.match(l)
        if m:
            line, fname = m.group(1), m.group(2) or "index.bs"
            l = l[m.end():]
            if fname == "index.bs" and starts:
                n = int(line.split(":")[0])
                for st, pg in starts:
                    if st <= n:
                        fname = pg
                        line = "%d" % (n - st)
        l = re.sub(r"^(WARNING|LINK ERROR|FATAL ERROR|LINT):\s*", "", l)
        rows.append(dict(file=fname, line=line, message=l, category=categorise(l)))
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("log")
    ap.add_argument("--json")
    ap.add_argument("--index", help="index.bs, to map line numbers back to page files (default: next to the log)")
    a = ap.parse_args()
    import os
    rows = parse(a.log, a.index or os.path.join(os.path.dirname(os.path.abspath(a.log)), "index.bs"))
    by_cat = {}
    for r in rows:
        by_cat.setdefault(r["category"], {}).setdefault(r["file"], 0)
        by_cat[r["category"]][r["file"]] += 1
    files = sorted(set(r["file"] for r in rows))
    print("%-55s %6s  %s" % ("category", "total", "  ".join(files)))
    for cat in sorted(by_cat, key=lambda c: -sum(by_cat[c].values())):
        tot = sum(by_cat[cat].values())
        print("%-55s %6d  %s" % (cat[:55], tot, "  ".join("%s=%d" % (f, by_cat[cat][f]) for f in files if f in by_cat[cat])))
    print("%-55s %6d" % ("TOTAL", len(rows)))
    if a.json:
        with open(a.json, "w", encoding="utf-8") as f:
            json.dump(rows, f, indent=1)


if __name__ == "__main__":
    sys.exit(main())
