"""End to end: build.sh on the real master/, then check.sh against the
current build in build/publish.

Skipped unless SVG_BIKESHED_E2E=1 is set, because it needs Bikeshed (the
one in $BIKESHED, else bikeshed on PATH), a current build in build/publish
(made by `make`, which needs Node.js), and takes about 15 seconds. Run it with:

    SVG_BIKESHED_E2E=1 python3 -m unittest discover -s tools/bikeshed/tests -t tools/bikeshed

check.sh writes its baseline and losses.tsv into build/bikeshed/, as it
does when run by hand; the Bikeshed build itself goes to a temporary folder.
"""

import os
import shutil
import subprocess
import unittest

from . import helpers

ENABLED = os.environ.get("SVG_BIKESHED_E2E") == "1"
BIKESHED = os.environ.get("BIKESHED") or shutil.which("bikeshed")
OLD = os.path.join(helpers.ROOT, "build", "publish")


@unittest.skipUnless(ENABLED, "set SVG_BIKESHED_E2E=1 to run the end-to-end build")
class EndToEndTests(unittest.TestCase):
    def setUp(self):
        if not BIKESHED or not (os.path.isfile(BIKESHED) or shutil.which(BIKESHED)):
            self.skipTest("Bikeshed not found ($BIKESHED or bikeshed on PATH)")
        if not os.path.isfile(os.path.join(OLD, "single-page.html")):
            self.skipTest("no current build in build/publish: run make first")
        self.tmp = helpers.TempDir()

    def tearDown(self):
        self.tmp.cleanup()

    def run_sh(self, *args):
        env = dict(os.environ, BIKESHED=BIKESHED)
        p = subprocess.run(list(args), cwd=helpers.ROOT, env=env, stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT, universal_newlines=True)
        return p.returncode, p.stdout

    def test_build_and_check(self):
        status, out = self.run_sh(os.path.join(helpers.TOOLS, "build.sh"), self.tmp.path)
        self.assertEqual(status, 0, out[-3000:])
        site = self.tmp.join("svg2-draft")
        for fn in ("index.html", "single-page.html", "shapes.html", "fragment-links.json"):
            self.assertTrue(os.path.isfile(os.path.join(site, fn)), fn)
        status, out = self.run_sh(os.path.join(helpers.TOOLS, "check.sh"), OLD, site)
        self.assertEqual(status, 0, out[-3000:])
        self.assertIn("TOTAL LOSSES: 0", out)


if __name__ == "__main__":
    unittest.main()
