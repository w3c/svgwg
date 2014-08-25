import sys, glyphlist
from metric import FontMetric, CharMetric, FontFormatError 

def parseLength(s): return 0.001 * float(s)

class AFMFormatError (FontFormatError):
    def __init__(self, msg):
        FontFormatError.__init__(self, msg)

class AFMMetric (FontMetric):

    def __init__(self, afmname, glyphlistname=None, log=None):
        FontMetric.__init__(self, log)
        afmfile = open(afmname, "r")
        if glyphlistname is None: 
            self.glyphList = glyphlist.defaultGlyphList 
        else: 
            self.glyphList = glyphlist.GlyphList(open(afmname, "r"))
        self.readFontMetrics(afmfile)
        afmfile.close()
        self.postParse()
        
    def readFontMetrics(self, afmfile):
        line = afmfile.readline()
        if not line.startswith("StartFontMetrics"):
            raise AFMFormatError, "File is not an AFM file"
        # TODO: AFM version control    
            
        while True:
            line = afmfile.readline()
            if len(line) == 0: break # EOF
            if line.startswith("EndFontMetrics"): break
            
            if line.startswith("StartCharMetrics"):
                self.readCharMetrics(afmfile)
            elif line.startswith("StartKernData"):
                self.readKernData(afmfile)
            elif line.startswith("StartComposites"):
                self.readComposites(afmfile)
            else:
                tokens = line.split(None, 1)
                if len (tokens) < 2: continue
                if tokens[0] == "FontName":
                    self.fontname = tokens[1].strip()
                elif tokens[0] == "FullName":
                    self.fullname = tokens[1].strip()
                elif tokens[0] == "FamilyName":
                    self.family = tokens[1].strip()
                elif tokens[0] == "Weight":
                    self.weight = tokens[1].strip()
                elif tokens[0] == "FontBBox":
                    self.bbox = map (parseLength, tokens[1].split())
                elif tokens[0] == "CapHeight":
                    self.capheight = parseLength(tokens[1])
                elif tokens[0] == "XHeight":
                    self.xheight = parseLength(tokens[1])
                elif tokens[0] == "Ascender":
                    self.ascender = parseLength(tokens[1])
                elif tokens[0] == "Descender":
                    self.descender = parseLength(tokens[1])
                elif tokens[0] == "StdHW":
                    self.stdhw = parseLength(tokens[1])
                elif tokens[0] == "StdVW":
                    self.stdvw = parseLength(tokens[1])
                elif tokens[0] == "UnderlinePosition":
                    self.underlineposition = parseLength(tokens[1])
                elif tokens[0] == "UnderlineThickness":
                    self.underlinethickness = parseLength(tokens[1])
                elif tokens[0] == "ItalicAngle":
                    self.italicangle = float(tokens[1])
                elif tokens[0] == "CharWidth":
                    self.charwidth = parseLength(tokens[1].split()[0])

    def readCharMetrics(self, afmfile):   
        while True:
            line = afmfile.readline()
            if len(line) == 0: break; # EOF
            if line.startswith("EndCharMetrics"): break
            self.parseCharMetric(line)     

                        
    def parseCharMetric(self, line):                    
        glyphname = None; width = None; bbox = None

        for token in line.split(";"):
            d = token.split()
            if len(d) < 2: continue
            if d[0] == "W" or d[0] == "WX" or d[0] == "W0X":
                width = parseLength(d[1])
            elif d[0] == "B" and len(d) == 5:
                bbox = map (parseLength, d[1:])
            elif d[0] == "N":            
                glyphname = d[1]

        if glyphname is None: return
        if bbox is None:
            if self.bbox is not None: bbox = self.bbox
            else: bbox = [0, 0, 0, 0]
        if width is None:
            if self.charwidth is not None: width = self.charwidth
            else: width = bbox[2] - bbox[0]

        codes = self.glyphList.lookup(glyphname)
        if codes is not None:
            cm = CharMetric(glyphname, codes, width, bbox)
            for c in codes: self.chardata[c] = cm
        elif glyphname.startswith("uni"):
            if len(glyphname) != 7: pass # no support for composites yet  
            try:
                c = int(glyphname[3:], 16)
                if c >= 0 and c < 0x10000: 
                    self.chardata[c] = CharMetric(glyphname, [c], width, bbox)
            except TypeError: pass
        elif glyphname.startswith("u"):
            if len(glyphname) not in [5, 6, 7]: pass   
            try:            
                c = int(glyphname[1:], 16)
                if c >= 0 and c < 0x10000: 
                    self.chardata[c] = CharMetric(glyphname, [c], width, bbox)
            except TypeError: pass

    def readKernData(self, afmfile):  
        while True:
            line = afmfile.readline()
            if len(line) == 0: break; # EOF
            if line.startswith("EndKernData"): break
            # TODO: parse kerning pairs    
                
    def readComposites(self, afmfile):    
        while True:
            line = afmfile.readline()
            if len(line) == 0: break; # EOF
            if line.startswith("EndComposites"): break
            # TODO: parse composites
               
def main():
    if len (sys.argv) == 2: 
        AFMMetric(sys.argv[1], log=sys.stderr).dump() 
    else:
        print """Usage: AFM.py <path to AFM file>"""

if __name__ == "__main__": main()
