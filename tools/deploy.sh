# Script that creates the right folder structure for deployment to GitHub Pages.
#
# The script must run *after* running `make`. Built versions of specs must be
# available in particular. The script fills a `deploy` folder with them, that
# can typically be pushed to the `gh-pages` branch for publication.
#
# The build script creates `Overview.html` files, which aren't served by default
# in GitHub Pages. The script renames these files to `index.html` in the
# `deploy` folder so that they can be served by default. For this to work
# properly, there must be no explicit reference to `Overview.html` in the
# specifications.
#
# Note: the script assumes it gets run from the root folder of the repository.

# Reset `deploy` folder
rm -rf deploy
mkdir deploy
mkdir deploy/specs
mkdir deploy/specs/svg-native
mkdir deploy/specs/transform

# Copy built files to `deploy` folder
cp -r build/publish deploy/svg2-draft/
cp -r specs/animations/build/publish deploy/specs/animations
cp -r specs/integration/build/publish deploy/specs/integration
cp -r specs/streaming deploy/specs/streaming
cp -r specs/markers/build/publish deploy/specs/markers
cp -r specs/paths/build/publish deploy/specs/paths
cp -r specs/strokes/build/publish deploy/specs/strokes
cp specs/svg-native/index.html deploy/specs/svg-native/index.html
cp specs/transform/Overview.html deploy/specs/transform/index.html
cp index.html deploy

# Rename `Overview.html` files
mv deploy/svg2-draft/Overview.html deploy/svg2-draft/index.html
mv deploy/specs/animations/Overview.html deploy/specs/animations/index.html
mv deploy/specs/integration/Overview.html deploy/specs/integration/index.html
mv deploy/specs/markers/Overview.html deploy/specs/markers/index.html
mv deploy/specs/paths/Overview.html deploy/specs/paths/index.html
mv deploy/specs/strokes/Overview.html deploy/specs/strokes/index.html
