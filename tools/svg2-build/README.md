# Building SVG 2 with Bikeshed

The other tools in this repository, and which spec each one builds, are listed in [../README.md](../README.md).

The SVG 2 editor's draft is written in [Bikeshed](https://speced.github.io/bikeshed/). Its source is in `master/`: one `.bs` file per chapter or appendix, `master/index.bs`, which holds the metadata and includes the chapters in order, and `master/header.include`, the front page up to the table of contents.

The Working Group decided to move SVG 2 to Bikeshed on 2026-10-13 ([w3c/svgwg#1036](https://github.com/w3c/svgwg/issues/1036), [minutes](https://www.w3.org/2026/10/13-svg-minutes.html#cadf)). The `.bs` files were made once from the old HTML source (`master/*.html` with `edit:*` elements) by `convert.py`, at commit 8b6274e7 of w3c/svgwg, and the old source was then removed. Every id and every link of the published draft was kept, on the chapter pages and on the single page.

## Requirements

- Python 3.9 or later for these scripts. They use the standard library only.
- [Bikeshed](https://speced.github.io/bikeshed/#installing) 7.2.0 or later (`pip install bikeshed`). Earlier releases do not link the `setter` keyword of the list interfaces to its definition. `build.sh` checks the version and stops with a message when Bikeshed is missing or older. Bikeshed itself needs Python 3.12 or later. The scripts use the `bikeshed` on your PATH, or the one named in `$BIKESHED`.

## Use

From the root of the repository:

```sh
make           # build SVG 2 into build/bikeshed/svg2-draft/
make check     # build, then fail if an id SVG 2 has published is missing
make test      # run the unit tests of these scripts (see Tests below)
```

Or call the scripts directly: `tools/svg2-build/build.sh [OUT_DIR]` and `tools/svg2-build/check.sh [NEW_DIR]`.

`build/bikeshed/` then holds:

- `work/`: `index.bs` with every chapter copied in and the generated content filled in, Bikeshed's own single-page output `index.html`, `build.log` with Bikeshed's messages, and `split-report.json`;
- `svg2-draft/`: what gets published, that is the 28 chapter pages, `single-page.html`, `style/`, `images/`, the stub pages of removed chapters, and `fragment-links.json` (which page holds each id);
- `losses.tsv`, after a check.

## Writing the source

The chapters are ordinary Bikeshed, with a few things specific to SVG 2.

### Links

Links to definitions in SVG 2 are written as Bikeshed shorthands:

| What | Write | Example |
|---|---|---|
| property | `'name'` | `'fill'` |
| element | `<{name}>` | `<{rect}>` |
| attribute of an element or of an attribute category | `<{element/attribute}>` | `<{rect/rx}>`, `<{core-attributes/id}>` |
| interface, dictionary | `{{Name}}` | `{{SVGRectElement}}` |
| IDL attribute, method, constant | `{{Interface/member}}` | `{{SVGSVGElement/currentScale}}`, `{{SVGTextContentElement/getNumberOfChars()\|getNumberOfChars}}` |
| term | `[=term=]` or `[=term\|text=]` | `[=invalid value\|invalid=]` |

SVG 2 shows element and attribute names in curly quotes, so the shorthand sits inside a span: `<span class="element-name">‘<{rect}>’</span>`, `<span class="attr-name">‘<{rect/rx}>’</span>`.

Some links keep their long form, `<a data-link-type=... data-lt=...>`: links with other attributes (a `title`, an `id`), links whose text holds markup, attribute categories whose name has a space (`conditional processing`), and links inside `<pre>`. Links to other specs are plain `<a href>`.

Text that Bikeshed would read as a shorthand is escaped with a backslash: `\'none'`, `\[=`, `\{{`. Bikeshed reads no shorthand inside `<pre>`, `<script>`, `<style>` and `<xmp>`, so nothing is escaped there.

### Generated content

The element summaries, the lists of elements or attributes in a category, the attribute table and two indexes are not written by hand. They are made from `master/definitions.xml` (and the other definitions files listed in `config/svg2.json`) at every build, so a change of content model or attribute list is made once, in the definitions. In the source, each is an empty placeholder:

```html
<div data-svg-fill="element-summary" data-name="rect"></div>
<span data-svg-fill="element-category" data-name="graphics"></span>
```

| `data-svg-fill` | Element | Other attributes | Content |
|---|---|---|---|
| `element-summary` | `div` | `data-name`: element | the summary box: categories, content model, attributes, geometry properties, DOM interfaces |
| `element-category` | `span` | `data-name`: category | "a, b and c" |
| `attribute-category` | `span` | `data-name`, `data-omit-quotes` | "a, b and c" |
| `elements-with-attribute-category` | `span` | `data-name`, `data-omit-quotes` | the elements that take that category |
| `attribute-table` | `div` | | the table of the attribute index |
| `element-index` | `div` | | the list of the element index |
| `interface-index` | `div` | | the list of the interface index |

The definitions files are also read by the modules under `specs/`, to link into SVG 2.

### Ids

People link to SVG 2's ids from everywhere, so they stay. `check.sh` fails when an id listed in `tools/svg2-build/baseline/` is missing (see Checking below). Some ids are written in a particular way so that both the chapter pages and the single page keep theirs:

- `oldids="shapes-RectElement"` on a heading or a definition is the id the same element has on the single page;
- an empty `<span class="bs-old-id" id="...">` carries an id where `oldids` cannot go;
- an id used on several chapters (`Introduction`, `DOMInterfaces`, ...) is written in its single-page form with the short one beside it, `id="shapes-Introduction" data-multipage-id="Introduction"`. One Bikeshed document cannot hold the same id twice, so the splitter puts the short id back on each chapter page.

New sections need none of this: give them an ordinary `id`.

### Two renamed classes

Bikeshed rewrites any `table.propdef` and links every grammar symbol (`|`, `?`, `#`, ...) inside an element of class `prod`. SVG 2 keeps its own property tables and grammar text, so these classes are written `svg-propdef` and `svg-prod`.

### Adding a chapter

Add its `<pre class=include>path: name.bs</pre>` line to `master/index.bs`, and its entry (name, title, body class, appendix or not) to `pages` in `config/svg2-split.json`. `generate.py` stops if the two lists differ.

## How the build works

`build.sh` runs four steps:

1. **`generate.py`** reads `master/index.bs` and the chapter files it includes, fills in every `data-svg-fill` placeholder from the definitions files, and copies the chapters into one `index.bs`. Bikeshed runs its Markdown reader on included files whatever the metadata says, which would change the text, so the chapters are copied in rather than included. To link the generated content the way the rest of the source links, it reads which ids and definitions each chapter has from the `.bs` files themselves. It also writes `single-page-nav.json` for step 3.
2. **Bikeshed** builds `index.bs` into one HTML page.
3. **`singlepage.py`** makes `single-page.html`. It adds each chapter's navigation bar and table of contents, with the ids the single page had before the move to Bikeshed.
4. **`split.py`** cuts Bikeshed's page into the chapter pages:
   - it rewrites links that now go to another page, including the data behind Bikeshed's "Referenced in" panels and link hints;
   - it puts back ids that one big document cannot hold twice (`Introduction` is on 9 pages);
   - it writes the page headers, previous/next links, per-page tables of contents and appendix letters.

   Bikeshed cannot write several pages yet. Its unmerged `pagesplit` branch ([speced/bikeshed#269](https://github.com/speced/bikeshed/issues/269)) would replace part of this step.

## Checking

`check.sh` runs `check-preservation.py check --ids-only` on the build. It fails when a chapter page or an id listed in `tools/svg2-build/baseline/` is missing. That list holds the 1,256 ids of the chapter pages and the 1,284 ids of the single page that the last build from the old source published (2026-10-14).

To remove or rename an id on purpose, remove its row from `multipage-ids.tsv` and `single-page-ids.tsv` in the same pull request, so that the removal is visible in review. Renaming is better done by keeping the old id as an `oldids` value.

Links are not checked any more: they change with every edit. The full comparison (every link, where it lands) was run when the source was converted, and `check-preservation.py` can still do it between any two builds, without `--ids-only`, from a baseline made with its `extract` command.

## Configuration

Everything specific to SVG 2 is in `config/`, not in the code:

- `config/svg2.json`, read by `generate.py`: where the source is (`source`), the definitions files the generated content is made from, and how generated links are written (`typed_link_policy`, `reserved_ids`, `published_base`, `host_rewrites`, ...). Metadata, CSS, the `anchors` block and the front page are not here: they are in `master/index.bs` and `master/header.include`.
- `config/svg2-split.json`, read by `generate.py` and `split.py`: page order, file names, titles and navigation.

## Tests

`tests/` holds unit tests for every Python script here. They check what each script produces from small hand-written inputs in `tests/fixtures/`: a tiny old-style source with `edit:*` elements, its definitions file, and small pages shaped like Bikeshed's output. The `generate.py` tests convert that source in source mode and check that `generate.py` puts back exactly what the converter makes in one go. They use the standard library only (`unittest`), need neither Bikeshed nor the network, and take a few seconds. From the root of the repository:

```sh
make test
# or
python3 -m unittest discover -s tools/svg2-build/tests -t tools/svg2-build
```

Run them after changing a script. A failing test either points at a real change in the output, or at a test that needs updating because the change was intended; say which in the commit message.

One more test builds the real SVG 2 with `build.sh` and runs `check.sh`. It is skipped unless you ask for it, because it needs Bikeshed:

```sh
SVG_BIKESHED_E2E=1 make test
```

It uses the Bikeshed in `$BIKESHED`, or `bikeshed` on your PATH.

## Continuous integration

`.github/workflows/publish.yml`:

- **The `build` job** installs Bikeshed, runs `make all-specs` (SVG 2 with Bikeshed, the modules with the old build), and `tools/deploy.sh` publishes `build/bikeshed/svg2-draft/` at https://w3c.github.io/svgwg/svg2-draft/.
- **The `check` job** runs the unit tests (`make test`), then `make check`, on every push and pull request. Its report (`losses.tsv`) and Bikeshed's log are kept as artifacts of the run.

## The converter, and the modules

`convert.py`, `svgdefs.py` and `measure.py` turned the old HTML source into Bikeshed and measured the result. They stay for two reasons: `generate.py` uses their code to write the generated content, and the modules under `specs/` are still in the old format and are meant to move the same way, each with its own configuration file (the keys are those of `tests/fixtures/config/tiny.json`).

The SVG 2 source was made from a checkout of the old source with:

```sh
python3 tools/svg2-build/convert.py --source . --config CONFIG.json --source-mode --out master
```

The configuration used then (metadata, CSS, anchors, front page, class renames) went into `master/index.bs` and `master/header.include`, and is not kept separately.

`--source-mode` writes links as shorthands and the generated content as placeholders. Without it, the converter writes one `.bs` file per page with everything spelled out; `measure.py` reads that output when the converter runs with `--trace-links`.

## Updating Bikeshed

The build runs with the latest Bikeshed release, and with `--no-update`, so it uses the cross-reference data shipped with that release. If a new release changes the output, compare a build made with each.
