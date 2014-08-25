"""Main structure class for MathML formatting."""

import sys, contextmakers, measurers, generators 
from xml import sax
from nodelocator import NodeLocator


def isHighSurrogate(ch):
    """Tests whether a Unicode character is from the high surrogates range"""
    code = ord(ch)
    return (0xD800 <= code and code <= 0xDBFF)
    
def isLowSurrogate(ch):
    """Tests whether a Unicode character is from the low surrogates range"""
    code = ord(ch)
    return (0xDC00 <= code and code < 0xDFFF)
    
def decodeSurrogatePair(hi, lo):
    """Returns a scalar value  that corresponds to a surrogate pair"""
    return ((ord(hi) - 0xD800) * 0x400) + (ord(lo) - 0xDC00) + 0x10000


globalDefaults = {
    # Font and color properties
    u"mathvariant": u"normal",
    u"mathsize": u"12pt",
    u"mathcolor": u"black",      
    u"mathbackground": u"transparent", 
    u"displaystyle": u"false",
    u"scriptlevel": u"0",
    # Script size factor and minimum value
    u"scriptsizemultiplier": u"0.71",
    u"scriptminsize": u"8pt",
    # Spaces
    u"veryverythinmathspace": u"0.0555556em",
    u"verythinmathspace": u"0.111111em",
    u"thinmathspace": u"0.166667em",
    u"mediummathspace": u"0.222222em",
    u"thickmathspace": u"0.277778em",
    u"verythickmathspace": u"0.333333em",
    u"veryverythickmathspace": u"0.388889em",
    # Line thickness and slope for mfrac    
    u"linethickness": "1",
    u"bevelled": u"false",
    u"enumalign": u"center",
    u"denomalign": u"center",
    # String quotes for ms
    u"lquote": u"\"",
    u"rquote": u"\"",
    # Properties for mspace
    u"height": u"0ex",
    u"depth": u"0ex",
    u"width": u"0em",
    # Properties for mfenced
    u"open": u"(",
    u"close": u")",
    u"separators": u",",
    # Property for menclose
    u"notation": u"longdiv",    
    # Properties for mtable
    u"align": u"axis",
    u"rowalign": u"baseline",
    u"columnalign": u"center",
    u"columnwidth": u"auto",
    u"equalrows": u"false",
    u"equalcolumns": u"false",
    u"rowspacing": u"1.0ex",
    u"columnspacing": u"0.8em",
    u"framespacing": u"0.4em 0.5ex",
    u"rowlines": u"none",
    u"columnlines": u"none",
    u"frame": u"none"
}

specialChars = { u'\u2145': u'D',
                 u'\u2146': u'd',
                 u'\u2147': u'e',
                 u'\u2148': u'i',
                 u'\u00A0': u' ' }

class FontMetricRecord:
    """Structure to track usage of a single font family"""
    def __init__(self, family, metric):
       self.family = family
       self.metric = metric
       self.used = False


