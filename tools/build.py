#!/usr/bin/env python

# -c == clean
# -s == stabilize issues
# -L == list external links
# -l == lint


# Note that we have to change directory below to make sure that build output
# goes in the 'build' directory, not in the 'master' directory. For that
# reason it's important that we use absolute paths!

'''
'''

import commands, os, sys, signal, time
from os.path import isfile, abspath, getmtime, exists, join, normpath
from xml.dom import minidom
import shutil

def exit(code, *message):
  if len(message):
    if code == 0:
      print message[0]
    else:
      sys.stderr.write(message[0] + '\n')
  sys.exit(code)

def native_path(s):
  if exists("/usr/bin/cygpath.exe"):
    return commands.getoutput("cygpath -a -w %s" % s)
  return s

# Multiplatform alternative to commands.getstatusoutput from
# http://stackoverflow.com/questions/1193583/what-is-the-multiplatform-alternative-to-subprocess-getstatusoutput-older-comma
def getstatusoutput(cmd): 
  """Return (status, output) of executing cmd in a shell."""
  """This new implementation should work on all platforms."""
  import subprocess
  pipe = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True,
                          universal_newlines=True)  
  output = "".join(pipe.stdout.readlines()) 
  sts = pipe.wait()
  if sts is None: sts = 0
  return sts, output

def getstatus(cmd):
    status, output = getstatusoutput(cmd)
    return status

def which(name, flags=os.X_OK):
    """ which that works on Windows too.
    
    Based on http://twistedmatrix.com/trac/browser/tags/releases/twisted-8.2.0/twisted/python/procutils.py
    """
    result = []
    exts = filter(None, os.environ.get('PATHEXT', '').split(os.pathsep))
    path = os.environ.get('PATH', None)
    if path is None:
        return []
    for p in os.environ.get('PATH', '').split(os.pathsep):
        p = os.path.join(p, name)
        if os.access(p, flags):
            result.append(p)
        for e in exts:
            pext = p + e
            if os.access(pext, flags):
                result.append(pext)
    return result

# could allow this to be passed in:
repo_dir = os.getcwd()

master_dir = join(repo_dir, 'master')
build_dir = join(repo_dir, 'build')
publish_dir = join(build_dir, 'publish')
tools_dir = join(repo_dir, 'tools')

if not exists(master_dir):
  exit(1, 'FAIL: build.py must be run from the root of the \'svg2\' repository '
          'or from one of the directories under \'specs/\'.')

if not exists(tools_dir):
  tools_dir = normpath(join(repo_dir, '..', '..', 'tools'))
  if not exists(tools_dir):
    exit(1, 'FAIL: could not find \'tools\' directory')

publishjs_dir = join(tools_dir, 'publish')

if not exists(publish_dir):
  assert os.pardir not in publish_dir
  os.makedirs(publish_dir)

# Add clean-up handler for SIGINT:

def handle_SIGINT(signal, frame):
  done()
  sys.exit(1)

signal.signal(signal.SIGINT, handle_SIGINT)

# Utility functions:

toremove = []

def done():
  global toremove
  if toremove:
    print "* error, removing " + " ".join(toremove)
    for file in toremove:
      os.remove(file)
    return 1

built_something = False

def run(cmd):
  global built_something
  # print cmd
  if os.system(cmd):
    done()
    sys.exit(1)
  built_something = True

# clean and exit if given -c option:

if len(sys.argv) == 2 and sys.argv[1] == "-c":
  # clean build (and publish) directory
  readme = join(build_dir, 'README.txt')
  for parent, dirs, files in os.walk(build_dir, topdown=False):
    for file in files[:]:
      file = join(parent, file)
      if file != readme:
        os.remove(file)
    for dir in dirs[:]:
      os.rmdir(join(parent, dir))
  sys.exit(0)

# See if we should call "node" or "nodejs":

if which("nodejs") != []:
    node = "nodejs"
elif which("node") != []:
    node = "node"
elif getstatus("[ -e /home/svgwg/bin/node ]") == 0:
    node = "/home/svgwg/bin/node"
else:
    exit(1, 'FAIL: could not find "nodejs" or "node" on the PATH')
  
if len(sys.argv) == 2 and (sys.argv[1] == "-L" or sys.argv[1] == "-l"):
  # list links or lint
  arg = "--list-external-links" if sys.argv[1] == "-L" else "--lint"
  os.chdir(master_dir)
  run(node + " \"" +
      native_path(join(tools_dir, join("publish","publish.js"))) +
      "\" " + arg)
  os.chdir(repo_dir) # chdir back
  sys.exit(0)

