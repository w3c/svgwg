"""Node locator for MathML parser."""
import sys

class NodeLocator:
    """Node locator for MathML parser.
    
    Stores data from a SAX locator object; 
    provides a method to format error messages from the parser."""
    def __init__ (self, locator):
        if locator:
            self.line = locator.getLineNumber()
            self.column = locator.getColumnNumber()
            self.filename = locator.getSystemId()
        else:
            self.line = None
            self.column = None
            self.filename = None
            
    def message(self, msg, label = None): 
        coordinate = ""
        separator = ""
        if self.filename is not None: 
            coordinate += "file %s" % self.filename
            separator = ", "
        if self.line is not None: 
            coordinate += separator + "line %d" % self.line
            separator = ", "
        if self.column is not None: 
            coordinate += separator + "column %d" % self.column

        if label:      sys.stderr.write("[%s] " % label)
        if coordinate: sys.stderr.write(coordinate + ": ")
        if msg:        sys.stderr.write(msg)
        sys.stderr.write('\n')
