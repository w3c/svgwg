"""measure.py: the development tool that compares ids, link counts, text
blocks and where traced links land."""

import json
import os
import unittest

from . import helpers

measure = helpers.load("measure.py")

NEW_INDEX = """<html><body>
<nav id="toc"><a href="#chapter-shapes">2. Basic Shapes</a></nav>
<main>
<h2 data-bs-page="shapes" id="chapter-shapes"><span class="secno">2. </span>Basic Shapes<a class="self-link" href="#chapter-shapes"></a></h2>
<h3 id="shapes-Introduction" data-multipage-id="Introduction">Introduction</h3>
<p id="Intro">Shapes use <a href="#RectElement" data-svgtrace="0">rect</a>, <a href="#Note" data-svgtrace="1">near</a>
and <a href="#Elsewhere" data-svgtrace="2">far</a>. It’s fine.</p>
<h3 id="RectElement">The rect element</h3>
<p id="Note">A note.</p>
<pre class="idl">interface <a href="#x">SVGRectElement</a> {};</pre>
<h3 id="Other">Other</h3>
<p id="Elsewhere">Elsewhere.</p>
</main>
<h2 id="index">Index</h2>
<p>Back matter text.</p>
</body></html>
"""

OLD_PAGE = """<html><body>
<h1>Chapter 2: Basic Shapes</h1>
<nav id="toc"><a href="#Introduction">2.1. Introduction</a></nav>
<h2 id="Introduction">2.1. Introduction</h2>
<p id="Intro">Shapes use <a href="#RectElement">rect</a>, <a href="#RectElement">near</a>
and <a href="#RectElement">far</a>. It's fine.</p>
<h2 id="RectElement">The rect element</h2>
<p id="Note">A note.</p>
<pre class="idl">interface <a href="#x">SVGRectElement</a> {};</pre>
<h2 id="Other">Other</h2>
<p id="Elsewhere">Elsewhere.</p>
<p id="OnlyOld">Gone.</p>
</body></html>
"""

OLD_SINGLE = """<html><body>
<div id="chapter-shapes"><h1>Basic Shapes</h1><h2 id="shapes-Introduction">Introduction</h2>
<p id="shapes-Lost">x</p></div>
<hr class="chapter-divider"><div id="chapter-paths"><p id="paths-Path">y</p></div>
</body></html>
"""


class NormTextTests(unittest.TestCase):
    def test_numbers_and_apostrophes(self):
        self.assertEqual(measure.norm_text("  10.2. The   rect element "), "The rect element")
        self.assertEqual(measure.norm_text("Chapter 3: Paths"), "Paths")
        self.assertEqual(measure.norm_text("Appendix B: Index"), "Index")
        self.assertEqual(measure.norm_text("It’s"), "It's")


class ScanTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = helpers.TempDir()
        p = cls.tmp.join("index.html")
        helpers.write(p, NEW_INDEX)
        cls.scan = measure.scan(p)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_ids_with_section_and_chapter(self):
        ids = self.scan.ids
        self.assertEqual(ids["Note"]["section"], "RectElement")
        self.assertEqual(ids["Note"]["chapter"], "shapes")
        # Bikeshed's back matter is outside every chapter
        self.assertIsNone(ids["index"]["chapter"])

    def test_link_flags(self):
        links = self.scan.links
        toc = [l for l in links if l["toc"]]
        self.assertEqual([l["href"] for l in toc], ["#chapter-shapes"])
        self.assertTrue(any(l["selflink"] for l in links))
        idl = [l for l in links if l["idl"]]
        self.assertEqual([l["href"] for l in idl], ["#x"])

    def test_trace(self):
        self.assertEqual(self.scan.trace, {"0": "#RectElement", "1": "#Note", "2": "#Elsewhere"})

    def test_text_blocks_skip_decoration(self):
        texts = [t for c, t in self.scan.blocks if c == "shapes"]
        self.assertIn("Basic Shapes", texts)          # secno and self-link left out
        self.assertIn("Shapes use rect, near and far. It's fine.", texts)
        self.assertNotIn("Back matter text.", texts)

    def test_single_page_chapter_ids(self):
        p = self.tmp.join("single-page.html")
        helpers.write(p, OLD_SINGLE)
        self.assertEqual(measure.single_page_chapter_ids(p, "shapes"), {"shapes-Introduction", "shapes-Lost"})
        self.assertEqual(measure.single_page_chapter_ids(p, "nosuch"), set())


class MainTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = helpers.TempDir()
        out, old = cls.tmp.join("out"), cls.tmp.join("old")
        helpers.write(os.path.join(out, "index.html"), NEW_INDEX)
        helpers.write(os.path.join(out, "convert-report.json"), json.dumps({"pages": ["shapes"]}))
        helpers.write(os.path.join(out, "expected-ids.json"), json.dumps({"shapes": {
            "Introduction": {"new": "shapes-Introduction", "alias": None},
            "RectElement": {"new": "RectElement", "alias": "shapes-RectElement"},
        }}))
        rows = [dict(n=i, page="shapes", old_page="shapes", old_id="RectElement", form="explicit", kind="element",
                     name="rect", written_href="#RectElement") for i in range(3)]
        rows.append(dict(n=3, page="shapes", old_page="shapes", old_id="Note", form="explicit", kind="term",
                         name="note", written_href="#Note"))
        helpers.write(os.path.join(out, "trace-links.json"), json.dumps(rows))
        helpers.write(os.path.join(old, "shapes.html"), OLD_PAGE)
        helpers.write(os.path.join(old, "single-page.html"), OLD_SINGLE)
        report = cls.tmp.join("report.json")
        status, cls.stdout, err = helpers.run_script("measure.py", "--old-build", old, "--out", out,
                                                     "--report", report)
        assert status in (0, None), err
        cls.report = json.loads(helpers.read(report))
        cls.page = cls.report["pages"]["shapes"]

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_ids(self):
        self.assertEqual(self.page["old_page_ids_in_single_page_form"], ["Introduction"])
        self.assertEqual(self.page["old_page_ids_missing"], ["OnlyOld"])
        self.assertEqual(self.page["source_ids_missing"], [])
        self.assertEqual(self.page["source_ids_without_single_page_alias"], ["RectElement"])
        self.assertEqual(self.page["old_single_page_ids_missing"], ["shapes-Lost"])

    def test_link_counts(self):
        self.assertEqual(self.page["old_links"], {"prose": 3, "idl": 1})
        self.assertEqual(self.page["new_links"], {"prose": 3, "idl": 1})
        self.assertEqual(self.page["idl_link_texts_lost"], [])

    def test_text_blocks(self):
        self.assertEqual(self.page["text_blocks_only_old"], ["Gone."])

    def test_landing(self):
        got = sorted((l["result"], l["count"]) for l in self.report["landing"])
        # exact; a different id in the same section; another section; not in the output
        self.assertEqual(got, [("elsewhere", 1), ("exact", 1), ("lost", 1), ("section", 1)])
        self.assertEqual(sorted(p["result"] for p in self.report["landing_problems"]), ["elsewhere", "lost"])


if __name__ == "__main__":
    unittest.main()
