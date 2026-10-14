"""split.py: cut Bikeshed's single page into the chapter pages.

The splitter runs on fixtures/split/index.html (a tiny page shaped like
Bikeshed's output) in a child Python, the way build.sh calls it, and the
tests read the pages it writes."""

import json
import os
import re
import unittest

from . import helpers

split = helpers.load("split.py")

SINGLE = helpers.fixture("split", "index.html")
CONFIG = helpers.fixture("split", "config.json")
RESOURCES = helpers.fixture("split", "resources")


def run_split(tmp, single=SINGLE, resources=True):
    out = tmp.join("out")
    args = ["--single", single, "--out", out, "--config", CONFIG]
    if resources:
        args += ["--resources", RESOURCES]
    status, stdout, stderr = helpers.run_script("split.py", *args)
    return out, status, stdout, stderr


def body_of(page):
    return page[page.index("<body"):]


class SplitTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = helpers.TempDir()
        cls.out, cls.status, cls.stdout, cls.stderr = run_split(cls.tmp)
        cls.pages = {}
        for fn in ("index.html", "intro.html", "shapes.html", "idl.html"):
            cls.pages[fn] = helpers.read(os.path.join(cls.out, fn))
        cls.report = json.loads(helpers.read(os.path.join(cls.out, "split-report.json")))
        cls.fragments = json.loads(helpers.read(os.path.join(cls.out, "fragment-links.json")))

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_runs_clean(self):
        self.assertEqual(self.status, 0, self.stdout + self.stderr)
        self.assertEqual(self.report["problems_after_split"], {})
        self.assertEqual(self.report["pages"], ["index.html", "intro.html", "shapes.html", "idl.html"])

    # -- cutting at the page markers -----------------------------------------

    def test_each_chapter_on_its_own_page(self):
        intro, shapes, idl = self.pages["intro.html"], self.pages["shapes.html"], self.pages["idl.html"]
        self.assertIn("draws <a", intro)
        self.assertNotIn("Shapes intro</span>", intro)
        self.assertIn("Back to", shapes)
        self.assertNotIn("draws <a", shapes)
        self.assertIn("interface <dfn", idl)

    def test_front_page_gets_header_front_matter_and_back_matter(self):
        front = self.pages["index.html"]
        self.assertIn('<div class="head"><h1 id="title">Tiny SVG</h1></div>', front)
        self.assertIn("Thanks to", front)
        self.assertIn('id="index"><span class="content">Index</span>', front)
        self.assertNotIn("Back to", front)

    # -- links ------------------------------------------------------------------

    def test_links_to_other_pages_rewritten(self):
        intro = self.pages["intro.html"]
        self.assertIn('<a data-link-type="element" href="shapes.html#elementdef-rect" id="ref-for-elementdef-rect">',
                      intro)
        self.assertIn('<a href="shapes.html#RectElement">the rect section</a>', intro)
        # a single-page id goes to the chapter-page id
        self.assertIn('<a href="shapes.html#Introduction">the shapes intro</a>', intro)
        # the chapter heading itself: the page, no fragment
        self.assertIn('<a href="shapes.html">chapter 2</a>', intro)
        # from the back matter on the front page
        self.assertIn('<a href="intro.html#TermUserAgent">user agent</a>', self.pages["index.html"])

    def test_links_on_the_same_page(self):
        shapes = self.pages["shapes.html"]
        self.assertIn('<a href="#RectElement">the section</a>', shapes)
        self.assertIn('<a href="#RectElement">its alias</a>', shapes)
        self.assertIn('<a class="self-link" href="#Introduction"></a>', shapes)

    def test_alias_of_existing_id_followed(self):
        # intro-AboutPara is an alias of AboutPara on intro.html
        self.assertIn('<a href="intro.html#AboutPara">about</a>', self.pages["shapes.html"])

    # -- ids --------------------------------------------------------------------

    def test_heading_with_multipage_id_gets_short_id_back(self):
        self.assertIn('<h2 class="heading settled" data-level="1.1" data-multipage-id="Introduction" id="Introduction">'
                      '<span class="bs-old-id" id="intro-Introduction"></span>', self.pages["intro.html"])
        self.assertIn('id="Introduction"><span class="bs-old-id" id="shapes-Introduction"></span>',
                      self.pages["shapes.html"])

    def test_other_element_with_multipage_id_gets_a_span(self):
        self.assertIn('<p id="shapes-Para" data-multipage-id="Para"><span class="bs-old-id" id="Para"></span>',
                      self.pages["shapes.html"])

    def test_lone_alias_gets_its_short_id(self):
        self.assertIn('<span class="bs-old-id" id="shapes-Extra"></span><span class="bs-old-id" id="Extra"></span>',
                      self.pages["shapes.html"])

    def test_restored_ids_reported(self):
        got = sorted((r["page"], r["id"], r["how"]) for r in self.report["ids_restored"])
        self.assertEqual(got, [("intro.html", "Introduction", "data-multipage-id"),
                               ("shapes.html", "Extra", "single-page alias"),
                               ("shapes.html", "Introduction", "data-multipage-id"),
                               ("shapes.html", "Para", "data-multipage-id")])

    def test_fragment_links_json(self):
        ids = self.fragments["ids"]
        self.assertEqual(ids["RectElement"], "shapes.html")
        self.assertEqual(ids["Introduction"], "intro.html")   # first page that has it
        self.assertEqual(ids["index"], "index.html")
        self.assertEqual(self.fragments["single_page_aliases"]["shapes-Introduction"], "shapes.html#Introduction")
        self.assertEqual(self.fragments["single_page_aliases"]["intro-AboutPara"], "intro.html#AboutPara")

    # -- headers, tables of contents, numbering --------------------------------

    def test_chapter_header(self):
        intro = body_of(self.pages["intro.html"])
        self.assertIn('<h1><span class="bs-old-id" id="chapter-intro"></span>Chapter 1: Introduction</h1>'
                      '<nav id="toc"><div class="header"><a href="./">Overview</a> · <a href="./">Previous</a> · '
                      '<a href="shapes.html">Next</a> · <a href="eltindex.html">Elements</a></div>'
                      '<h2 id="Contents" class="contents">Contents</h2>', intro)
        # the header stays outside <main>
        self.assertLess(intro.index("</nav>"), intro.index("<main>"))

    def test_previous_and_next(self):
        self.assertIn('<a href="intro.html">Previous</a> · <a href="idl.html">Next</a>', self.pages["shapes.html"])
        idl = self.pages["idl.html"]
        self.assertIn('<a href="shapes.html">Previous</a> · <a href="eltindex.html">Elements</a>', idl)
        self.assertNotIn(">Next<", idl)

    def test_chapter_toc(self):
        self.assertIn('<li><a href="shapes.html#RectElement"><span class="secno">2.2.</span> The rect element</a>'
                      '<ol class="toc"><li><a href="shapes.html#RectAttrs"><span class="secno">2.2.1.</span> '
                      'Attributes</a></li></ol></li>', self.pages["shapes.html"])

    def test_headings_promoted(self):
        shapes = self.pages["shapes.html"]
        self.assertIn('<h2 class="heading settled" data-level="2.2" id="RectElement">', shapes)
        self.assertIn('<h3 class="heading settled" data-level="2.2.1" id="RectAttrs">', shapes)
        self.assertNotIn("<h4", shapes)

    def test_appendix_letters(self):
        idl = self.pages["idl.html"]
        self.assertIn('<h1><span class="bs-old-id" id="chapter-idl"></span>Appendix A: IDL Definitions</h1>', idl)
        self.assertIn('<h2 class="heading settled" id="IdlSection"><span class="secno">A.1. </span>', idl)
        self.assertIn('<ol class="toc appendix-toc">', idl)
        self.assertIn('<a href="idl.html#IdlSection"><span class="secno">A.1.</span> All IDL</a>', idl)

    def test_drop_headings(self):
        idl = self.pages["idl.html"]
        self.assertIn('<span id="idl-index"></span>', idl)
        self.assertNotIn("IDL Index", idl)

    def test_full_toc_on_front_page(self):
        front = self.pages["index.html"]
        self.assertIn('<nav id="toc" data-never-rename="">\n  <h2 id="fulltoc">Table of Contents'
                      '<span id="contents"></span></h2>', front)
        self.assertIn('<li><span class="secno">1.</span> <a href="intro.html">Introduction</a>', front)
        self.assertIn('<a href="intro.html#Introduction"><span class="secno">1.1.</span> About</a>', front)
        self.assertIn('<li><a href="idl.html">Appendix A: IDL Definitions</a>', front)
        # Bikeshed's own table of contents is gone
        self.assertNotIn('data-fill-with="table-of-contents"', front)

    def test_head_title_canonical_and_extras(self):
        intro = self.pages["intro.html"]
        self.assertIn("<title>Introduction \u2014 Tiny</title>", intro)
        self.assertNotIn('rel="canonical"', intro)
        self.assertIn('<link rel="stylesheet" href="style/tiny.css"/>', intro)
        self.assertIn('<body class="chapter-intro">', intro)
        front = self.pages["index.html"]
        self.assertIn("<title>Tiny SVG</title>", front)
        self.assertIn('rel="canonical"', front)
        self.assertIn('<meta name="front" content="yes">', front)
        self.assertIn('<body class="chapter-Overview">', front)

    # -- Bikeshed's script data -------------------------------------------------

    def data(self, page, name):
        m = re.search(r"let %s = \{\n(.*?)\n\};" % name, self.pages[page], re.S)
        out = {}
        for line in m.group(1).split("\n"):
            if line.strip():
                k, v = line.split(": ", 1)
                out[json.loads(k)] = json.loads(v.rstrip(","))
        return out

    def test_dfn_panels_follow_their_dfn(self):
        intro = self.data("intro.html", "dfnPanelData")
        self.assertEqual(list(intro), ["TermUserAgent"])
        self.assertEqual(intro["TermUserAgent"]["refSections"][0]["refs"][0]["url"],
                         "shapes.html#ref-for-TermUserAgent")
        shapes = self.data("shapes.html", "dfnPanelData")
        self.assertEqual(list(shapes), ["elementdef-rect"])
        self.assertEqual(shapes["elementdef-rect"]["refSections"][0]["refs"][0]["url"],
                         "intro.html#ref-for-elementdef-rect")
        self.assertEqual(self.data("index.html", "dfnPanelData"), {})

    def test_dfn_panel_script_patched(self):
        self.assertIn("mk.a({ href: ref.url || `#${ref.id}` },", self.pages["intro.html"])

    def test_ref_hints_rewritten_and_trimmed(self):
        intro = self.data("intro.html", "refsData")
        self.assertEqual(list(intro), ["shapes.html#elementdef-rect"])
        self.assertEqual(intro["shapes.html#elementdef-rect"]["url"], "shapes.html#elementdef-rect")
        self.assertEqual(list(self.data("index.html", "refsData")), ["intro.html#TermUserAgent"])

    def test_scripts_after_main_on_every_page(self):
        for fn, page in self.pages.items():
            self.assertIn('<script src="https://www.w3.org/scripts/TR/2021/fixup.js"></script>', page, fn)
            self.assertIn('<script src="style/expanders.js"></script>', page, fn)

    # -- resources --------------------------------------------------------------

    def test_resources_copied(self):
        self.assertTrue(os.path.isfile(os.path.join(self.out, "style", "tiny.css")))
        self.assertTrue(os.path.isfile(os.path.join(self.out, "stub.html")))
        self.assertEqual(self.report["resources_missing"], ["missing-folder"])