# Get all the pages and resources from publish.xml:

def get_list(arg, desc):
    os.chdir(master_dir)
    cmd = node + " \"" + native_path(join(tools_dir, "publish/publish.js")) + "\" " + arg
    status, output = getstatusoutput(cmd)
    os.chdir(repo_dir)
    if status != 0:
      exit(1, 'FAIL: could not get list of ' + desc)
    return output.split()

tocpages    = get_list("--list-toc-pages", "specification pages")
nontocpages = get_list("--list-nontoc-pages", "specification pages")
resources   = get_list("--list-resources", "resources")
defs        = get_list("--list-definition-files", "definition files")

all = tocpages + nontocpages

# Build chapters as required:

deps = [join(master_dir, "publish.xml")] + [join(master_dir, f) for f in defs]
for filename in os.listdir(publishjs_dir):
  path = join(publishjs_dir, filename)
  if os.path.isfile(path):
    deps.append(path)
deptimes = [getmtime(file) for file in deps]
tobuild = []
tobuild_names = []
for name in all:
  localdeps = []
  if name in tocpages or name == "idl":
    # pages with spec-wide ToCs on them depend on all chapters for
    # their headings; also, the IDL appendix must be rebuilt to pick
    # up IDL changes in individual chapters
    localdeps += [join(master_dir, page + ".html") for page in nontocpages]
  localdeptimes = [getmtime(file) for file in localdeps]
  pub_path = join(publish_dir, name + ".html")
  src_path = join(master_dir, name + ".html")
  if not isfile(pub_path):
    # destination doesn't exist; build it
    tobuild.append(pub_path)
    tobuild_names.append(name)
    continue
  desttime = getmtime(pub_path)
  desttime_s = time.gmtime(desttime)
  now_s = time.gmtime()
  if ((desttime_s.tm_year, desttime_s.tm_mon, desttime_s.tm_mday) !=
      (now_s.tm_year, now_s.tm_mon, now_s.tm_mday)):
    # date has changed; rebuild so the page header/footer has the right date
    tobuild.append(pub_path)
    tobuild_names.append(name)
    continue
  for srctime in deptimes + localdeptimes + [getmtime(src_path)]:
    # a dependency is newer; rebuild
    if srctime > desttime:
      tobuild.append(pub_path)
      tobuild_names.append(name)
      break

if len(sys.argv) == 2 and sys.argv[1] == "-s":
  # stabilize issues
  if tobuild:
    os.chdir(master_dir)
    print "* stabilizing issues in " + ", ".join(tobuild_names)
    for page in tobuild_names:
      run("perl \"" + native_path(join(tools_dir, "stabilizer.pl")) + "\" " +
          page + ".html issue-state.txt")
    os.chdir(repo_dir) # chdir back
  sys.exit(0)

if tobuild:
  # build chapters
  toremove = tobuild
  os.chdir(master_dir)
  print "* building " + ", ".join(tobuild_names)
  run(node + " \"" +
      native_path(join(tools_dir, join("publish","publish.js"))) +
      "\" --build " +
      " ".join(tobuild_names) +
      (" --local-style" if os.environ.get("SVG_BUILD_LOCAL_STYLE_SHEETS") else ""))
  toremove = []
  os.chdir(repo_dir) # chdir back

# Build single page spec as required:

if len(all) > 1 and not os.environ.get("SVG_BUILD_NO_SINGLE_PAGE"):
  buildSinglePage = False
  single_page = join(publish_dir, "single-page.html")
  
  if not isfile(single_page):
    buildSinglePage = True
  else:
    singlePageTime = getmtime(single_page)
    for name in all:
      if getmtime(join(publish_dir, name + ".html")) > singlePageTime:
        buildSinglePage = True
        break
  
  if buildSinglePage:
    os.chdir(master_dir)
    print "* building single page spec"
    run(node + " \"" +
        native_path(join(tools_dir, join("publish","publish.js"))) +
        "\" --build-single-page")
    os.chdir(repo_dir) # chdir back

# Copy over anything else that needs to be copied to 'publish':
for f in resources:
  tocopypath = join(master_dir, f)
  if os.path.exists(tocopypath):
    copyto = os.path.join(publish_dir,os.path.basename(tocopypath))
    shutil.rmtree(copyto, ignore_errors=True)
    if os.path.isdir(tocopypath):
      shutil.copytree(tocopypath, copyto)
    else:
      shutil.copyfile(tocopypath, copyto)

# Done:

if not built_something:
  print "* nothing to do"

done()
