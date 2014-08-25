"""Configuration for MathML-to-SVG formatter."""

import os, sys 
from xml import sax
from fonts.afm import AFMMetric
from fonts.ttf import TTFMetric
from fonts.metric import FontFormatError

class MathConfig(sax.ContentHandler):
    """Configuration for MathML-to-SVG formatter.
    
    Implements SAX ContentHandler for ease of reading from file."""    
    def __init__(self, configfile):
        self.verbose = False
        self.debug = []
        self.currentFamily = None
        self.fonts = {}
        self.variants = {}
        self.defaults = {}
        self.opstyles = {}
        self.fallbackFamilies = []
        
        # Parse config file
        try:
            parser = sax.make_parser()
            parser.setContentHandler(self)
            parser.setFeature(sax.handler.feature_namespaces, 0)
            parser.parse(configfile)
        except sax.SAXException, xcpt:
            print "Error parsing configuration file ", configfile, ": ", xcpt.getMessage()
            sys.exit(1)

    
    def startElement(self, name, attributes):
        if name == u"config":
            self.verbose = (attributes.get(u"verbose") == u"true") 
            self.debug = (attributes.get(u"debug", u"")).replace(u",", u" ").split()

        elif name == u"defaults":
            self.defaults.update(attributes)
            
        elif name == u"fallback":
            familyattr = attributes.get(u"family", u"")
            self.fallbackFamilies = [" ".join(x.split()) for x in familyattr.split(u",")]

        elif name == u"family":
            self.currentFamily = attributes.get(u"name", u"")
            self.currentFamily = "".join(self.currentFamily.lower().split())

        elif name == u"font":
            weight = attributes.get(u"weight", u"normal")
            style = attributes.get(u"style", u"normal")
            fontfullname = self.currentFamily;
            if weight != u"normal":
                fontfullname += u" " + weight
            if style != u"normal":
                fontfullname += u" " + style
            try:
                if u"afm" in attributes.keys():
                    fontpath = attributes.get(u"afm")
                    metric = AFMMetric(fontpath, attributes.get(u"glyph-list"), sys.stderr)
                elif u"ttf" in attributes.keys():
                    fontpath = attributes.get(u"ttf")
                    metric = TTFMetric(fontpath, sys.stderr)
                else:
                    sys.stderr.write("Bad record in configuration file: font is neither AFM nor TTF\n")
                    sys.stderr.write("Font entry for '%s' ignored\n" % fontfullname)
                    return
            except FontFormatError, err:
                sys.stderr.write("Invalid or unsupported file format in '%s': %s\n" % (fontpath, err.message))
                sys.stderr.write("Font entry for '%s' ignored\n" % fontfullname)
                return
            except IOError:
                message = sys.exc_info()[1]
                sys.stderr.write("I/O error reading font file '%s': %s\n" % (fontpath, str(message)))
                sys.stderr.write("Font entry for '%s' ignored\n" % fontfullname)
                return
                 
            self.fonts[weight+u" "+style+u" "+self.currentFamily] = metric
                
        elif name == u"mathvariant":
            variantattr = attributes.get(u"name")
            familyattr = attributes.get(u"family", "")
            splitFamily = [" ".join(x.split()) for x in familyattr.split(u",")] 
            weightattr = attributes.get(u"weight", u"normal")
            styleattr = attributes.get(u"style", u"normal")
            self.variants[variantattr] = (weightattr, styleattr, splitFamily)

        elif name == u"operator-style":
            opname = attributes.get(u"operator")
            if opname:
                styling = {}
                styling.update(attributes)
                del styling[u"operator"]
                self.opstyles[opname] = styling
            else:
                sys.stderr.write("Bad record in configuration file: operator-style with no operator attribute\n")            

        
    def endElement(self, name):
        if name == u"family":
            self.currentFamily = None


    def findfont(self, weight, style, family):
        """Finds a metric for family+weight+style."""
        weight = (weight or u"normal").strip()
        style = (style or u"normal").strip()
        family = "".join((family or u"").lower().split())
        
        for w in [weight, u"normal"]:
            for s in [style, u"normal"]:                
                metric = self.fonts.get(w+u" "+s+u" "+family)
                if metric: return metric
        return None


def main():
    if len(sys.argv) == 1:
        config = MathConfig(None)
    else:
        config = MathConfig(sys.argv[1])
        
    print "Options:  verbose =", config.verbose, " debug =", config.debug
    print "Fonts:"
    for (font, metric) in config.fonts.items():
        print "    ", font, "-->", metric.fontname
    print "Math variants:"
    for (variant, value) in config.variants.items():
        print "    ", variant, "-->", value
    print "Defaults:"
    for (attr, value) in config.defaults.items():
        print "    ", attr, "=", value
    print "Operator styling:"
    for (opname, value) in config.opstyles.items():
        print "    ", repr(opname), ":", value
    print "Fallback font families:", config.fallbackFamilies  
        
    
if __name__ == "__main__": main()