class SplitFaultTests(unittest.TestCase):
    def setUp(self):
        self.tmp = helpers.TempDir()

    def tearDown(self):
        self.tmp.cleanup()

    def variant(self, old, new):
        text = helpers.read(SINGLE)
        self.assertIn(old, text)
        p = self.tmp.join("index.html")
        helpers.write(p, text.replace(old, new, 1))
        return p

    def test_link_to_nowhere_reported_and_fails(self):
        single = self.variant('<a href="#RectElement">the section</a>', '<a href="#nowhere">the section</a>')
        out, status, _, _ = run_split(self.tmp, single, resources=False)
        self.assertEqual(status, 1)
        report = json.loads(helpers.read(os.path.join(out, "split-report.json")))
        self.assertEqual(report["notes"]["link to an id that exists nowhere"], ["shapes.html: #nowhere"])
        self.assertEqual(report["problems_after_split"]["link to a missing fragment"], ["shapes.html: #nowhere"])

    def test_page_markers_must_match_config(self):
        single = self.variant('data-bs-page="shapes"', 'data-bs-page="other"')
        _, status, _, err = run_split(self.tmp, single, resources=False)
        self.assertNotEqual(status, 0)
        self.assertIn("page markers do not match the config", err)

    def test_chapter_start_inside_wrapper_refused(self):
        single = self.variant('<h2 class="heading settled" data-bs-page="shapes"',
                              '<div><h2 class="heading settled" data-bs-page="shapes"')
        single_text = helpers.read(single).replace('</main>', '</div></main>', 1)
        helpers.write(single, single_text)
        _, status, _, err = run_split(self.tmp, single, resources=False)
        self.assertNotEqual(status, 0)
        self.assertIn("starts inside an open element", err)


