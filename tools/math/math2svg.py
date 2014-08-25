#!/usr/bin/python

"""Command-line tool to replace MathML with SVG throughout a document.

Replaces all instances of MathML throughout the document"""

import getopt, sys, os.path
from xml import sax
# from xml.sax.saxutils import XMLGenerator
from svgmath.tools.saxtools import XMLGenerator, ContentFilter
from svgmath.mathhandler import MathHandler, MathNS, MathEntityResolver

def open_or_die(fname, fmode, role):        
    try: return open(fname, fmode)
    except IOError, xcpt: 
        print "Cannot open %s file '%s': %s" % (role, fname, str(xcpt))
        sys.exit(1)

def usage():
    sys.stderr.write("""
Usage: math2svg.py [options] FILE
Replaces MathML formulae in a document by SVG images. Argument is a file name.

Options:
    -h, --help               display this synopsis and exit
    -s, --standalone         treat input as a standalone MathML document
    -o FILE, --output=FILE   write results to FILE instead of stdout
    -c FILE, --config=FILE   read configuration from FILE
    -e ENC,  --encoding=ENC  produce output in ENC encoding
""")  

class MathFilter (ContentFilter):
    def __init__(self, out, mathout):
        ContentFilter.__init__(self, out)
        self.plainOutput = out
        self.mathOutput = mathout
        self.depth = 0

    # ContentHandler methods
    def setDocumentLocator(self, locator):
        self.plainOutput.setDocumentLocator(locator)
        self.mathOutput.setDocumentLocator(locator)

    def startElementNS(self, elementName, qName, attrs):
        if self.depth == 0:
            (namespace, localName) = elementName
            if namespace == MathNS:
                self.output = self.mathOutput
                self.depth = 1
        else: self.depth += 1
        ContentFilter.startElementNS(self, elementName, qName, attrs)

    def endElementNS(self, elementName, qName):
        ContentFilter.endElementNS(self, elementName, qName)
        if self.depth > 0:
            self.depth -= 1
            if self.depth == 0:
                self.output = self.plainOutput

def main():
    try:
        (opts, args) = getopt.getopt(sys.argv[1:], "c:e:ho:s", ["config=", "encoding=", "help", "output=", "standalone"])
    except getopt.GetoptError:
        usage(); sys.exit(2)
    
    outputfile = None
    configfile = None
    encoding = 'utf-8'
    standalone = False
  
    for o, a in opts:
        if o in ("-h", "--help"):       usage(); sys.exit(0)
        if o in ("-o", "--output"):     outputfile = a
        if o in ("-c", "--config"):     configfile = a
        if o in ("-e", "--encoding"):   encoding = a
        if o in ("-s", "--standalone"): standalone = True
     
    # Check input
    if len(args) < 1:
        sys.stderr.write ("No input file specified!\n")
        usage(); sys.exit(1)        
    elif len(args) > 1: 
        sys.stderr.write("WARNING: extra command line arguments ignored\n")

    source = open_or_die(args[0], "rb", "input") 
        
    # Determine output destination
    if outputfile is None: 
        output = sys.stdout 
    else: 
        output = open_or_die(outputfile, "wb", "output") 
  
    # Determine config file location
    if configfile is None:
        configfile = os.path.join(os.path.dirname(__file__), "svgmath.xml")
    config = open_or_die(configfile, "rb", "configuration")    

    # Create the converter as a content handler. 
    saxoutput = XMLGenerator(output, encoding)
    handler = MathHandler(saxoutput, config)
    if not standalone:
        handler = MathFilter(saxoutput, handler)
    
    # Parse input file
    exitcode = 0
    try:
        parser = sax.make_parser()
        parser.setFeature(sax.handler.feature_namespaces, 1)
	parser.setEntityResolver(MathEntityResolver())
        parser.setContentHandler(handler)
        parser.parse(source)
    except sax.SAXException, xcpt:
        print "Error parsing input file %s: %s" % (args[0], xcpt.getMessage())
        exitcode = 1
    source.close()
    if outputfile is not None:
        output.close()
    sys.exit(exitcode)
    
if __name__ == "__main__":
    main()
