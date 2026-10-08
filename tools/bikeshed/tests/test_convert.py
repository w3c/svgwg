"""convert.py: the SVG 2 source (XHTML with edit:* elements) to Bikeshed.

The converter runs on the tiny source in fixtures/src/master into a
temporary folder, and the tests look at the .bs text it writes."""

import io
import json
import os
import re
import shutil
import unittest

from . import helpers

convert = helpers.load("convert.py")

CONFIG = helpers.fixture("config", "tiny.json")
# The source has one link on the old filter effects host, which the config
# rewrites. The host is put in at run time so that no file in this folder
# carries the old address.
LEGACY_HOST = "https://drafts." + "fxtf.org/"


def make_source(tmp):
    src = tmp.join("src")
    shutil.copytree(helpers.fixture("src"), src)
    p = os.path.join(src, "master", "intro.html")
    helpers.write(p, helpers.read(p).replace("LEGACYFX/", LEGACY_HOST))
    return src


def run_convert(src, out, config=CONFIG, extra=()):
    saved = convert.KEEP_STRAIGHT_APOSTROPHES[0]
    try:
        with helpers.quiet() as (stdout, _):
            convert.main(["--source", src, "--config", config, "--out", out] + list(extra))
    finally:
        convert.KEEP_STRAIGHT_APOSTROPHES[0] = saved
    files = {}
    for fn in os.listdir(out):
        p = os.path.join(out, fn)
        if os.path.isfile(p):
            files[fn] = helpers.read(p)
    return files, stdout.getvalue()


class ConvertTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = helpers.TempDir()
        cls.src = make_source(cls.tmp)
        cls.out = cls.tmp.join("out")
        cls.files, cls.stdout = run_convert(cls.src, cls.out)
        cls.intro = cls.files["intro.bs"]
        cls.shapes = cls.files["shapes.bs"]
        cls.index = cls.files["index.bs"]

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    # -- files and page markers ----------------------------------------------

    def test_files_written(self):
        for fn in ("intro.bs", "shapes.bs", "idl.bs", "eltindex.bs", "index.bs",
                   "single-page-nav.json", "trace-links.json", "expected-ids.json",
                   "convert-report.json"):
            self.assertIn(fn, self.files)
        self.assertNotIn("Overview.bs", self.files)  # skip_pages

    def test_page_markers(self):
        self.assertTrue(self.intro.startswith('<h2 id="chapter-intro" data-bs-page="intro">Introduction</h2>'))
        self.assertIn('<h2 id="chapter-shapes" data-bs-page="shapes">Basic Shapes</h2>', self.shapes)
        # appendices get their letter in the title
        self.assertIn('<h2 id="chapter-idl" data-bs-page="idl">Appendix A: IDL Definitions</h2>',
                      self.files["idl.bs"])
        self.assertIn('data-bs-page="eltindex">Appendix B: Element Index</h2>', self.files["eltindex.bs"])

    def test_pages_inlined_in_publish_order(self):
        marks = re.findall(r"<!-- page: (\S+)\.bs -->", self.index)
        self.assertEqual(marks, ["intro", "shapes", "idl", "eltindex"])
        self.assertIn(self.intro.strip(), self.index)

    def test_headings_move_down_one_level(self):
        self.assertIn('<h3 id="RectElement"', self.shapes)
        self.assertIn('<h4 id="InterfaceSVGRectElement"', self.shapes)
        self.assertNotIn("<h1", self.shapes)

    # -- ids --------------------------------------------------------------------

    def test_clashing_id_gets_page_prefix_and_multipage_id(self):
        # "Introduction" is on two pages
        self.assertIn('<h3 id="intro-Introduction" data-multipage-id="Introduction">About</h3>', self.intro)
        self.assertIn('<h3 id="shapes-Introduction" data-multipage-id="Introduction">', self.shapes)

    def test_heading_and_dfn_keep_single_page_id_as_oldids(self):
        self.assertIn('<h3 id="RectElement" oldids="shapes-RectElement">', self.shapes)
        self.assertIn('id="TermUserAgent" data-dfn-type="dfn" data-noexport="" oldids="intro-TermUserAgent"',
                      self.intro)
        # examples and issues also take oldids
        self.assertIn('<div class="example" id="ExampleOne" oldids="intro-ExampleOne">', self.intro)

    def test_other_elements_get_alias_span(self):
        self.assertIn('<p id="AboutPara"><span id="intro-AboutPara" class="bs-old-id"></span>The', self.intro)

    def test_expected_ids(self):
        ids = json.loads(self.files["expected-ids.json"])
        self.assertEqual(ids["shapes"]["Introduction"], {"alias": None, "new": "shapes-Introduction"})
        self.assertEqual(ids["shapes"]["RectElement"], {"alias": "shapes-RectElement", "new": "RectElement"})
        self.assertTrue(ids["shapes"]["elementdef-rect"]["generated"])

    # -- links ------------------------------------------------------------------

    def test_typed_element_link(self):
        self.assertIn('<span class="element-name">‘<a data-link-type="element" data-lt="rect">rect</a>’</span>',
                      self.intro)

    def test_typed_dfn_link(self):
        self.assertIn('<a data-link-type="dfn" data-lt="user agent">user agent</a>', self.intro)

    def test_typed_attribute_link_with_for(self):
        self.assertIn('<a data-link-type="element-attr" data-link-for="rect" data-lt="rx">rx</a>', self.shapes)

    def test_typed_property_and_interface_links(self):
        self.assertIn('<a data-link-type="property" data-lt="fill" class="property">fill</a>', self.shapes)
        self.assertIn('<a data-link-type="interface" data-lt="SVGRectElement" class="idlinterface">', self.shapes)
        self.assertIn('<a data-link-type="attribute" data-link-for="SVGRectElement" data-lt="x">x</a>', self.shapes)

    def test_explicit_href_when_no_definition_to_land_on(self):
        # no dfn carries RectElementXAttribute: the link keeps its target
        self.assertIn('<a href="#RectElementXAttribute" data-link-type="element-attr">x</a>', self.shapes)
        self.assertIn('<a href="#DataTypeLength">&lt;length></a>', self.intro)

    def test_href_links_look_like_typed_links(self):
        # Bikeshed shows typed element and attribute links in code font by
        # their data-link-type; href links of the same kind get it too.
        self.assertIn('<span class="element-name">‘<a href="#DescElement" data-link-type="element">desc</a>’</span>',
                      self.shapes)
        self.assertIn('<a href="#PathLengthAttribute" data-link-type="element-attr">pathLength</a>', self.shapes)
        # other kinds are left alone
        self.assertIn('<a href="#TermCoreAttribute">core attributes</a>', self.shapes)
        self.assertIn('<a href="#XProperty" class="property">x</a>', self.shapes)
        # a typed link keeps its own data-link-type, only once
        self.assertNotIn('data-link-type="element-attr" data-link-for="rect" data-lt="rx" data-link-type', self.shapes)

    def test_external_definition_link(self):
        self.assertIn('<a href="https://drafts.csswg.org/filter-effects-1/#FilterProperty" class="property">filter</a>',
                      self.shapes)

    def test_term_markup_kept(self):
        self.assertIn('<a href="#TermCTM"><abbr title="current transformation matrix">CTM</abbr></a>', self.intro)

    def test_unresolved_link_stays_visible(self):
        self.assertIn('<span class="xxx">@@ unknown element, attribute or property "nosuchthing"</span>', self.intro)
        self.assertIn('<span class="xxx">@@ ambiguous name "dup" (matches multiple attributes)</span>', self.intro)
        self.assertIn('warning: intro.html: ambiguous name "dup"', self.stdout)

    def test_handwritten_links(self):
        self.assertIn('<a href="#RectElement">hand-written link</a>', self.intro)
        # [SPECID] links resolved against the definitions base
        self.assertIn('<a href="https://drafts.csswg.org/filter-effects-1/#FilterProperty">spec-relative link</a>',
                      self.intro)

    def test_host_rewrite(self):
        self.assertIn('<a href="https://drafts.csswg.org/filter-effects-1/#FilterProperty">old host link</a>',
                      self.intro)
        self.assertNotIn("fxtf", self.intro)

    # -- edit:* elements ----------------------------------------------------------

    def test_edit_with_becomes_link_for_hint(self):
        self.assertIn('<div link-for-hint="script">\n<p>Inside a script:', self.intro)
        # inside the hint, 'type' is the script element's attribute
        self.assertIn('<a href="#ScriptElementTypeAttribute" data-link-type="element-attr">type</a>', self.intro)
        # an edit:with holding a heading leaves no wrapper
        self.assertNotIn('link-for-hint="rect"', self.shapes)

    def test_element_summary(self):
        s = self.shapes
        self.assertIn('<div class="def element-summary"><div class="element-summary-name"><span class="element-name">'
                      '‘<dfn data-dfn-type="element" data-export="" id="elementdef-rect" '
                      'oldids="shapes-elementdef-rect">rect</dfn>’</span></div>', s)
        summary = s[s.index('id="elementdef-rect"'):s.index('id="elementdef-rect"') + 3000]
        summary = summary[:summary.index("</div>", summary.index("DOM Interfaces"))]
        self.assertIn('<dt>Categories:</dt><dd><a data-link-type="dfn" data-lt="shape elements">Shape element</a></dd>',
                      summary)
        self.assertIn("Any number of the following elements, in any order:", summary)
        self.assertIn('<a href="#TermDescriptiveElement">descriptive elements</a>', summary)
        self.assertIn('<a href="#TermCoreAttribute">core attributes</a>', summary)
        self.assertIn('<dt>Geometry properties:</dt>', summary)
        self.assertIn('<a href="#XProperty" class="property">x</a>', summary)
        self.assertIn('data-lt="SVGRectElement" class="idlinterface">SVGRectElement</a>', summary)

    def test_element_category_list(self):
        self.assertIn('Specifically: <span class="element-name">‘<a data-link-type="element" data-lt="circle">circle</a>’'
                      '</span> and <span class="element-name">‘<a data-link-type="element" data-lt="rect">rect</a>’</span>.',
                      self.shapes)

    def test_attribute_category_list(self):
        self.assertIn('Core attributes are <span class="attr-name">‘<a href="#IDAttribute" data-link-type="element-attr">id</a>’'
                      '</span>, <span class="attr-name">‘<a href="#ClassAttribute" data-link-type="element-attr">class</a>’'
                      '</span> and <span class="attr-name">‘<a href="#CoreDupAttribute" data-link-type="element-attr">dup</a>’'
                      '</span>.', self.intro)

    def test_elements_with_attribute_category(self):
        self.assertIn('Elements with core attributes: <span class="element-name">'
                      '<a data-link-type="element" data-lt="circle">circle</a></span>, ', self.files["eltindex.bs"])

    def test_attribute_table(self):
        t = self.files["eltindex.bs"]
        self.assertIn('<table class="proptable attrtable"><thead><tr><th>Attribute</th>', t)
        self.assertIn('<th title="Animatable"><a href="#TermAnimatable">Anim.</a></th>', t)
        rows = re.findall(r'<tr><th><span class="attr-name"><a [^>]*>([^<]+)</a></span></th><td>(.*?)</td><td>(.*?)</td></tr>', t)
        self.assertEqual([r[0] for r in rows], ["class", "dup", "dup", "id", "lone", "pathLength", "rx", "type", "x"])
        rx = [r for r in rows if r[0] == "rx"][0]
        self.assertIn(">rect</a>", rx[1])
        self.assertEqual(rx[2], "✓")
        lone = [r for r in rows if r[0] == "lone"][0]
        self.assertEqual(lone[2], "")

    def test_element_index(self):
        self.assertIn('<ul class="element-index"><li><span class="element-name">‘<a data-link-type="element" '
                      'data-lt="circle">circle</a>’</span></li>', self.files["eltindex.bs"])

    def test_example(self):
        self.assertIn('<div class="example"><pre class="include-code xml">path: images/shapes/rect01.svg</pre>'
                      '<div class="figure"><img alt="Example rect01 \u2014 a plain rect" src="images/shapes/rect01.png">'
                      '<p class="caption">Example rect01</p></div><p class="view-as-svg">'
                      '<a href="images/shapes/rect01.svg">View this example as SVG (SVG-enabled browsers only)</a>'
                      '</p></div>', self.shapes)

    def test_includefile_path_relative_to_output(self):
        m = re.search(r'<pre class="include-code">path: ([^<]+)</pre>', self.shapes)
        self.assertIsNotNone(m)
        self.assertEqual(os.path.normpath(os.path.join(self.out, m.group(1))),
                         os.path.normpath(os.path.join(self.src, "master", "examples", "rect.txt")))

    def test_unknown_edit_element_warns(self):
        self.assertIn("warning: eltindex.html: edit:nosuchelement not converted", self.stdout)

    # -- IDL ------------------------------------------------------------------------

    def test_idl_block_is_plain_text(self):
        self.assertIn('<pre class="idl">[Exposed=Window]\ninterface SVGRectElement : SVGElement {\n'
                      '  readonly attribute long x;\n', self.shapes)

    def test_ids_inside_idl_kept_before_block(self):
        self.assertIn('<span id="RectIdlName" class="bs-old-id"></span><span id="shapes-RectIdlName" '
                      'class="bs-old-id"></span><pre class="idl">', self.shapes)

    def test_idl_member_prose_becomes_dfn(self):
        self.assertIn('<dfn id="__svg__SVGRectElement__x" data-dfn-type="attribute" data-dfn-for="SVGRectElement" '
                      'data-lt="x" oldids="shapes-__svg__SVGRectElement__x">x</dfn>', self.shapes)
        self.assertIn('data-dfn-type="method" data-dfn-for="SVGRectElement" data-lt="frob(count, label)"', self.shapes)

    def test_excludefromidl_gets_class_extract(self):
        self.assertIn('<pre class="idl extract">dictionary TinyDict {', self.shapes)

    def test_complete_idl(self):
        self.assertIn('<span id="idl-RectIdlName" class="bs-old-id"></span><div data-fill-with="idl-index"></div>',
                      self.files["idl.bs"])

    # -- dfns -------------------------------------------------------------------------

    def test_dfn_types_written_out(self):
        self.assertIn('<dfn id="RectElementRXAttribute" data-dfn-type="element-attr" data-dfn-for="rect"', self.shapes)
        self.assertIn('<dfn id="FillProperty" data-dfn-type="property"', self.shapes)

    def test_duplicate_dfn_gets_distinct_linking_text(self):
        # "thing" is defined in intro and again in shapes: the later one is renamed
        self.assertIn('<dfn id="TermThing" data-dfn-type="dfn" data-noexport="" oldids="intro-TermThing">thing</dfn>',
                      self.intro)
        self.assertIn('<dfn id="ThingAgain" data-dfn-type="dfn" data-noexport="" data-lt="thing (ThingAgain)"',
                      self.shapes)
        report = json.loads(self.files["convert-report.json"])
        self.assertEqual(report["duplicate_dfns"],
                         [{"fors": [], "text": "thing", "type": "dfn", "where": ["intro#TermThing", "shapes#ThingAgain"]}])

    def test_class_rename(self):
        self.assertIn('<table class="svg-propdef">', self.shapes)

    # -- text -------------------------------------------------------------------------

    def test_straight_apostrophe_kept_by_default(self):
        self.assertIn("Don&#39;t panic", self.intro)

    def test_text_macro_escaped(self):
        self.assertIn("A &#91;FOO] stays text.", self.intro)

    # -- index.bs -----------------------------------------------------------------------

    def test_metadata(self):
        md = self.index[self.index.index("<pre class=metadata>"):self.index.index("</pre>")]
        self.assertIn("Title: Tiny SVG\n", md)
        self.assertIn("Shortname: tiny\n", md)
        self.assertIn("Status: ED\n", md)
        self.assertIn("ED: https://w3c.github.io/svgwg/svg2-draft/\n", md)
        self.assertIn("Editor: Ada Lovelace, Example Org, ada@example.org, w3cid 123\n", md)
        self.assertIn("Former Editor: Charles Babbage, Engine Works, cb@example.org\n", md)
        self.assertIn("Abstract: This is a tiny specification.\n", md)

    def test_anchors_block_from_config(self):
        self.assertIn("<pre class=anchors>\nurl: https://dom.spec.whatwg.org/#interface-element; spec: DOM; "
                      "type: interface; text: Element\n</pre>", self.index)

    def test_extra_css_and_body_end(self):
        self.assertIn("<style>\n.tiny { color: red; }\n</style>", self.index)
        self.assertTrue(self.index.rstrip().endswith('<script src="style/expanders.js"></script>'))

    def test_single_page_nav_json(self):
        nav = json.loads(self.files["single-page-nav.json"])
        self.assertEqual(nav["pages"], ["intro", "shapes", "idl", "eltindex"])
        self.assertEqual(nav["index"], ["Overview"])
        self.assertEqual(nav["elements"], "eltindex")
        self.assertIsNone(nav["attributes"])
        self.assertEqual(nav["appendix_letters"], {"idl": "A", "eltindex": "B"})
        self.assertEqual(nav["drop_headings"], ["idl-index"])

    def test_resource_folders_linked(self):
        self.assertTrue(os.path.islink(os.path.join(self.out, "images")))


