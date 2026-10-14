"""convert.py --source-mode and generate.py: the .bs source people edit,
and the build step that fills in its generated content.

The tiny source in fixtures/src/master is converted in source mode, then
generate.py puts it together again. The key test is that, with shorthands
off, the result is exactly what the plain converter writes: generate.py
then makes the same element summaries, lists and indexes from the .bs files
alone as convert.py made from the old source."""

import json
import os
import unittest

from . import helpers
from .test_convert import CONFIG, make_source, run_convert

convert = helpers.load("convert.py")
generate = helpers.load("generate.py")

SPLIT = helpers.fixture("config", "tiny-split.json")


def run_generate(root, src, out, extra=()):
    saved = convert.KEEP_STRAIGHT_APOSTROPHES[0], convert.SHORTHANDS[0]
    try:
        with helpers.quiet() as (stdout, _):
            status = generate.main(["--root", root, "--config", CONFIG, "--split-config", SPLIT,
                                    "--src", src, "--out", out] + list(extra))
    finally:
        convert.KEEP_STRAIGHT_APOSTROPHES[0], convert.SHORTHANDS[0] = saved
    return status, stdout.getvalue()


class SourceModeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = helpers.TempDir()
        cls.src = make_source(cls.tmp)
        cls.plain, _ = run_convert(cls.src, cls.tmp.join("plain"))
        cls.long_src, _ = run_convert(cls.src, cls.tmp.join("long"), extra=["--source-mode", "--no-shorthands"])
        cls.short_src, _ = run_convert(cls.src, cls.tmp.join("short"), extra=["--source-mode"])
        run_generate(cls.src, cls.tmp.join("long"), cls.tmp.join("gen-long"), ["--no-shorthands"])
        run_generate(cls.src, cls.tmp.join("short"), cls.tmp.join("gen-short"))

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_generated_index_is_the_plain_conversion(self):
        # One difference is intended: a file included from outside the
        # linked resource folders is named from the source folder, where
        # the .bs files live, not from the output folder.
        plain = self.plain["index.bs"].replace("path: ../src/master/examples/", "path: examples/")
        self.assertEqual(helpers.read(self.tmp.join("gen-long", "index.bs")), plain)

    def test_single_page_nav_is_the_same(self):
        got = json.loads(helpers.read(self.tmp.join("gen-long", "single-page-nav.json")))
        want = json.loads(self.plain["single-page-nav.json"])
        self.assertEqual(got, want)

    def test_placeholders_instead_of_generated_content(self):
        shapes = self.short_src["shapes.bs"]
        self.assertIn('<div data-svg-fill="element-summary" data-name="rect"></div>', shapes)
        self.assertIn('<span data-svg-fill="element-category" data-name="shape"></span>', shapes)
        self.assertNotIn("elementdef-rect", shapes)

    def test_pages_are_included_not_copied(self):
        index = self.short_src["index.bs"]
        self.assertIn("<pre class=include>path: shapes.bs</pre>", index)
        self.assertNotIn("Basic Shapes", index)

    def test_markup_shorthands_switched_on(self):
        self.assertIn("Markup Shorthands: css yes, dfn yes, markup yes, idl yes", self.short_src["index.bs"])

    def test_links_written_as_shorthands(self):
        shapes = self.short_src["shapes.bs"]
        for s in ("<{rect/rx}>", "<{circle}>", "'fill'", "{{SVGRectElement}}", "{{SVGRectElement/x}}"):
            self.assertIn(s, shapes)

    def test_href_links_keep_their_form(self):
        # links to other specs are not typed, so they stay as they are
        self.assertIn('<a href="https://drafts.csswg.org/filter-effects-1/#FilterProperty" class="property">filter</a>',
                      self.short_src["shapes.bs"])

    def test_generated_content_filled_in(self):
        index = helpers.read(self.tmp.join("gen-short", "index.bs"))
        self.assertNotIn("data-svg-fill", index)
        self.assertIn('id="elementdef-rect"', index)
        self.assertIn("<!-- page: shapes.bs -->", index)

    def test_page_list_must_match_split_config(self):
        bad = self.tmp.join("bad")
        os.makedirs(bad)
        helpers.write(os.path.join(bad, "index.bs"), "<pre class=include>path: shapes.bs</pre>\n")
        with self.assertRaises(SystemExit):
            run_generate(self.src, bad, self.tmp.join("gen-bad"))


