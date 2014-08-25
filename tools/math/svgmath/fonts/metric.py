class CharMetric:
    def __init__(self, glyphname = None, codes = None, width = None, bbox = None):
        self.name = glyphname
        if codes: self.codes = codes
        else: self.codes = []
        self.width = width
        self.bbox = bbox

class FontFormatError(Exception):
    def __init__(self, msg):
        self.message = msg
    def __str__(self):
        return self.message

class FontMetric:
    def __init__(self, log=None):
        self.fontname = None
        self.fullname = None
        self.family = None
        self.weight = None
        self.bbox = None
        self.capheight = None
        self.xheight = None
        self.ascender = None
        self.descender = None
        self.stdhw = None
        self.stdvw = None
        self.underlineposition = None
        self.underlinethickness = None
        self.italicangle = None
        self.charwidth = None
        self.axisposition = None
        self.chardata = {}
        self.missingGlyph = None
        self.log = log
    
    def postParse(self):
        # Get Ascender from the 'd' glyph
        if self.ascender is None:
            cm = self.chardata.get(ord(u'd'))
            if cm is not None:
                self.descender = cm.bbox[3]
            else: self.ascender = 0.7 
        
        # Get Descender from the 'p' glyph
        if self.descender is None:
            cm = self.chardata.get(ord(u'p'))
            if cm is not None:
                self.descender = cm.bbox[1]
            else: self.descender = -0.2 
        
        # Get CapHeight from the 'H' glyph
        if self.capheight is None:
            cm = self.chardata.get(ord(u'H'))
            if cm is not None:
                self.capheight = cm.bbox[3]
            else: self.capheight = self.ascender 
       
        # Get XHeight from the 'H' glyph
        if self.xheight is None:
            cm = self.chardata.get(ord(u'x'))
            if cm is not None:
                self.xheight = cm.bbox[3]
            else: self.xheight = 0.45 
    
        # Determine the vertical position of the mathematical axis -
        # that is, the quote to which fraction separator lines are raised.
        # We try to deduce it from the median of the following characters:
        # "equal", "minus", "plus", "less", "greater", "periodcentered")
        # Default is CapHeight / 2, or 0.3 if there's no CapHeight.
        if self.axisposition is None:             
            for ch in [ord(u'+'), 0x2212, ord(u'='), ord(u'<'), ord(u'>'), 0xB7]:
                cm = self.chardata.get(ch)
                if cm is not None:
                    self.axisposition = (cm.bbox[1] + cm.bbox[3]) / 2
                    break
            else: self.axisposition = self.capheight / 2
            
        # Determine the dominant rule width for math        
        if self.underlinethickness is not None:
            self.rulewidth = self.underlinethickness
        else:
            for ch in [0x2013, 0x2014, 0x2015, 0x2212, ord(u'-')]:
                cm = self.chardata.get(ch)
                if cm is not None:
                    self.rulewidth = cm.bbox[3] - cm.bbox[1]
                    break
            else: self.rulewidth = 0.05
            
        if self.stdhw is None:
            self.stdhw = 0.03
            
        if self.stdvw is None and not self.italicangle:
            cm = self.chardata.get(ord('!'))
            if cm is not None:
                self.stdvw = cm.bbox[2] - cm.bbox[0]
        if self.stdvw is None:
            cm = self.chardata.get(ord('.'))
            if cm is not None:
                self.stdvw = cm.bbox[2] - cm.bbox[0]
            else:
                self.stdvw = 0.08

        # Set rule gap
        if self.underlineposition is not None:
            self.vgap = - self.underlineposition
        else: self.vgap = self.rulewidth * 2
        
        # Set missing glyph to be a space    
        self.missingGlyph = self.chardata.get(ord(u' ')) or self.chardata.get(0xA0)
   
    def dump(self):
        print "FontName: ", self.fontname
        print "FullName: ", self.fullname
        print "FontFamily: ", self.family
        print "Weight: ", self.weight
        print "FontBBox: ", 
        for x in self.bbox:
            print x,
        print            
        print "CapHeight: ", self.capheight
        print "XHeight: ", self.xheight
        print "Ascender: ", self.ascender
        print "Descender: ", self.descender
        print "StdHW: ", self.stdhw
        print "StdVW: ", self.stdvw
        print "UnderlinePosition: ", self.underlineposition
        print "UnderlineThickness: ", self.underlinethickness
        print "ItalicAngle: ", self.italicangle
        print "CharWidth: ", self.charwidth
        print "MathematicalBaseline: ", self.axisposition
        print "Character data: "
        chars = self.chardata.items()
        chars.sort(key = lambda c: c[0])
        for i, cm in chars:
            if cm is None: continue
            print "    ", ("U+%04X" % i), cm.name+":", "  W", cm.width, "  B",
            for x in cm.bbox: 
                print x,
            print
    