"""singlepage.py: single-page.html from Bikeshed's index.html, with each
chapter's navigation bar and table of contents, appendix numbers, and the
headings today's page does not have removed."""

import shutil
import unittest

from . import helpers

singlepage = helpers.load("singlepage.py")

NAV = {"pages": ["intro", "shapes", "idl"], "index": ["Overview"], "elements": "shapes",
       "attributes": None, "properties": None, "toc": True}


class PieceTests(unittest.TestCase):
    def test_entry_html_cleans_heading(self):
        inner = ('<span class="secno">2.1 </span><span class="bs-old-id" id="x-y"></span>'
                 '<span class="content">The <dfn id="d">rect</dfn> <a href="#z">element</a></span>'
                 '<a class="self-link" href="#y"></a>')
        self.assertEqual(singlepage.entry_html(inner),
                         '<span class="secno">2.1.</span> The <span>rect</span> element')

    def test_entry_html_without_number(self):
        self.assertEqual(singlepage.entry_html('<span class="content">Plain</span>'), "Plain")

    def test_chapter_toc_nesting_and_skips(self):
        body = ('<h3 id="a"><span class="content">A</span></h3>'
                '<h4 id="a1"><span class="content">A1</span></h4>'
                '<h3 id="b" class="no-toc">B</h3>'
                '<h3><span class="content">no id</span></h3>'
                '<h3 id="c"><span class="content">C</span></h3>')
        self.assertEqual(singlepage.chapter_toc(body),
                         '<ol class="toc"><li><ol class="toc"><li><a href="#a">A</a>'
                         '<ol class="toc"><li><a href="#a1">A1</a></li></ol></li>'
                         '<li><a href="#c">C</a></li></ol></li></ol>')

    def test_chapter_toc_empty(self):
        self.assertEqual(singlepage.chapter_toc("<p>nothing</p>"), "")

    def test_number_appendix(self):
        numbers = {}
        body = ('<h3 id="a"><span class="content">A</span></h3>'
                '<h4 id="a1">A1</h4><h4 id="a2">A2</h4>'
                '<h3 id="b">B</h3><h4 id="b1">B1</h4>'
                '<h3 id="skip" class="no-toc">S</h3>'
                '<h3 id="done"><span class="secno">X </span>Has one</h3>')
        out = singlepage.number_appendix(body, "K", numbers)
        self.assertEqual(numbers, {"a": "K.1.", "a1": "K.1.1.", "a2": "K.1.2.", "b": "K.2.", "b1": "K.2.1."})
        self.assertIn('<h3 id="a"><span class="secno">K.1. </span><span class="content">A</span></h3>', out)
        self.assertIn('<h3 id="skip" class="no-toc">S</h3>', out)
        self.assertIn('<h3 id="done"><span class="secno">X </span>Has one</h3>', out)

    def test_nav_first_middle_last(self):
        first = singlepage.nav_html(NAV, "intro", "")
        self.assertEqual(first, '<nav id="intro-toc" class="chapter-toc" data-multipage-id="toc">'
                                '<div class="header"><a href="./">Overview</a> · <a href="./">Previous</a> · '
                                '<a href="#chapter-shapes">Next</a> · <a href="#chapter-shapes">Elements</a>'
                                '</div></nav>')
        middle = singlepage.nav_html(NAV, "shapes", "<ol></ol>")
        self.assertIn('<a href="#chapter-intro">Previous</a> · <a href="#chapter-idl">Next</a>', middle)
        self.assertIn('<h3 id="shapes-Contents" class="contents no-num no-toc" data-multipage-id="Contents">'
                      'Contents</h3><ol></ol>', middle)
        last = singlepage.nav_html(NAV, "idl", "")
        self.assertNotIn("Next", last)


class MainTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = helpers.TempDir()
        for fn in ("index.html", "single-page-nav.json"):
            shutil.copy(helpers.fixture("singlepage", fn), cls.tmp.join(fn))
        with helpers.quiet() as (out, _):
            singlepage.main(["singlepage.py", cls.tmp.path])
        cls.stdout = out.getvalue()
        cls.doc = helpers.read(cls.tmp.join("single-page.html"))

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_index_html_unchanged(self):
        self.assertEqual(helpers.read(self.tmp.join("index.html")),
                         helpers.read(helpers.fixture("singlepage", "index.html")))

    def test_one_nav_bar_per_chapter_right_after_its_heading(self):
        self.assertIn("3 chapter navigation bars added", self.stdout)
        for name in ("intro", "shapes", "idl"):
            self.assertIn('<a class="self-link" href="#chapter-%s"></a></h2><nav id="%s-toc" class="chapter-toc" '
                          'data-multipage-id="toc">' % (name, name), self.doc)

    def test_chapter_toc_ids(self):
        self.assertIn('<h3 id="shapes-Contents" class="contents no-num no-toc" data-multipage-id="Contents">', self.doc)
        self.assertIn('<li><a href="#RectElement"><span class="secno">2.1.</span> The <span>rect</span> element</a>'
                      '<ol class="toc"><li><a href="#RectAttrs"><span class="secno">2.1.1.</span> Attributes</a>',
                      self.doc)
        self.assertNotIn('href="#NotInToc"', self.doc)

    def test_appendix_numbers_in_headings_and_both_tocs(self):
        self.assertIn('<h3 class="heading settled" id="IdlSection"><span class="secno">A.1. </span>', self.doc)
        self.assertIn('<h4 class="heading settled" id="IdlSub"><span class="secno">A.1.1. </span>', self.doc)
        # Bikeshed's full table of contents
        self.assertIn('<li><a href="#IdlSection"><span class="secno">A.1.</span> <span class="content">All IDL</span>',
                      self.doc)
        # the chapter's own
        self.assertIn('<a href="#IdlSub"><span class="secno">A.1.1.</span> Sub part</a>', self.doc)

    def test_drop_headings(self):
        self.assertIn('<span class="bs-old-id" id="idl-index"></span>', self.doc)
        self.assertNotIn("IDL Index", self.doc)
        self.assertNotIn('href="#idl-index"', self.doc)

    def test_rest_untouched(self):
        self.assertIn('<h2 class="heading no-num no-ref settled" id="index"><span class="content">Index</span></h2>',
                      self.doc)
        self.assertIn('<pre class="idl">interface X {};</pre>', self.doc)


if __name__ == "__main__":
    unittest.main()