class EscapeShorthandTests(unittest.TestCase):
    def test_quoted_word(self):
        self.assertEqual(convert.escape_shorthands("the value 'none' here"), "the value \\'none' here")

    def test_apostrophe_in_a_word_is_left_alone(self):
        self.assertEqual(convert.escape_shorthands("don't and path's end"), "don't and path's end")

    def test_double_apostrophe_runs(self):
        # once the first run is escaped, Bikeshed would read the closing
        # one as the start of another ''value'' link
        self.assertEqual(convert.escape_shorthands("''auto''"), "\\''auto\\''")

    def test_lone_dash(self):
        self.assertEqual(convert.escape_shorthands("'-'"), "'-'")

    def test_dfn_and_idl_openers(self):
        self.assertEqual(convert.escape_shorthands("[=x=] [$y$] {{z}} {{{w"), "\\[=x=] \\[$y$] \\{{z}} \\{{{w")

    def test_plain_brackets(self):
        self.assertEqual(convert.escape_shorthands("[0, 1] {a}"), "[0, 1] {a}")

    def test_esc_text_leaves_opaque_elements_alone(self):
        saved = convert.SHORTHANDS[0], convert.OPAQUE[0], convert.KEEP_STRAIGHT_APOSTROPHES[0]
        try:
            convert.SHORTHANDS[0], convert.KEEP_STRAIGHT_APOSTROPHES[0] = True, False
            self.assertEqual(convert.esc_text("'none'"), "\\'none'")
            convert.OPAQUE[0] = 1
            self.assertEqual(convert.esc_text("'none'"), "'none'")
        finally:
            convert.SHORTHANDS[0], convert.OPAQUE[0], convert.KEEP_STRAIGHT_APOSTROPHES[0] = saved


class ShorthandTests(unittest.TestCase):
    def sh(self, typed, extra=(), inner=None):
        return convert.Converter.shorthand(None, typed, list(extra), inner)

    def test_property(self):
        self.assertEqual(self.sh([("data-link-type", "property"), ("data-lt", "fill")], [("class", "property")], "fill"),
                         "'fill'")

    def test_dfn_with_other_text(self):
        self.assertEqual(self.sh([("data-link-type", "dfn"), ("data-lt", "invalid value")], (), "invalid"),
                         "[=invalid value|invalid=]")

    def test_element_attribute(self):
        self.assertEqual(self.sh([("data-link-type", "element-attr"), ("data-link-for", "rect"), ("data-lt", "rx")],
                                 (), "rx"), "<{rect/rx}>")

    def test_attribute_for_with_a_space_keeps_long_form(self):
        self.assertIsNone(self.sh([("data-link-type", "element-attr"),
                                   ("data-link-for", "conditional processing"), ("data-lt", "systemLanguage")],
                                  (), "systemLanguage"))

    def test_method(self):
        self.assertEqual(self.sh([("data-link-type", "method"), ("data-link-for", "SVGNumberList"),
                                  ("data-lt", "clear()")], (), "clear"), "{{SVGNumberList/clear()|clear}}")

    def test_interface_class_dropped(self):
        self.assertEqual(self.sh([("data-link-type", "interface"), ("data-lt", "SVGElement")],
                                 [("class", "idlinterface")], "SVGElement"), "{{SVGElement}}")

    def test_extra_attribute_keeps_long_form(self):
        self.assertIsNone(self.sh([("data-link-type", "dfn"), ("data-lt", "x")], [("title", "t")], "x"))

    def test_markup_in_text_keeps_long_form(self):
        self.assertIsNone(self.sh([("data-link-type", "dfn"), ("data-lt", "x")], (), "<code>x</code>"))


if __name__ == "__main__":
    unittest.main()