class ConvertVariantTests(unittest.TestCase):
    """Second run: curly apostrophes allowed, the front page as Bikeshed's
    header.include, and only one page built."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = helpers.TempDir()
        cls.src = make_source(cls.tmp)
        with io.open(CONFIG, encoding="utf-8") as f:
            cfg = json.load(f)
        cfg["keep_straight_apostrophes"] = False
        cfg["front_matter"] = "header_include"
        cfg["head_html"] = ['<meta charset="utf-8">']
        cfg_path = cls.tmp.join("variant.json")
        helpers.write(cfg_path, json.dumps(cfg))
        cls.files, _ = run_convert(cls.src, cls.tmp.join("out"), cfg_path, ["--pages", "intro", "--trace-links"])

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_apostrophe_left_for_bikeshed(self):
        self.assertIn("Don't panic", self.files["intro.bs"])

    def test_only_requested_pages(self):
        self.assertIn("intro.bs", self.files)
        self.assertNotIn("shapes.bs", self.files)

    def test_links_to_pages_not_built_are_absolute(self):
        intro = self.files["intro.bs"]
        self.assertIn('<a href="https://w3c.github.io/svgwg/svg2-draft/shapes.html#RectElement" data-svgtrace=',
                      intro)
        # not typed: no Bikeshed autolink (data-lt), only the styling attribute
        self.assertNotIn('data-link-type="element" data-lt=', intro)

    def test_trace_links(self):
        rows = json.loads(self.files["trace-links.json"])
        self.assertTrue(rows)
        first = rows[0]
        self.assertEqual((first["page"], first["old_page"], first["old_id"]), ("intro", "intro", "TermUserAgent"))
        self.assertEqual(first["form"], "typed-exact")
        self.assertIn('data-svgtrace="0"', self.files["intro.bs"])

    def test_header_include(self):
        h = self.files["header.include"]
        self.assertTrue(h.startswith('<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n</head>\n'
                                     '<body class="h-entry">\n'))
        self.assertIn("Editor’s Draft, [DATE]", h)
        # today's toc heading id kept next to Bikeshed's table of contents
        self.assertIn('<nav data-fill-with="table-of-contents" id="toc"><span class="bs-old-id" id="fulltoc"></span>'
                      '<span class="bs-old-id" id="Overview-fulltoc"></span></nav>', h)
        self.assertIn('<span class="bs-old-id" id="chapter-Overview"></span>', h)
        self.assertTrue(h.rstrip().endswith("<main>"))
        self.assertNotIn("Acknowledgments", h)

    def test_front_page_rest_goes_into_index(self):
        idx = self.files["index.bs"]
        self.assertIn("Local Boilerplate: header yes", idx)
        self.assertIn("Canonical URL: https://www.w3.org/TR/SVG2/", idx)
        self.assertIn("<!-- front page, after the table of contents (Overview.html) -->", idx)
        # front page headings stay out of the numbering and the toc
        self.assertIn('<h2 id="Acknowledgments" class="no-num no-toc" oldids="Overview-Acknowledgments">', idx)
        self.assertLess(idx.index("Acknowledgments"), idx.index("<!-- page: intro.bs -->"))


class EscapeTests(unittest.TestCase):
    def test_esc_text(self):
        self.assertEqual(convert.esc_text("a < b & c"), "a &lt; b &amp; c")

    def test_line_ending_em_dash_gets_a_space(self):
        self.assertEqual(convert.esc_text("one\u2014\ntwo"), "one\u2014 \ntwo")

    def test_esc_attr(self):
        self.assertEqual(convert.esc_attr('say "hi" [FOO]'), "say &quot;hi&quot; &#91;FOO]")


class IdlScannerTests(unittest.TestCase):
    def test_idl_members(self):
        text = ("interface A : B {\n  const short C = 1;\n  readonly attribute long x;\n"
                "  undefined f(long a, optional DOMString b = \"\");\n  setter undefined (unsigned long i, long v);\n};\n"
                "dictionary D { long size = 0; };")
        got = [(m["iface"], m["name"], m["kind"], m["args"]) for m in convert.idl_members(text)]
        self.assertEqual(got, [("A", "C", "const", None), ("A", "x", "attribute", None),
                               ("A", "f", "method", ["a", "b"]), ("D", "size", "dict-member", None)])

    def test_comments_ignored(self):
        got = [m["name"] for m in convert.idl_members("interface A { /* attribute long no; */ attribute long yes; };")]
        self.assertEqual(got, ["yes"])


if __name__ == "__main__":
    unittest.main()
