"""check-preservation.py: does a new build keep every id and link of a baseline?

The synthetic cases come from the self test written while the checker was
developed (selftest-check-preservation.sh): small made-up pages where a
link moves to an alias of its old target, to the definition in the same
section, elsewhere in the section, or to another section. Then a round
trip on a tiny site: checked against itself it loses nothing, and planted
faults are all caught."""

import os
import re
import shutil
import unittest

from . import helpers

check = helpers.load("check-preservation.py")


def extract(multipage, single, out):
    status, stdout, stderr = helpers.run_script("check-preservation.py", "extract", "--multipage", multipage,
                                                "--single", single, "--out", out)
    assert status == 0, stdout + stderr


def run_check(baseline, *args):
    """Returns (exit status, report text)."""
    status, stdout, stderr = helpers.run_script("check-preservation.py", "check", "--baseline", baseline,
                                                "--limit", "1000", *args)
    return status, stdout + stderr


def baseline_from(tmp, page_path, name="base"):
    """A baseline from one page used as both the multipage set and the single page."""
    old = tmp.join(name + "-old")
    os.makedirs(old)
    shutil.copy(page_path, os.path.join(old, "index.html"))
    shutil.copy(page_path, os.path.join(old, "single-page.html"))
    base = tmp.join(name)
    extract(old, os.path.join(old, "single-page.html"), base)
    return base


class SyntheticTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = helpers.TempDir()
        base = baseline_from(cls.tmp, helpers.fixture("check", "synthetic", "old", "index.html"))
        new = helpers.fixture("check", "synthetic", "new", "index.html")
        cls.default = run_check(base, "--single", new)
        cls.same = run_check(base, "--single", new, "--allow-same-section")
        cls.strict = run_check(base, "--single", new, "--strict")

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_exactly_two_losses_by_default(self):
        status, text = self.default
        self.assertEqual(status, 1)
        self.assertRegex(text, r"LOSSES 2\n")
        self.assertIn("TOTAL LOSSES: 2", text)

    def test_alias_of_old_target_is_kept(self):
        # the toc entry and the "rect heading" link land on the same element
        self.assertIn("2 land on the same element under another fragment", self.default[1])

    def test_definition_in_same_section_is_kept_and_listed(self):
        self.assertIn("1 on the definition in the same section", self.default[1])

    def test_same_section_move_is_a_loss(self):
        self.assertIn("'the element' #0: single-page.html#RectElement -> single-page.html#Note", self.default[1])

    def test_moved_link_not_hidden_by_copy_elsewhere(self):
        self.assertIn("a@href 'rect' #0 -> now in another section", self.default[1])

    def test_toc_number_format_change_still_pairs(self):
        # '1.1.' in the baseline, '1.1' in the new build
        self.assertIn("0 vanished", self.default[1])

    def test_allow_same_section(self):
        status, text = self.same
        self.assertRegex(text, r"LOSSES 1\n")
        self.assertIn("same section (accepted)", text)

    def test_strict_reports_fragment_change_on_same_element(self):
        self.assertIn("'rect heading' #0: single-page.html#RectElement -> single-page.html#rect", self.strict[1])
        self.assertIn("[strict: fragment strings compared]", self.strict[1])


