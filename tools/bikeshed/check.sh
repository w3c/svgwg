#!/bin/sh
# Check that the Bikeshed version keeps every id and every link of the
# current build, on the chapter pages and on the single page.
#
#   tools/bikeshed/check.sh [OLD_DIR] [NEW_DIR]
#
# OLD_DIR: output of the current build (default build/publish, made by `make`).
# NEW_DIR: output of build.sh (default build/bikeshed/svg2-draft).
# Exit status 1 when anything is lost. See README.md in this folder.
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
ROOT=$(cd "$HERE/../.." && pwd)
OLD=${1:-"$ROOT/build/publish"}
NEW=${2:-"$ROOT/build/bikeshed/svg2-draft"}
BASE="$ROOT/build/bikeshed/baseline"

if [ ! -f "$OLD/single-page.html" ]; then
  echo "no current build in $OLD: run make first" >&2
  exit 2
fi
if [ ! -f "$NEW/single-page.html" ]; then
  echo "no Bikeshed build in $NEW: run tools/bikeshed/build.sh first" >&2
  exit 2
fi

python3 "$HERE/check-preservation.py" extract \
  --multipage "$OLD" --single "$OLD/single-page.html" --out "$BASE"
python3 "$HERE/check-preservation.py" check --baseline "$BASE" \
  --multipage "$NEW" --single "$NEW/single-page.html" \
  --losses-tsv "$ROOT/build/bikeshed/losses.tsv"
