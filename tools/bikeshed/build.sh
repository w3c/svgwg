#!/bin/sh
# Build the Bikeshed version of the SVG 2 editor's draft from master/.
#
#   tools/bikeshed/build.sh [OUT_DIR]        (default: build/bikeshed)
#
# Writes OUT_DIR/work (the .bs files, Bikeshed's index.html, build.log) and
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

rm -rf "$WORK" "$SITE"

echo "1/5 convert master/ to Bikeshed source"
python3 "$HERE/convert.py" --source "$ROOT" --config "$HERE/config/svg2.json" --out "$WORK"

echo "2/5 run Bikeshed"
cd "$WORK"
if ! "$BIKESHED" --no-update spec index.bs index.html > build.log 2>&1 || [ ! -s index.html ]; then
  cat build.log
  echo "Bikeshed failed, see above" >&2
  exit 1
fi
python3 "$HERE/buildlog.py" build.log

echo "3/5 link the IDL keywords Bikeshed leaves plain"
python3 "$HERE/idlkeywords.py" "$WORK" --config "$HERE/config/svg2.json"

echo "4/5 make single-page.html"
python3 "$HERE/singlepage.py" "$WORK"

echo "5/5 cut into chapter pages"
python3 "$HERE/split.py" --single "$WORK/index.html" --out "$SITE" \
  --config "$HERE/config/svg2-split.json" --resources "$ROOT/master"
cp "$WORK/single-page.html" "$SITE/single-page.html"

echo "done: $SITE"
