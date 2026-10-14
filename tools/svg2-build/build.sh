#!/bin/sh
# Build the SVG 2 editor's draft from its Bikeshed source in master/.
#
#   tools/svg2-build/build.sh [OUT_DIR]        (default: build/bikeshed)
#
# $SVG_SOURCE names another folder of .bs files (default: master/).
#
# Writes OUT_DIR/work (index.bs with the generated content filled in,
# Bikeshed's index.html, build.log) and
# OUT_DIR/svg2-draft (the chapter pages, single-page.html, style/, images/),
# which is what gets published.
#
# Needs python3 (3.9+ for these scripts) and Bikeshed (which needs 3.12+):
# $BIKESHED if set, else bikeshed on PATH.
# See README.md in this folder.
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
ROOT=$(cd "$HERE/../.." && pwd)
OUT=${1:-"$ROOT/build/bikeshed"}
mkdir -p "$OUT"
OUT=$(cd "$OUT" && pwd)
WORK="$OUT/work"
SITE="$OUT/svg2-draft"
BIKESHED=${BIKESHED:-bikeshed}
SRC=${SVG_SOURCE:-"$ROOT/master"}

# 7.2.0 links the setter keyword of the list interfaces to its definition
# (speced/bikeshed#3326); older releases leave it as plain text.
MIN_BIKESHED=7.2.0
if ! VERSION=$("$BIKESHED" --version 2>/dev/null | tail -n 1) || [ -z "$VERSION" ]; then
  echo "Bikeshed not found ($BIKESHED). Install it: pip install 'bikeshed>=$MIN_BIKESHED'" >&2
  exit 1
fi
if ! python3 -c '
import re, sys
num = lambda s: tuple(int(x) for x in re.findall(r"\d+", s)[:3])
sys.exit(num(sys.argv[1]) < num(sys.argv[2]))' "$VERSION" "$MIN_BIKESHED"; then
  echo "Bikeshed $VERSION is too old, $MIN_BIKESHED or later is needed: pip install --upgrade bikeshed (or pipx upgrade bikeshed)" >&2
  exit 1
fi

rm -rf "$WORK" "$SITE"

echo "1/4 fill in the content generated from definitions.xml"
python3 "$HERE/generate.py" --root "$ROOT" --src "$SRC" --out "$WORK"

echo "2/4 run Bikeshed"
cd "$WORK"
if ! "$BIKESHED" --no-update spec index.bs index.html > build.log 2>&1 || [ ! -s index.html ]; then
  cat build.log
  echo "Bikeshed failed, see above" >&2
  exit 1
fi
python3 "$HERE/buildlog.py" build.log

echo "3/4 make single-page.html"
python3 "$HERE/singlepage.py" "$WORK"

echo "4/4 cut into chapter pages"
python3 "$HERE/split.py" --single "$WORK/index.html" --out "$SITE" \
  --config "$HERE/config/svg2-split.json" --resources "$ROOT/master"
cp "$WORK/single-page.html" "$SITE/single-page.html"
# the splitter's report is for us, not for the published folder
mv "$SITE/split-report.json" "$WORK/split-report.json"

echo "done: $SITE"
