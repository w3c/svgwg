"""build.sh stops early when Bikeshed is missing or older than 7.2.0.

Fake bikeshed programs that only print a version stand in for the real
one, so these tests need neither Bikeshed nor a build."""

import os
import stat
import subprocess
import unittest

from . import helpers


class BikeshedVersionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = helpers.TempDir()

    def tearDown(self):
        self.tmp.cleanup()

    def fake(self, version):
        p = self.tmp.join("bikeshed-" + version)
        helpers.write(p, "#!/bin/sh\necho %s\n" % version)
        os.chmod(p, os.stat(p).st_mode | stat.S_IEXEC)
        return p

    def build(self, bikeshed):
        env = dict(os.environ, BIKESHED=bikeshed)
        p = subprocess.run([os.path.join(helpers.TOOLS, "build.sh"), self.tmp.join("out")], env=env,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        return p.returncode, p.stdout, p.stderr

    def test_too_old(self):
        status, out, err = self.build(self.fake("7.1.3"))
        self.assertEqual(status, 1)
        self.assertIn("Bikeshed 7.1.3 is too old, 7.2.0 or later is needed", err)
        self.assertNotIn("1/4", out)   # stopped before building anything

    def test_missing(self):
        status, out, err = self.build(self.tmp.join("no-such-bikeshed"))
        self.assertEqual(status, 1)
        self.assertIn("Bikeshed not found", err)

    def test_recent_enough_goes_on(self):
        # 7.10.0 is newer than 7.2.0: numbers are compared, not text.
        # The fake cannot build, so the build fails later, at Bikeshed.
        status, out, err = self.build(self.fake("7.10.0"))
        self.assertIn("1/4", out)
        self.assertNotIn("too old", err)


if __name__ == "__main__":
    unittest.main()
