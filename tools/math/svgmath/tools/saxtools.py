"""Miscellaneous SAX-related utilities used in SVGMath"""

from xml.sax import handler
from codecs import getwriter
    
def escape(data):
    """Escape &, <, and > in a string of data.
    
    Unicode version of the same-named function in xml.sax.saxutils,
    with entity replacement stripped off (not needed for generation)."""

    # must do ampersand first
    data = unicode(data)
    data = data.replace(u"&", u"&amp;")
    data = data.replace(u">", u"&gt;")
    data = data.replace(u"<", u"&lt;")
    return data

def quoteattr(data):
    """Escape and quote an attribute value.

    Unicode version of the same-named function in xml.sax.saxutils,
    with entity replacement stripped off (not needed for generation).
    Escape &, <, and > in a string of data, then quote it for use as
    an attribute value.  The '"' character will be escaped as well, if
    necessary.
    """
    data = escape(data)
    if u'"' in data:
        if u"'" in data:
            data = u'"%s"' % data.replace(u'"', u"&quot;")
        else:
            data = u"'%s'" % data
    else:
        data = u'"%s"' % data
    return data
   
   
class XMLGenerator(handler.ContentHandler):
    """Clone of xml.sax.saxutils.XMLGenerator, with bugs fixed.
       
    This is an exact copy of the XMLGenerator class. Unfortunately,
    the original class has critical bugs in namespace processing
    and output encoding support (as of 2.4.3). This serializer fixes 
    them, and additionally provides contraction of empty elements 
    (<a/> instead of <a></a>)
    """

    def __init__(self, out, encoding="iso-8859-1"):
        handler.ContentHandler.__init__(self)
        self._encoding = encoding
        self._out = getwriter(encoding)(out, "xmlcharrefreplace")
        self._ns_contexts = [{}]
        self._current_context = self._ns_contexts[-1]
        self._undeclared_ns_maps = []
        self._starttag_pending = False

    def _write(self, text):
        self._out.write(unicode(text))

    def _qname(self, name):
        if name[0]:
            prefix = self._current_context[name[0]]
            if prefix: 
                return unicode(prefix) + u":" + unicode(name[1])
        return unicode(name[1])
        
    def _flush_starttag(self):
        if self._starttag_pending:
            self._write(u">")
            self._starttag_pending = False

    # ContentHandler methods
    def startDocument(self):
        self._out.reset()
        self._write(u'<?xml version="1.0" encoding="%s"?>\n' % unicode(self._encoding))

    def endDocument(self):
        self._out.reset()

    def startPrefixMapping(self, prefix, uri):
        self._ns_contexts.append(self._current_context.copy())
        self._current_context[uri] = prefix
        self._undeclared_ns_maps.append((prefix, uri))

    def endPrefixMapping(self, prefix):
        self._current_context = self._ns_contexts[-1]
        del self._ns_contexts[-1]

    def startElement(self, name, attrs):
        self._flush_starttag()
        self._write(u"<%s" % unicode(name))
        for (name, value) in attrs.items():
            self._write(u" %s=%s" % (unicode(name), quoteattr(value)))
        self._starttag_pending = True

    def endElement(self, name):
        if self._starttag_pending:
            self._write(u"/>")
            self._starttag_pending = False
        else:
            self._write(u"</%s>" % unicode(name))

    def startElementNS(self, name, qname, attrs):
        qattrs = {}
        for attname, attvalue in attrs.items(): 
            qattrs[self._qname(attname)] = attvalue
        for prefix, uri in self._undeclared_ns_maps:
            if prefix:
                qattrs[u"xmlns:%s" % unicode(prefix)] = uri
            else:
                qattrs[u"xmlns"] = uri        
        self._undeclared_ns_maps = []    
        self.startElement(self._qname(name), qattrs)

    def endElementNS(self, name, qname):
        self.endElement(self._qname(name))

    def characters(self, content):
        self._flush_starttag()
        self._write(escape(content))

    def ignorableWhitespace(self, content):
        self.characters(content)

    def processingInstruction(self, target, data):
        self._flush_starttag()
        self._write(u"<?%s %s?>" % (unicode(target), unicode(data)))


class ContentFilter (handler.ContentHandler):
    """Implementation of ContentHandler that passes callbacks to another ContentHandler.
    
    Used to implement filtering functionality on the ContentHandler side."""
    
    def __init__(self, out):
        handler.ContentHandler.__init__(self)
        self.output = out

    # ContentHandler methods
    def startDocument(self):
        self.output.startDocument()

    def endDocument(self):
        self.output.endDocument()

    def startPrefixMapping(self, prefix, uri):
        self.output.startPrefixMapping(prefix, uri)

    def endPrefixMapping(self, prefix):
        self.output.endPrefixMapping(prefix)

    def startElement(self, elementName, attrs):
        self.output.startElement(elementName, attrs)

    def endElement(self, elementName):
        self.output.endElement(elementName)                

    def startElementNS(self, elementName, qName, attrs):
        self.output.startElementNS(elementName, qName, attrs)

    def endElementNS(self, elementName, qName):
        self.output.endElementNS(elementName, qName)                

    def characters(self, content):
        self.output.characters(content)

    def ignorableWhitespace(self, content):
        self.output.ignorableWhitespace(content)

    def processingInstruction(self, target, data):
        self.output.processingInstruction(target, data)

