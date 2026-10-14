#!/bin/sh
# Check that the build still has every id SVG 2 has published, on the
# chapter pages and on the single page.
#
#   tools/svg2-build/check.sh [NEW_DIR]
#
# NEW_DIR: output of build.sh (default build/bikeshed/svg2-draft).
# The ids are listed in tools/svg2-build/baseline/, taken from the last build
# of the old HTML source (2026-10-14). Removing an id on purpose means
# removing its row there too, in the same change.
# Exit status 1 when an id or a page is missing. See README.md in this folder.
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
ROOT=$(cd "$HERE/../.." && pwd)
NEW=${1:-"$ROOT/build/bikeshed/svg2-draft"}

if [ ! -f "$NEW/single-page.html" ]; then
  echo "no build in $NEW: run make first" >&2
  exit 2
fi

python3 "$HERE/check-preservation.py" check --ids-only --baseline "$HERE/baseline" \
  --multipage "$NEW" --single "$NEW/single-page.html" \
  --losses-tsv "$ROOT/build/bikeshed/losses.tsv"
