import sys 
from metric import FontMetric, CharMetric, FontFormatError 

def readUnsigned(ff, size): 
    res = 0;
    for c in ff.read(size): 
        res *= 0x100; 
        res += ord(c)
    return res

def readSigned(ff, size):
    res = ord(ff.read(1));
    if res >= 0x80: res -= 0x100 
    for c in ff.read(size - 1): 
        res *= 0x100; 
        res += ord(c)
    return res

def readFixed32(ff):
    return readSigned(ff, 4) / 65536.0

def readF2_14(ff):
    return readSigned(ff, 2) / 16384.0

def skip(ff, size):
    ff.read(size)


class TTFFormatError (FontFormatError):
    def __init__(self, msg):
        FontFormatError.__init__(self, msg)
           
class TTFMetric (FontMetric):

    def __init__(self, ttfname, log=None):
        FontMetric.__init__(self, log)
        ff = open(ttfname, "rb")
        self.readFontMetrics(ff)
        ff.close()
        self.postParse()
        
    def readFontMetrics(self, ff):
        version = ff.read(4)
        if map(ord, version) == [0, 1, 0, 0]:
            self.fonttype="TTF"
        elif version == "OTTO":
            # self.fonttype="OTF"
            # At the moment, I cannot parse bbox data out from CFF
            raise TTFFormatError, "OpenType/CFF fonts are unsupported"
        else:
            raise TTFFormatError, "Not a TrueType file"
        
        numTables = readUnsigned(ff, 2)
        tables = {}
        skip(ff, 6)
        for i in range(0, numTables):
            tag = ff.read(4)
            checksum = readUnsigned(ff, 4)
            offset = readUnsigned(ff, 4)
            length = readUnsigned(ff, 4)
            tables[tag] = (offset, length)

        def switchTable(tableTag):
            if tableTag not in tables.keys():
                raise TTFFormatError, "Required table "+tableTag+" missing in TrueType file"
            return tables[tableTag]
            
        (offset, length) = switchTable("head")
        ff.seek(offset+12)
        magic = readUnsigned(ff, 4)
        if magic != 0x5F0F3CF5:
            raise TTFFormatError, "Magic number in 'head' table does not match the spec"
        skip(ff, 2)
        self.unitsPerEm = readUnsigned(ff, 2)
        emScale = 1.0 / self.unitsPerEm
        
        skip(ff, 16)
        xMin = readSigned(ff, 2) * emScale
        yMin = readSigned(ff, 2) * emScale
        xMax = readSigned(ff, 2) * emScale
        yMax = readSigned(ff, 2) * emScale        
        self.bbox = [xMin, yMin, xMax, yMax]

        skip(ff, 6)
        self.indexToLocFormat = readSigned(ff, 2)
           
        (offset, length) = switchTable("maxp")
        ff.seek(offset+4)
        self.numGlyphs = readUnsigned(ff, 2)

        (offset, length) = switchTable("name")
        ff.seek(offset+2)
        
        numRecords = readUnsigned(ff, 2)
        storageOffset = readUnsigned(ff, 2) + offset
        
        uniNames = {}
        macNames = {}
        englishCodes = [0x409, 0x809, 0xC09, 0x1009, 0x1409, 0x1809]
        
        for i in range (0, numRecords):
            platformID = readUnsigned(ff, 2)
            encodingID = readUnsigned(ff, 2)
            languageID = readUnsigned(ff, 2)
            nameID = readUnsigned(ff, 2)
            nameLength = readUnsigned(ff, 2)
            nameOffset = readUnsigned(ff, 2)
        
            if platformID == 3 and encodingID == 1:
                if languageID in englishCodes or nameID not in uniNames.keys(): 
                    uniNames[nameID] = (nameOffset, nameLength)
            elif platformID == 1 and encodingID == 0:
                if languageID == 0 or nameID not in macNames.keys():
                    macNames[nameID] = (nameOffset, nameLength)

        def getName (code):
            if code in macNames.keys():
                (nameOffset, nameLength) = macNames[code]
                ff.seek (storageOffset + nameOffset)
                return ff.read(nameLength)
                # FIXME: repair Mac encoding here
            elif code in uniNames.keys():
                (nameOffset, nameLength) = uniNames[code]
                ff.seek (storageOffset + nameOffset)
                result = u""
                for i in range (0, nameLength/2):
                    result += unichr(readUnsigned(ff, 2))
                return result
       
        self.family = getName(1)
        self.fullname = getName(4)
        self.fontname = getName(6)
        
        (offset, length) = switchTable("OS/2")
        ff.seek(offset)
        tableVersion = readUnsigned(ff, 2)
        cw = readSigned(ff, 2)
        if cw: self.charwidth = cw * emScale

        wght = readUnsigned(ff, 2)
        if wght < 150: self.weight = "Thin"
        elif wght < 250: self.weight = "Extra-Light"
        elif wght < 350: self.weight = "Light"
        elif wght < 450: self.weight = "Regular"
        elif wght < 550: self.weight = "Medium"
        elif wght < 650: self.weight = "Demi-Bold"
        elif wght < 750: self.weight = "Bold"
        elif wght < 850: self.weight = "Extra-Bold"
        else: self.weight = "Black"

        skip(ff, 62)
        self.ascender = readSigned(ff, 2) * emScale
        self.descender = readSigned(ff, 2) * emScale

        if tableVersion == 2: 
            skip(ff, 14)
            xh = readSigned(ff, 2)
            if xh: self.xheight = xh * emScale
            ch = readSigned(ff, 2)
            if ch: self.capheight = ch * emScale
            
           
        (offset, length) = switchTable("post")
        ff.seek(offset+4)
        self.italicangle = readFixed32(ff)
        self.underlineposition = readSigned(ff, 2) * emScale
        self.underlinethickness = readSigned(ff, 2) * emScale

        (offset, length) = switchTable("hhea")
        ff.seek(offset+34)
        numHmtx = readUnsigned(ff, 2)

        (offset, length) = switchTable("hmtx")
        ff.seek(offset)
        glyphArray = []
        w = 0
        for i in range (0, self.numGlyphs):
            if i < numHmtx: 
                w = readUnsigned(ff, 2) * emScale
                skip (ff, 2)
            glyphArray.append(CharMetric(width = w))
        
        (offset, length) = switchTable("cmap")
        ff.seek(offset+2)
        subtableOffset = 0
        numTables = readUnsigned(ff, 2)
        
        cmapEncodings = {}        
        for i in range (0, numTables):
             platformID = readUnsigned(ff, 2)
             encodingID = readUnsigned(ff, 2)
             subtableOffset = readUnsigned(ff, 4)
             cmapEncodings[(platformID, encodingID)] = subtableOffset
        
        encodingScheme = "Unicode"
        subtableOffset = cmapEncodings.get((3, 1))
        if subtableOffset is None: 
            encodingScheme = "Symbol"
            subtableOffset = cmapEncodings.get((3, 0))            
            if subtableOffset is None: 
                raise TTFFormatError, "Cannot use font '%s': no known subtable in 'cmap' table" % self.fullname
            else:
                if self.log:
                    self.log.write("WARNING: font '%s' is a symbolic font - Unicode mapping may be unreliable\n" % self.fullname) 

        ff.seek(offset + subtableOffset)

        tableFormat = readUnsigned(ff, 2)
        if tableFormat != 4:
            raise TTFFormatError, "Unsupported format in 'cmap' table: %d" % tableFormat
        
        subtableLength = readUnsigned(ff, 2)
        skip (ff, 2)
        segCount = readUnsigned(ff, 2) / 2
        skip (ff, 6)
        
        endCounts = []
        for i in range (0, segCount): endCounts.append(readUnsigned(ff, 2))
        
        skip (ff, 2)
        startCounts = []
        for i in range (0, segCount): startCounts.append(readUnsigned(ff, 2))

        idDeltas = []
        for i in range (0, segCount): idDeltas.append(readSigned(ff, 2))

        rangeOffsets = []
        for i in range (0, segCount): rangeOffsets.append(readUnsigned(ff, 2))
        
        remainingLength = subtableLength - 8*segCount - 16
        if remainingLength <= 0:
            remainingLength += 0x10000 # protection against Adobe's bug

        glyphIdArray = []
        for i in range (0, remainingLength/2): glyphIdArray.append(readUnsigned(ff, 2))

        for i in range (0, segCount):
            for c in range(startCounts[i], endCounts[i]+1):
                if c == 0xFFFF: continue
                gid = 0
                if rangeOffsets[i]:
                    idx = c - startCounts[i] + rangeOffsets[i]/2 - (segCount - i)   
                    gid = glyphIdArray[idx]
                else: gid = c + idDeltas[i] 
                if gid >= 0x10000: gid -= 0x10000
                elif gid < 0: gid += 0x10000
                
                cm = glyphArray[gid]
                cm.codes.append(c)
                # Dirty hack: map the lower half of the private-use area to ASCII
                if encodingScheme == "Symbol" and c in range(0xF020, 0xF07F):
                    cm.codes.append(c - 0xF000)
                if not cm.name: cm.name = "u%04X" % c

        (offset, length) = switchTable("loca")
        ff.seek(offset)
        glyphIndex = []
        scalefactor = self.indexToLocFormat + 1

        if self.indexToLocFormat == 0:
            for i in range (0, self.numGlyphs+1):
                glyphIndex.append(readUnsigned(ff, 2) * 2)
        elif self.indexToLocFormat == 1:
            for i in range (0, self.numGlyphs+1):
                glyphIndex.append(readUnsigned(ff, 4))        
        else:
            raise TTFFormatError, "Invalid indexToLocFormat value (%d) in 'head' table" % str(self.indexToLocFormat)
        
        (offset, length) = switchTable("glyf")
        for i in range (0, self.numGlyphs):
            cm = glyphArray[i]
            if glyphIndex[i] == glyphIndex[i+1]: 
                cm.bbox = [0, 0, 0, 0] # empty glyph
            else:
                ff.seek(offset + glyphIndex[i] + 2)
                xMin = readSigned(ff, 2) * emScale
                yMin = readSigned(ff, 2) * emScale
                xMax = readSigned(ff, 2) * emScale
                yMax = readSigned(ff, 2) * emScale        
                cm.bbox = [xMin, yMin, xMax, yMax]
            for c in cm.codes: self.chardata[c] = cm
            
def main():
    if len (sys.argv) == 2: 
        TTFMetric(sys.argv[1], log=sys.stderr).dump() 
    else:
        print """Usage: TTF.py <path to TTF file>"""

if __name__ == "__main__": main()
