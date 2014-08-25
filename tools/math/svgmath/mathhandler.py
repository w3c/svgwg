"""SAX filter for MathML-to-SVG conversion."""

import os
import sys
from xml import sax
from mathnode import MathNode
from mathconfig import MathConfig
from nodelocator import NodeLocator

# MathML namespace
MathNS = u"http://www.w3.org/1998/Math/MathML"

class MathHandler (sax.ContentHandler):
    """SAX ContentHandler for converting MathML formulae to SVG.
    
    Instances of this class read MathML through SAX callbacks, and write
    SVG to the destination (specified as another SAX ContentHandler).
    Uses namespace-aware SAX calls for both input and output."""
    
    def __init__(self, saxoutput, config):
        self.config = MathConfig(config)
        self.output = saxoutput
        self.skip = 0
        self.currentNode = None
        self.locator = None

    
    def setDocumentLocator(self, locator): 
        self.locator = locator


    def startDocument(self): 
        self.output.startDocument()   


    def endDocument(self): 
        self.output.endDocument()   


    def startElementNS(self, elementName, qName, attributes):
        if self.skip > 0: self.skip += 1; return

        locator = NodeLocator(self.locator)
        (namespace, localName) = elementName
        if namespace and namespace != MathNS:
            if self.config.verbose:
                locator.message("Skipped element '%s' from an unknown namespace '%s'" % (localName, namespace), "INFO")
            self.skip = 1; return
            
        properties = {}
        for (attName, value) in attributes.items():
            (attNamespace, attLocalName) = attName
            if attNamespace and attNamespace != MathNS:
                if self.config.verbose:
                    locator.message("Ignored attribute '%s' from an unknown namespace '%s'" % (attLocalName, attNamespace), "INFO")
                continue            
            properties[attLocalName] = value

        self.currentNode = MathNode (localName, properties, locator, self.config, self.currentNode)

      
    def endElementNS(self, elementName, qName): 
        if self.skip > 0: 
            self.skip -= 1
            if self.skip > 0: return

        (namespace, localname) = elementName
        if namespace and namespace != MathNS:
            raise sax.SAXParseException("SAX parser error: namespace on opening and closing elements don't match", None, self.locator)
        if self.currentNode is None: 
            raise sax.SAXParseException("SAX parser error: unmatched closing tag", None, self.locator)

        # Normalize text
        self.currentNode.text = u' '.join(self.currentNode.text.split())

        # If we're back to the top of the tree, measure and draw everything
        if self.currentNode.parent is None:
            self.currentNode.makeImage(self.output)
            
        self.currentNode = self.currentNode.parent


    def characters(self, content):
        if self.skip > 0: return
        if self.currentNode: 
            self.currentNode.text += content

class MathEntityResolver(sax.handler.EntityResolver):
    def __init__(self):
        pass

    def resolveEntity(self, publicId, systemId):
        if systemId == "http://www.w3.org/TR/MathML2/dtd/mathml2.dtd":
            return os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]),  "mathml2.dtd"))
        return systemId
