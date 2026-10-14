"""buildlog.py: Bikeshed's messages grouped into categories, per page file."""

import json
import os
import unittest

from . import helpers

buildlog = helpers.load("buildlog.py")

RED, RESET = "\x1b[31;1m", "\x1b[0m"

INDEX_BS = "\n".join([
    "<pre class=metadata>",       # 1
    "Title: Tiny",                # 2
    "</pre>",                     # 3
    "<!-- page: intro.bs -->",    # 4
    "<h2>Intro</h2>",             # 5
    "<p>text</p>",                # 6
    "<!-- page: shapes.bs -->",   # 7
    "<h2>Shapes</h2>",            # 8
    "<p>more</p>",                # 9
]) + "\n"

LOG = "\n".join([
    # Bikeshed writes "LINE n:" in place of the severity when it knows the line
    RED + "LINE 6:" + RESET + " No 'dfn' refs found for 'frobnicate'.",
    "<a data-link-type=dfn>frobnicate</a>",
    "LINE ~9:2: Multiple possible 'element-attr' local refs for 'x'.",
    "  indented continuation line",
    "Add a 'for' attribute to one of them.",
    "LINE 2 of file 'other.bs': Multiple elements have the same ID 'Introduction'.",
    "LINT: The var 'q' (in algorithm 'x') is only used once.",
    "WARNING: Something completely 'new' happened.",
    "",
    "Successfully generated, with 4 warnings",
]) + "\n"


class CategoriseTests(unittest.TestCase):
    def test_known_shapes(self):
        c = buildlog.categorise
        self.assertEqual(c("No 'dfn' refs found for 'x'."), "link error: no dfn dfn found")
        self.assertEqual(c("Multiple possible 'element-attr' local refs for 'x'."),
                         "link error: several element-attr dfns match")
        self.assertEqual(c("Multiple local 'dfn' <dfn>s have the same linking text 'x'."), "duplicate dfn: dfn")
        self.assertEqual(c("Multiple elements have the same ID 'a'."), "duplicate id")
        self.assertEqual(c("The var 'q' is only used once."), "lint: var used only once")
        self.assertEqual(c("Found unmatched text macro [FOO]."), "text macro")

    def test_unknown_message_keeps_its_shape(self):
        self.assertEqual(buildlog.categorise("Something 'odd' at 'here'"), "other: Something '…' at '…'")


class ParseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = helpers.TempDir()
        cls.log = cls.tmp.join("build.log")
        helpers.write(cls.log, LOG)
        helpers.write(cls.tmp.join("index.bs"), INDEX_BS)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_page_map(self):
        self.assertEqual(buildlog.page_map(self.tmp.join("index.bs")), [(4, "intro.bs"), (7, "shapes.bs")])
        self.assertEqual(buildlog.page_map(self.tmp.join("missing.bs")), [])

    def test_parse_maps_lines_to_page_files(self):
        rows = buildlog.parse(self.log, self.tmp.join("index.bs"))
        got = [(r["file"], r["line"], r["category"]) for r in rows]
        self.assertEqual(got, [
            ("intro.bs", "2", "link error: no dfn dfn found"),
            ("shapes.bs", "2", "link error: several element-attr dfns match"),
            ("other.bs", "2", "duplicate id"),
            ("-", "", "lint: var used only once"),
            ("-", "", "other: Something completely '…' happened."),
        ])
        # colours and the severity word are gone from the message
        self.assertEqual(rows[0]["message"], "No 'dfn' refs found for 'frobnicate'.")

    def test_parse_without_index(self):
        rows = buildlog.parse(self.log)
        self.assertEqual(rows[0]["file"], "index.bs")
        self.assertEqual(rows[0]["line"], "6")

    def test_command_line(self):
        out_json = self.tmp.join("rows.json")
        status, stdout, _ = helpers.run_script("buildlog.py", self.log, "--json", out_json)
        self.assertEqual(status, 0)
        self.assertRegex(stdout, r"TOTAL\s+5\n")
        self.assertEqual(len(json.loads(helpers.read(out_json))), 5)
        self.assertTrue(os.path.isfile(out_json))


if __name__ == "__main__":
    unittest.main()