class SelfLinkTests(unittest.TestCase):
    """A link that pointed at its own id (SVG 2 IDL member names) is accepted
    when Bikeshed replaced it by a definition and the id survives."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = helpers.TempDir()
        base = baseline_from(cls.tmp, helpers.fixture("check", "selflink", "old", "index.html"))
        new = helpers.fixture("check", "selflink", "new", "index.html")
        gone = cls.tmp.join("gone.html")
        helpers.write(gone, helpers.read(new).replace('<span class="bs-old-id" id="__svg__X__m"></span>', ""))
        cls.default = run_check(base, "--single", new)
        cls.keep = run_check(base, "--single", new, "--keep-self-links")
        cls.gone = run_check(base, "--single", gone)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_listed_not_lost_while_id_survives(self):
        status, text = self.default
        self.assertEqual(status, 0)
        self.assertIn("1 self-links dropped", text)
        self.assertRegex(text, r"LOSSES 0\n")

    def test_keep_self_links_counts_it(self):
        status, text = self.keep
        self.assertEqual(status, 1)
        self.assertRegex(text, r"LOSSES 1\n")

    def test_id_gone(self):
        status, text = self.gone
        self.assertEqual(status, 1)
        self.assertIn("1 missing", text)
        self.assertIn("1 vanished", text)


class HeadResourceTests(unittest.TestCase):
    """Style sheet and script references are not links a reader follows:
    dropping the old ones is not a loss, unless --strict."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = helpers.TempDir()
        old = cls.tmp.join("old.html")
        helpers.write(old, '<html><head><link rel="stylesheet" href="style/svg.css">'
                           '<script src="style/expanders.js"></script></head>'
                           '<body><h2 id="A">A</h2><p><a href="#A">a</a></p></body></html>')
        new = cls.tmp.join("new.html")
        helpers.write(new, '<html><head><link href="https://www.w3.org/StyleSheets/TR/2021/W3C-ED" '
                           'rel="stylesheet"></head>'
                           '<body><h2 id="A">A</h2><p><a href="#A">a</a></p></body></html>')
        base = baseline_from(cls.tmp, old)
        cls.default = run_check(base, "--single", new)
        cls.strict = run_check(base, "--single", new, "--strict")

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_not_compared_by_default(self):
        status, text = self.default
        self.assertEqual(status, 0)
        self.assertIn("2 style sheet and script references not compared", text)
        self.assertRegex(text, r"LOSSES 0\n")

    def test_strict_compares_them(self):
        status, text = self.strict
        self.assertEqual(status, 1)
        self.assertIn("0 style sheet and script references not compared", text)


