# Bikeshed version of SVG 2

These scripts build the SVG 2 editor's draft with [Bikeshed](https://speced.github.io/bikeshed/), from the same source as the current build (`master/*.html`, `master/publish.xml`, `master/definitions*.xml`). The result has the same pages, the same text, every id and every link of the current version, on the chapter pages and on the single page.

For now both versions are built from `master/`. The current one stays published at https://w3c.github.io/svgwg/svg2-draft/, and the Bikeshed one goes next to it at https://w3c.github.io/svgwg/svg2-draft-bikeshed/. Once the Bikeshed version has proven itself, the `.bs` files it produces become the source, and these conversion scripts are retired.

**Do not edit the generated `.bs` files while `master/` is the source.** They are rewritten on every build. A problem in the output is fixed either in `master/` or in these scripts.

## Requirements

- Python 3.9 or later for these scripts. They use the standard library only.
- [Bikeshed](https://speced.github.io/bikeshed/#installing), latest release (`pip install bikeshed`). Bikeshed itself needs Python 3.12 or later. The scripts use the `bikeshed` on your PATH, or the one named in `$BIKESHED`.
- Node.js, only for `make bikeshed-check`, which also builds the current version.

## Use

From the root of the repository:

```sh
make bikeshed          # build the Bikeshed version into build/bikeshed/svg2-draft/
make bikeshed-check    # build both versions and compare them
make bikeshed-test     # run the unit tests of these scripts (see Tests below)
```

Or call the scripts directly: `tools/bikeshed/build.sh [OUT_DIR]` and `tools/bikeshed/check.sh [OLD_DIR] [NEW_DIR]`.

`build/bikeshed/` then holds:

- `work/`: the generated `.bs` files, Bikeshed's own single-page output `index.html`, and `build.log` with Bikeshed's messages;
- `svg2-draft/`: what gets published, that is the 28 chapter pages, `single-page.html`, `style/`, `images/`, the stub pages of removed chapters, and `fragment-links.json` (which page holds each id);
- `baseline/` and `losses.tsv`, after a check.

## How it works

`build.sh` runs five steps:

1. **`convert.py`** turns `master/*.html` into one `.bs` file per page and an `index.bs` that holds them all. It reads `publish.xml` and the definitions files the same way the current tool does (`svgdefs.py`), keeps every id written in the source, and gives each element the chapter-prefixed id of the single page as well (`shapes-RectElement`). It replaces each `edit:*` element with its Bikeshed form, and writes element summaries, category lists, the attribute table and the indexes from the definitions. Untyped links become typed Bikeshed links (`<{rect}>`, `{{SVGElement}}`, `'fill'`), pointing where the current tool sends them.
2. **Bikeshed** builds `index.bs` into one HTML page.
3. **`idlkeywords.py`** links the `setter` keyword in the IDL, which Bikeshed leaves as plain text ([speced/bikeshed#3326](https://github.com/speced/bikeshed/pull/3326) would make this step unnecessary).
4. **`singlepage.py`** makes `single-page.html`. It adds each chapter's navigation bar and table of contents, with the ids the current single page has.
5. **`split.py`** cuts Bikeshed's page into the chapter pages:
   - it rewrites links that now go to another page, including the data behind Bikeshed's "Referenced in" panels and link hints;
   - it puts back ids that one big document cannot hold twice (`Introduction` is on 9 pages);
   - it writes the page headers, previous/next links, per-page tables of contents and appendix letters.

   Bikeshed cannot write several pages yet. Its unmerged `pagesplit` branch ([speced/bikeshed#269](https://github.com/speced/bikeshed/issues/269)) would replace part of this step.

`check.sh` reads the current build (`build/publish/`) and the Bikeshed build with `check-preservation.py`. It fails if any id or link of the current version is missing from the Bikeshed version. A link counts as kept when it lands on the same element, even under another id. These differences are deliberate and are listed, not counted as losses:

- typed links to an element, attribute, property or interface land on its definition (the summary box or the IDL), as in other Bikeshed specs, rather than on the section heading, whose id still exists;
- IDL member names that linked to themselves are now Bikeshed's definitions; their old ids still exist;
- links to the animations module move from the old SVG WG host to `w3c.github.io`.

`measure.py` is a development tool. It compares the text of every block and where each link lands, in more detail, when `convert.py` is run with `--trace-links`.

## Configuration

Everything specific to SVG 2 is in `config/`, not in the code:

- `config/svg2.json`, read by `convert.py`, `idlkeywords.py` and `singlepage.py`:
  - Bikeshed metadata, the front page, CSS added on top of Bikeshed's;
  - the ids Bikeshed reserves;
  - the `anchors` block, which keeps links to other specs on the targets the current version uses;
  - the IDL keywords to link.
- `config/svg2-split.json`, read by `split.py`: page order, file names, titles and navigation.

The same scripts are meant to convert the single-page modules under `specs/` later, each with its own configuration file.

## Tests

`tests/` holds unit tests for every Python script here. They check what each script produces from small hand-written inputs in `tests/fixtures/`: a tiny source with `edit:*` elements, a tiny `publish.xml` and definitions file, and small pages shaped like Bikeshed's output. They use the standard library only (`unittest`), need neither Bikeshed nor the network, and take a few seconds. From the root of the repository:

```sh
make bikeshed-test
# or
python3 -m unittest discover -s tools/bikeshed/tests -t tools/bikeshed
```

Run them after changing a script. A failing test either points at a real change in the output, or at a test that needs updating because the change was intended; say which in the commit message.

One more test builds the real SVG 2 with `build.sh` and runs `check.sh` against `build/publish`. It is skipped unless you ask for it, because it needs Bikeshed and a current build from `make`:

```sh
SVG_BIKESHED_E2E=1 make bikeshed-test
```

It uses the Bikeshed in `$BIKESHED`, or `bikeshed` on your PATH.

## Continuous integration

`.github/workflows/publish.yml` does two things with these scripts:

- **The `build` job** builds the Bikeshed version after the current specs, and `tools/deploy.sh` publishes it at `svg2-draft-bikeshed/`. That step is allowed to fail: it never blocks the publication of the current specs.
- **The `bikeshed-check` job** runs the unit tests (`make bikeshed-test`), then `make bikeshed-check`, on every push and pull request. It fails when the Bikeshed version loses an id or a link. Its report (`losses.tsv`) and Bikeshed's log are kept as artifacts of the run.

## Updating Bikeshed

The build runs with the latest Bikeshed release, and with `--no-update`, so it uses the cross-reference data shipped with that release. If a new release changes the output, `make bikeshed-check` shows it.
