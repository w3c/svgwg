# Tools

What is in this folder, who runs each piece, and when. Two build systems live here side by side:

- **The Bikeshed build** (`svg2-build/`) builds SVG 2 from `master/*.bs`. SVG 2 moved to it in October 2026 ([w3c/svgwg#1036](https://github.com/w3c/svgwg/issues/1036)).
- **The old HTML build** (`build.py`, `spec.mk`, `publish/`, `stabilizer.pl`) builds the modules under `specs/` that are still written in the old format (`master/*.html` with `edit:*` elements and a `publish.xml`). It needs Node.js. When the last of those modules has moved to Bikeshed, these four go.

## Files

| Path | What it is | Run by |
|---|---|---|
| `svg2-build/` | The SVG 2 build. Details in [svg2-build/README.md](svg2-build/README.md) and the table below. | `make`, `make check`, `make test` at the root; CI |
| `build.py` | Old HTML build of one module: runs `publish/publish.js` on each page listed in the module's `master/publish.xml`, copies the resources, writes `build/publish/`. Options: `-c` clean, `-s` number issues, `-l` lint, `-L` list external links. | `make` in `specs/animations`, `integration`, `markers`, `paths`, `strokes` (and `template`), through `spec.mk`; `make all-specs` at the root; CI |
| `spec.mk` | The Makefile rules those modules include (`include ../../tools/spec.mk`): `all`, `clean`, `stabilize-issues`, `lint`, `list-external-links`, each calling `build.py`. | the module Makefiles |
| `publish/` | The old publishing tool, in JavaScript: reads a page and `publish.xml`, expands the `edit:*` elements from the definitions files, writes the page with its header, table of contents and links. `node_modules/xmldom` is a bundled copy of the XML library it needs, so no `npm install` is required. | `build.py` |
| `stabilizer.pl` | Gives each issue box of an old-format page a permanent number (`data-issue="7"`, published as `id="issue7"`), so links to an issue keep working when others are added or removed. Keeps the next free number per page in `issue-state.txt` (not committed). | `build.py -s`: `make stabilize-issues` in a module, `make stabilize-issues-all-specs` at the root |
| `deploy.sh` | Puts the built specs into `deploy/` in the shape of https://w3c.github.io/svgwg/: SVG 2 from `build/bikeshed/svg2-draft/`, the modules from their `build/publish/` (renaming `Overview.html` to `index.html`), and the hand-built ones as they are. | CI, after `make all-specs`; pushed to the `gh-pages` branch on `main` |

### `svg2-build/`

| Path | What it is | Run by |
|---|---|---|
| `build.sh` | The SVG 2 build: checks the Bikeshed version (7.2.0 or later), then runs the four steps below. | `make` |
| `generate.py` | Step 1: fills in the element summaries, category lists, attribute table and indexes from `master/definitions*.xml`, and copies the chapters into one `index.bs`. | `build.sh` |
| `buildlog.py` | Step 2, after Bikeshed: groups Bikeshed's messages by kind and prints a short table. | `build.sh` |
| `singlepage.py` | Step 3: makes `single-page.html`, with each chapter's navigation bar and table of contents. | `build.sh` |
| `split.py` | Step 4: cuts Bikeshed's single page into the chapter pages, rewriting links between pages and putting back the ids that one page cannot hold twice. | `build.sh` |
| `check.sh`, `check-preservation.py` | Fails when an id SVG 2 has published is missing from the build. `check-preservation.py` can also compare every link of two builds; that was used for the conversion. | `make check`; CI |
| `baseline/` | The published ids that `check.sh` looks for: those of the last build from the old source. | `check.sh` |
| `config/svg2.json` | Where the source is, which definitions files to read, and how generated links are written. | `generate.py` |
| `config/svg2-split.json` | Page order, file names, titles, navigation. | `generate.py`, `split.py` |
| `convert.py` | The converter from the old HTML format to Bikeshed. It made `master/*.bs` once. It stays because `generate.py` uses its code to write the generated content, and because the modules above are to be converted with it. | `generate.py` (as a library); by hand, to convert a module |
| `svgdefs.py` | Reads the definitions files and resolves names to links the way the old build did. | `convert.py`, `generate.py` |
| `measure.py` | Not part of any build. Compares a conversion with the old build in detail: the text of every block, and where each link lands (`convert.py --trace-links`). Kept for converting the modules. | by hand |
| `tests/` | Unit tests of all the Python scripts, with small inputs in `tests/fixtures/`. | `make test`; CI |

## How each spec is built

| Spec | Source | Built by | Published (`deploy.sh`) |
|---|---|---|---|
| SVG 2 | `master/*.bs` | `svg2-build/build.sh` | yes, `svg2-draft/` |
| animations, integration, markers, paths, strokes | `specs/<name>/master/` (old format) | `build.py` | yes |
| template | `specs/template/master/` (old format) | `build.py`, skipped by `make all-specs` | no; starting point for a new module |
| svg-native | `specs/svg-native/index.bs` | its own Makefile: local Bikeshed, or the W3C spec generator on CI | yes |
| transform | `specs/transform/Overview.bs`, built `Overview.html` committed | by hand | yes (the committed `Overview.html`) |
| streaming | `specs/streaming/index.html`, plain HTML | nothing to build | yes |
| color, marker | `Overview.bs`, built `Overview.html` committed | by hand | no |
| animation-elements | ReSpec | in the browser | no |
| svg-authoring | plain HTML | nothing to build | no |

## Make targets at the root

| Target | What it does |
|---|---|
| `make` | builds SVG 2 into `build/bikeshed/svg2-draft/` |
| `make check` | builds SVG 2, then fails if a published id is missing |
| `make test` | unit tests of `svg2-build/` |
| `make all-specs` | SVG 2, then every module with a Makefile (except `template`); what CI runs |
| `make clean` | removes `build/bikeshed/` |
| `make pdf` | prints the single page to PDF with [Prince](https://www.princexml.com/), which is not installed on CI |
| `make stabilize-issues-all-specs` | numbers the new issue boxes of every old-format module (`stabilizer.pl`) |