class HelperTests(unittest.TestCase):
    def test_set_attr(self):
        self.assertEqual(split.set_attr('<a href="#x" id=y>', "href", "p.html#x"), '<a href="p.html#x" id=y>')
        self.assertEqual(split.set_attr("<br/>", "class", 'a"b'), '<br class="a&quot;b"/>')

    def test_rename_tag(self):
        self.assertEqual(split.rename_tag('<h3 id="a">', "h2"), '<h2 id="a">')
        self.assertEqual(split.rename_tag("</h3>", "h2"), "</h2>")

    def test_matching_end_counts_nesting(self):
        tags = split.scan("<div><div></div><p></div>")
        self.assertEqual(split.matching_end(tags, 0), 4)

    def test_edits_apply_in_order_and_refuse_overlap(self):
        text = "0123456789"
        e = split.Edits()
        e.replace(2, 4, "ab")
        e.insert(2, "^")
        self.assertEqual(e.apply(text, 0, 10), "01^ab456789")
        e.replace(3, 5, "zz")
        with self.assertRaises(ValueError):
            e.apply(text, 0, 10)

    def test_verify_finds_missing_fragments_and_duplicate_ids(self):
        files = {"a.html": '<p id="x"></p><p id="x"></p><a href="b.html#y">y</a><a href="#x">x</a>',
                 "b.html": '<p id="z"></p><a href="https://example.org/#q">ext</a>'}
        problems = split.verify(files)
        self.assertEqual(problems["duplicate id on a page"], ["a.html#x"])
        self.assertEqual(problems["link to a missing fragment"], ["a.html: b.html#y"])


if __name__ == "__main__":
    unittest.main()
