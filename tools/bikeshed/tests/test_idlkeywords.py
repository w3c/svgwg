"""idlkeywords.py: link the IDL keywords Bikeshed leaves as plain text."""

import json
import os
import unittest

from . import helpers

idlkeywords = helpers.load("idlkeywords.py")

LINKS = {"setter": "__svg__SVGNameList__setter"}

PAGE = """<html><body>
<p>Prose mentions <c- b>setter</c-> too.</p>
<pre class="idl highlight def">interface <dfn>SVGNameList</dfn> {
  <c- b>setter</c-> <c- b>undefined</c-> (<c- b>unsigned</c-> <c- b>long</c-> <c- g>index</c->);
  <a href="#x"><c- b>setter</c-></a> again;
};</pre>
<p id="__svg__SVGNameList__setter">The setter.</p>
</body></html>
"""


class LinkKeywordsTests(unittest.TestCase):
    def test_wraps_keyword(self):
        out, n = idlkeywords.link_keywords("a <c- b>setter</c-> b", LINKS)
        self.assertEqual(n, 1)
        self.assertEqual(out, 'a <a href="#__svg__SVGNameList__setter"><c- b>setter</c-></a> b')

    def test_skips_keyword_already_in_a_link(self):
        block = '<a href="#x"><c- b>setter</c-></a>'
        out, n = idlkeywords.link_keywords(block, LINKS)
        self.assertEqual((out, n), (block, 0))

    def test_other_keywords_left_alone(self):
        block = "<c- b>getter</c-> <c- b>setterish</c->"
        self.assertEqual(idlkeywords.link_keywords(block, LINKS), (block, 0))


class MainTests(unittest.TestCase):
    def setUp(self):
        self.tmp = helpers.TempDir()
        self.index = self.tmp.join("index.html")

    def tearDown(self):
        self.tmp.cleanup()

    def config(self, data):
        p = self.tmp.join("config.json")
        helpers.write(p, json.dumps(data))
        return p

    def run_main(self, cfg):
        with helpers.quiet() as (out, err):
            status = idlkeywords.main(["idlkeywords.py", self.tmp.path, "--config", cfg])
        return status, out.getvalue(), err.getvalue()

    def test_only_inside_idl_blocks(self):
        helpers.write(self.index, PAGE)
        status, out, _ = self.run_main(self.config({"idl_keyword_links": LINKS}))
        self.assertEqual(status, 0)
        doc = helpers.read(self.index)
        self.assertIn("<p>Prose mentions <c- b>setter</c-> too.</p>", doc)
        self.assertIn('  <a href="#__svg__SVGNameList__setter"><c- b>setter</c-></a> <c- b>undefined</c->', doc)
        self.assertEqual(doc.count('href="#__svg__SVGNameList__setter"'), 1)
        self.assertIn("1 IDL keywords linked", out)

    def test_missing_target_id_is_an_error(self):
        page = PAGE.replace(' id="__svg__SVGNameList__setter"', "")
        helpers.write(self.index, page)
        status, _, err = self.run_main(self.config({"idl_keyword_links": LINKS}))
        self.assertEqual(status, 1)
        self.assertIn("target id not in index.html: __svg__SVGNameList__setter", err)
        self.assertEqual(helpers.read(self.index), page)

    def test_no_config_entry_does_nothing(self):
        status, out, _ = self.run_main(self.config({}))
        self.assertEqual(status, 0)
        self.assertIn("nothing to do", out)
        self.assertFalse(os.path.exists(self.index))


if __name__ == "__main__":
    unittest.main()
