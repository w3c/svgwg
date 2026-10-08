"""Shared helpers for the tests: where things are, and how to load a script.

The scripts are not a package, and some have a hyphen in their file name
(check-preservation.py), so they are loaded from their path with importlib.
"""

import contextlib
import importlib.util
import io
import os
import shutil
import subprocess
import sys
import tempfile

TESTS = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.dirname(TESTS)                     # tools/bikeshed
ROOT = os.path.dirname(os.path.dirname(TOOLS))     # the svgwg checkout
FIXTURES = os.path.join(TESTS, "fixtures")

if TOOLS not in sys.path:
    sys.path.insert(0, TOOLS)  # convert.py imports svgdefs by name

_loaded = {}


def load(filename):
    """Load tools/bikeshed/<filename> as a module (once)."""
    if filename not in _loaded:
        name = "bikeshed_" + os.path.splitext(filename)[0].replace("-", "_")
        spec = importlib.util.spec_from_file_location(name, os.path.join(TOOLS, filename))
        mod = importlib.util.module_from_spec(spec)
        sys.modules[name] = mod
        spec.loader.exec_module(mod)
        _loaded[filename] = mod
    return _loaded[filename]


def fixture(*parts):
    return os.path.join(FIXTURES, *parts)


def read(path):
    with io.open(path, encoding="utf-8") as f:
        return f.read()


def write(path, text):
    d = os.path.dirname(path)
    if d:
        os.makedirs(d, exist_ok=True)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(text)


@contextlib.contextmanager
def quiet():
    """Swallow what a script prints, and give it back for inspection."""
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        yield out, err


def run_script(filename, *args, cwd=None):
    """Run a script in a child Python, the way build.sh does. Returns
    (exit status, stdout, stderr)."""
    p = subprocess.run([sys.executable, os.path.join(TOOLS, filename)] + list(args),
                       cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                       universal_newlines=True)
    return p.returncode, p.stdout, p.stderr


class TempDir(object):
    """A temporary folder, removed by cleanup()."""

    def __init__(self):
        self.path = tempfile.mkdtemp(prefix="bikeshed-test-")

    def join(self, *parts):
        return os.path.join(self.path, *parts)

    def cleanup(self):
        shutil.rmtree(self.path, ignore_errors=True)