class MathNode:
    """MathML node descriptor.
    
    This class defines properties and methods that permit to building blocks
    to combine with each other, creating a complex mathematical expression.
    It uses dynamic binding to find methods to process specific MathML 
    elements: these methods are contained in three other modules - 
    contextmakers, measurers, and generators.
    """

    def __init__(self, elementName, attributes, locator, config, parent):
        self.elementName = elementName
        self.config = config
        
        if locator is not None:
            self.locator = locator
        elif parent is not None: # handy when we add nodes in preprocessing
            self.locator = parent.locator
        else:
            self.locator = NodeLocator(None)

        self.text = u''
        self.children = []
        self.attributes = attributes
        self.parent = parent
        self.metriclist = None
        self.nominalMetric = None
        if parent is not None: 
            self.nodeIndex = len(parent.children)
            self.defaults = parent.defaults
            parent.children.append(self)
        else: 
            self.defaults = globalDefaults.copy()
            self.defaults.update(config.defaults)
            self.nodeIndex = 0

                                    
    def makeContext (self):
        contextmakers.__dict__.get(u"context_"+self.elementName, 
                                   contextmakers.default_context)(self)

    def makeChildContext (self, child):
        contextmakers.__dict__.get(u"child_context_"+self.elementName, 
                                   contextmakers.default_child_context)(self, child)


    def measure(self):
        # Create the context for the node
        self.makeContext()     
        # Measure all children        
        for ch in self.children: ch.measure()
        # Perform node-specific measurement
        self.measureNode()
    
    def measureNode(self):
        measureMethod = measurers.__dict__.get(u"measure_"+self.elementName, 
                                               measurers.default_measure)
        if self.config.verbose and measureMethod is measurers.default_measure: 
            self.warning("MathML element '%s' is unsupported" % self.elementName)
        measureMethod(self)


    def draw (self, output):
        generators.__dict__.get(u"draw_"+self.elementName, 
                                generators.default_draw)(self, output)
    
    def makeImage(self, output):        
        if self.elementName != 'math':
            self.warning("Root element in MathML document must be 'math'")
        self.measure()
        generators.drawImage(self, output)

    
    def warning(self, msg): 
        self.locator.message(msg, "WARNING")

    def error(self, msg): 
        self.locator.message(msg, "ERROR")

    def info(self, msg): 
        if self.config.verbose: self.locator.message(msg, "INFO")

    def debug(self, event, msg):
        if event.strip() in self.config.debug: self.locator.message(msg, "DEBUG")


    def parseInt (self, x):
        try: return int(x, 10)
        except TypeError:
            self.error("Cannot parse string '%s' as an integer" % str(x))
            return 0
            
    def parseFloat (self, x):
        try: value = float(x)
        except ValueError:
            self.error("Cannot parse string '%s' as a float" % str(x))
            return 0.0
        text = str(value).lower()
        if text.find("nan") >= 0 or text.find("inf") >= 0:  
            self.error("Cannot parse string '%s' as a float" % str(x))
            return 0.0
        return value
            
    def parseLength(self, lenattr, unitlessScale = 0.75):
        lenattr = lenattr.strip()
        if lenattr.endswith("pt"):
           return self.parseFloat(lenattr[:-2])
        elif lenattr.endswith("mm"):
           return self.parseFloat(lenattr[:-2]) * 72.0 / 25.4 
        elif lenattr.endswith("cm"):
           return self.parseFloat(lenattr[:-2]) * 72.0 / 2.54 
        elif lenattr.endswith("in"):
           return self.parseFloat(lenattr[:-2]) * 72.0
        elif lenattr.endswith("pc"):
           return self.parseFloat(lenattr[:-2]) * 12.0
        elif lenattr.endswith("px"):
           # pixels are calculated for 96 dpi
           return self.parseFloat(lenattr[:-2]) * 72.0 / 96.0
        elif lenattr.endswith("em"):
           return self.parseFloat(lenattr[:-2]) * self.fontSize
        elif lenattr.endswith("ex"):
           return self.parseFloat(lenattr[:-2]) * self.fontSize * self.metric().xheight
        else: 
           # unitless lengths are treated as if  expressed in pixels
           return self.parseFloat(lenattr) * unitlessScale

    def parseSpace(self, spaceattr, unitlessScale = 0.75):
        sign = 1.0
        spaceattr = spaceattr.strip()
        if spaceattr.endswith(u"mathspace"):
           if spaceattr.startswith(u"negative"): 
               sign = -1.0
               spaceattr = spaceattr[8:]
           realspaceattr = self.defaults.get(spaceattr);
           if realspaceattr is None:
               self.error("Bad space token: '%s'" % spaceattr)
               realspaceattr = "0em"
           return self.parseLength(realspaceattr, unitlessScale)
        else:
           return self.parseLength(spaceattr, unitlessScale)

    def parsePercent(self, lenattr, percentBase):
        value = self.parseFloat(lenattr[:-1])
        if value is not None: return percentBase * value / 100
        else: return 0

    def parseLengthOrPercent(self, lenattr, percentBase, unitlessScale = 0.75):
        if lenattr.endswith(u"%"): return self.parsePercent(lenattr, percentBase)
        else: return self.parseLength(lenattr, unitlessScale) 

    def parseSpaceOrPercent(self, lenattr, percentBase, unitlessScale = 0.75):
        if lenattr.endswith(u"%"): return self.parsePercent(lenattr, percentBase)
        else: return self.parseSpace(lenattr, unitlessScale) 


    def getProperty(self, key, defvalue = None):
        return self.attributes.get(key, self.defaults.get(key, defvalue))
    
    def getListProperty(self, attr, value = None):
        if value is None: value = self.getProperty(attr)
        splitvalue = value.split()
        if len(splitvalue) > 0: return splitvalue
        self.error("Bad value for '%s' attribute: empty list" % attr)
        return self.defaults[attr].split()

    def getUCSText(self):
        codes = []
        hisurr = None
        for ch in self.text:
            chcode = ord(ch)

            # Processing surrogate pairs
            if isLowSurrogate(ch):            
                if hisurr is None:
                    self.error("Invalid Unicode sequence - low surrogate character (U+%X) not preceded by a high surrogate" % ord(ch))
                else:
                    chcode = decodeSurrogatePair(hisurr, ch)
                    hisurr = None

            if hisurr is not None:         
                self.error("Invalid Unicode sequence - high surrogate character (U+%X) not followed by a low surrogate" % ord(hisurr))
                hisurr = None
            if isHighSurrogate(ch): 
                hisurr = ch; continue                
            codes.append(chcode)    

        if hisurr is not None:         
            self.error("Invalid Unicode sequence - high surrogate character (U+%X) not followed by a low surrogate" % ord(hisurr))
        return codes


    def fontpool(self):
        if self.metriclist is None:             
            def fillMetricList(familylist):
                metriclist = []
                for family in familylist:
                    metric = self.config.findfont(self.fontweight, self.fontstyle, family)
                    if metric is not None: 
                        metriclist.append(FontMetricRecord(family, metric))
                if len(metriclist) == 0:
                    self.warning("Cannot find any font metric for family "+(", ".join(familylist)))
                    return None
                else: return metriclist
            self.metriclist = fillMetricList(self.fontfamilies)
            if self.metriclist is None:
                self.fontfamilies = self.config.fallbackFamilies
                self.metriclist = fillMetricList(self.fontfamilies)
            if self.metriclist is None:
                self.error("Fatal error: cannot find any font metric for the node; fallback font families misconfiguration")
                raise sax.SAXException("Fatal error: cannot find any font metric for the node")
        return self.metriclist

    def metric(self):
        if self.nominalMetric is None:
            self.nominalMetric = self.fontpool()[0].metric
            for fd in self.metriclist:
                if fd.used: 
                    self.nominalMetric = fd.metric; break                    
        return self.nominalMetric        


    def axis(self):
        return self.metric().axisposition * self.fontSize

    def nominalLineWidth(self):
        return self.metric().rulewidth * self.fontSize
        
    def nominalThinStrokeWidth(self):    
        return 0.04 * self.originalFontSize

    def nominalMediumStrokeWidth(self):    
        return 0.06 * self.originalFontSize

    def nominalThickStrokeWidth(self):    
        return 0.08 * self.originalFontSize

    def nominalLineGap(self):
        return self.metric().vgap * self.fontSize

    def nominalAscender(self):
        return self.metric().ascender * self.fontSize

    def nominalDescender(self):
        return (- self.metric().descender * self.fontSize)

    def hasGlyph(self, ch):
        for fdesc in self.fontpool():
            if fdesc.metric.chardata.get(ch) is not None: 
                return True
        return False
           
    def findChar(self, ch):
        for fd in self.fontpool():
            cm = fd.metric.chardata.get(ch)
            if cm: return (cm, fd)
        else:
            if 0 < ch and ch < 0xFFFF and unichr(ch) in specialChars.keys():
                return self.findChar(ord(specialChars[unichr(ch)]))
            self.warning("Glyph U+%X not found" % ch)
            return None      


    def measureText(self):
        """Measures text contents of a node"""
        if len(self.text) == 0: 
            self.isSpace = True; return        

        cm0 = None; cm1 = None;
        ucstext = self.getUCSText()
        for chcode in ucstext:
            chardesc = self.findChar(chcode)
            if chardesc is None: 
                self.width += self.metric().missingGlyph.width
            else:
                (cm, fd) = chardesc
                fd.used = True
                if chcode == ucstext[0]: cm0 = cm
                if chcode == ucstext[-1]: cm1 = cm
                self.width += cm.width
                if self.height + self.depth == 0:
                    self.height = cm.bbox[3]
                    self.depth = - cm.bbox[1]
                elif cm.bbox[3] != cm.bbox[1]: # exclude space  
                    self.height = max (self.height, cm.bbox[3])
                    self.depth = max (self.depth, - cm.bbox[1])
                    
        # Normalize to the font size
        self.width *= self.fontSize 
        self.depth *= self.fontSize
        self.height *= self.fontSize

        # Add ascender/descender values
        self.ascender = self.nominalAscender()
        self.descender = self.nominalDescender()

        # Shape correction  
        if cm0 is not None: self.leftBearing = max(0, - cm0.bbox[0]) * self.fontSize
        if cm1 is not None: self.rightBearing = max(0, cm1.bbox[2] - cm.width) * self.fontSize
        self.width += self.leftBearing + self.rightBearing        
        
        # Reset nominal metric
        self.nominalMetric = None