class RoundTripTests(unittest.TestCase):
    """extract then check on a tiny site: no loss against itself, and each
    planted fault is reported."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = helpers.TempDir()
        cls.site = helpers.fixture("check", "site")
        cls.base = cls.tmp.join("baseline")
        extract(cls.site, os.path.join(cls.site, "single-page.html"), cls.base)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_baseline_files(self):
        for fn in ("multipage-ids.tsv", "multipage-links.tsv", "multipage-page-counts.tsv",
                   "multipage-duplicate-ids.tsv", "multipage-ids-on-several-pages.tsv",
                   "multipage-broken-links.tsv", "single-page-ids.tsv", "single-page-links.tsv"):
            self.assertTrue(os.path.isfile(os.path.join(self.base, fn)), fn)
        several = check.read_tsv(os.path.join(self.base, "multipage-ids-on-several-pages.tsv"))
        self.assertEqual([(r["anchor"], r["pages"]) for r in several], [("Introduction", "paths.html shapes.html"), ("toc", "index.html shapes.html")])

    def test_links_resolved_against_their_page(self):
        links = check.read_tsv(os.path.join(self.base, "multipage-links.tsv"))
        rows = [(r["source_page"], r["target_page"], r["target_fragment"], r["target_exists"]) for r in links
                if r["link_text"] == "use"]
        self.assertEqual(rows, [("shapes.html", "paths.html", "UseElement", "yes")])
        # "./" is the front page; an image inside the spec is a link too
        self.assertIn(("shapes.html", "index.html"), [(r["source_page"], r["target_page"]) for r in links])
        self.assertIn("img@src", [r["kind"] for r in links])

    def test_site_against_itself_has_no_loss(self):
        status, text = run_check(self.base, "--multipage", self.site,
                                 "--single", os.path.join(self.site, "single-page.html"))
        self.assertEqual(status, 0, text)
        self.assertIn("TOTAL LOSSES: 0", text)

    def test_planted_faults_are_caught(self):
        d = self.tmp.join("damaged")
        shutil.copytree(self.site, d)

        def edit(fn, old, new):
            p = os.path.join(d, fn)
            text = helpers.read(p)
            self.assertIn(old, text)
            helpers.write(p, text.replace(old, new, 1))

        edit("shapes.html", 'id="RectNote"', 'id="rect-note"')                           # id renamed
        edit("shapes.html", 'href="paths.html#UseElement"', 'href="paths.html#use-element"')  # link retargeted
        edit("paths.html", '<a href="#PathLengthAttribute">pathLength</a>', "pathLength")  # link removed
        edit("single-page.html", 'id="paths-ForeignObjectElement"', 'id="ForeignObjectElement"')
        os.remove(os.path.join(d, "index.html"))                                          # page removed
        tsv = self.tmp.join("losses.tsv")
        status, text = run_check(self.base, "--multipage", d, "--single", os.path.join(d, "single-page.html"),
                                 "--losses-tsv", tsv)
        self.assertEqual(status, 1)
        self.assertRegex(text, r"(?m)^   shapes\.html#RectNote$")
        self.assertIn("shapes.html#RectNote", text)
        self.assertRegex(text, r"(?m)^   index\.html$")
        self.assertIn("paths.html (in #-) a@href 'pathLength' #0 -> paths.html#PathLengthAttribute (link not found)", text)
        self.assertRegex(text, r"(?m)^   single-page\.html#paths-ForeignObjectElement$")
        self.assertIn("paths.html#UseElement -> paths.html#use-element (new target does not exist)", text)
        verdicts = sorted(r["verdict"] for r in check.read_tsv(tsv))
        self.assertIn("id missing", verdicts)
        self.assertIn("vanished", verdicts)
        self.assertNotIn("TOTAL LOSSES: 0", text)


class FunctionTests(unittest.TestCase):
    def test_resolve(self):
        self.assertEqual(check.resolve("#x", "shapes.html")[:3], (True, "shapes.html", "x"))
        self.assertEqual(check.resolve("./", "shapes.html")[:3], (True, "index.html", ""))
        self.assertEqual(check.resolve("paths.html#a%20b", "shapes.html")[:3], (True, "paths.html", "a b"))
        internal, _, frag, url = check.resolve("https://www.w3.org/TR/SVG11/#x", "a.html")
        self.assertFalse(internal)
        self.assertEqual((frag, url), ("x", "https://www.w3.org/TR/SVG11/#x"))
        # http on the spec host counts as the spec
        self.assertTrue(check.resolve("http://w3c.github.io/svgwg/svg2-draft/a.html", "b.html")[0])

    def test_page_name(self):
        self.assertEqual(check.page_name("Overview.html"), "index.html")
        self.assertEqual(check.page_name("shapes.html"), "shapes.html")

    def test_tidy_and_match_text(self):
        self.assertEqual(check.tidy_text("  ‘rect’ \n element "), "rect element")
        self.assertEqual(check.match_text("1.1. Shapes"), "Shapes")
        self.assertEqual(check.match_text("1.1 Shapes"), "Shapes")
        self.assertEqual(check.match_text("B.1. Annex"), "Annex")
        self.assertEqual(check.match_text("§ 10.2 Paths"), "Paths")
        self.assertEqual(check.match_text("A path"), "A path")

    def test_alias_marker_lands_on_parent_or_next_element(self):
        p = check.PageParser()
        p.page = "x.html"
        p.feed('<div><h2 id="h"><span class="bs-old-id" id="old"></span>Title</h2>'
               '<span class="bs-old-id" id="before"></span><p id="para">text</p>'
               '<span id="real"></span><p>more</p></div>')
        p.close()
        doc = check.Doc(p)
        h, para = doc.spot("h"), doc.spot("para")
        self.assertEqual(doc.spot("old"), h)            # first thing in the heading: the heading
        self.assertEqual(doc.spot("before"), para)      # marker just before: the paragraph
        self.assertEqual(len(doc.spot("real")), 1)      # an empty span without the class is itself
        self.assertNotEqual(doc.spot("real"), para)
        self.assertIsNone(doc.spot("missing"))

    def test_area_of(self):
        self.assertEqual(check.area_of({"source_id": "toc", "kind": "a@href"}), "table of contents")
        self.assertEqual(check.area_of({"source_id": "shapes-toc", "kind": "a@href"}), "chapter table of contents")
        self.assertEqual(check.area_of({"source_id": "", "kind": "a@href"}), "outside any id")
        self.assertEqual(check.area_of({"source_id": "", "kind": "link@href"}), "head (link@href)")


if __name__ == "__main__":
    unittest.main()
