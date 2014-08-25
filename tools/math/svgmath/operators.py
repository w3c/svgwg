"""MathML operator dictionary and related functions"""
import sys

operatorDictionary = {}

def lookup(op, form = u"infix"):
    """Find the entry for an operator in the dictionary"""
    res = operatorDictionary.get(op+form)
    if res is not None: return res 
    
    for f in [u"infix", u"postfix", u"prefix"]:
        res = operatorDictionary.get(op+f)
        if res is not None: return res 
    
    return operatorDictionary[u""+u"infix"]  # default entry

    
def createEntry( content, 
                 form = u"infix", 
                 fence = u"false", 
                 separator = u"false",
                 accent = u"false",
                 largeop = u"false",
                 lspace = u"thickmathspace", 
                 rspace = u"thickmathspace",
                 stretchy = u"false", 
                 scaling = u"uniform", 
                 minsize = u"1", 
                 maxsize = u"infinity", 
                 movablelimits = u"false",
                 symmetric = u"true" ) :
    if content+form in operatorDictionary.keys():
        sys.stderr.write("WARNING: duplicate entry in operator dictionary, %s %s\n" %(form, str(content)))
    operatorDictionary[content+form] = { u"form": form,
                                         u"fence": fence,
                                         u"separator": separator,
                                         u"accent": accent,
                                         u"largeop": largeop,
                                         u"lspace": lspace, 
                                         u"rspace": rspace,
                                         u"stretchy": stretchy, 
                                         u"scaling": scaling, 
                                         u"minsize": minsize, 
                                         u"maxsize": maxsize, 
                                         u"movablelimits": movablelimits,
                                         u"symmetric": symmetric } 
                
# Create default entry
createEntry (content=u"")

# Create real entries
createEntry (content=u"(", form=u"prefix", fence=u"true", stretchy=u"true", scaling="vertical", lspace=u"0em", rspace=u"0em")
createEntry (content=u")", form=u"postfix", fence=u"true", stretchy=u"true", scaling="vertical", lspace=u"0em", rspace=u"0em")
createEntry (content=u"[", form=u"prefix", fence=u"true", stretchy=u"true", scaling="vertical", lspace=u"0em", rspace=u"0em")
createEntry (content=u"]", form=u"postfix", fence=u"true", stretchy=u"true", scaling="vertical", lspace=u"0em", rspace=u"0em")
createEntry (content=u"{", form=u"prefix", fence=u"true", stretchy=u"true", scaling="vertical", lspace=u"0em", rspace=u"0em")
createEntry (content=u"}", form=u"postfix", fence=u"true", stretchy=u"true", scaling="vertical", lspace=u"0em", rspace=u"0em")
createEntry (content=u"\u201D", form=u"postfix", fence=u"true", lspace=u"0em", rspace=u"0em") # CloseCurlyDoubleQuote
createEntry (content=u"\u2019", form=u"postfix", fence=u"true", lspace=u"0em", rspace=u"0em") # CloseCurlyQuote
createEntry (content=u"\u2329", form=u"prefix", fence=u"true", stretchy=u"true", scaling="vertical", lspace=u"0em", rspace=u"0em") # LeftAngleBracket
createEntry (content=u"\u2308", form=u"prefix", fence=u"true", stretchy=u"true", scaling="vertical", lspace=u"0em", rspace=u"0em") # LeftCeiling
createEntry (content=u"\u301A", form=u"prefix", fence=u"true", stretchy=u"true", scaling="vertical", lspace=u"0em", rspace=u"0em") # LeftDoubleBracket
createEntry (content=u"\u230A", form=u"prefix", fence=u"true", stretchy=u"true", scaling="vertical", lspace=u"0em", rspace=u"0em") # LeftFloor
createEntry (content=u"\u201C", form=u"prefix", fence=u"true", lspace=u"0em", rspace=u"0em") # OpenCurlyDoubleQuote
createEntry (content=u"\u2018", form=u"prefix", fence=u"true", lspace=u"0em", rspace=u"0em") # OpenCurlyQuote
createEntry (content=u"\u232A", form=u"postfix", fence=u"true", stretchy=u"true", scaling="vertical", lspace=u"0em", rspace=u"0em") # RightAngleBracket
createEntry (content=u"\u2309", form=u"postfix", fence=u"true", stretchy=u"true", scaling="vertical", lspace=u"0em", rspace=u"0em") # RightCeiling
createEntry (content=u"\u301B", form=u"postfix", fence=u"true", stretchy=u"true", scaling="vertical", lspace=u"0em", rspace=u"0em") # RightDoubleBracket
createEntry (content=u"\u230B", form=u"postfix", fence=u"true", stretchy=u"true", scaling="vertical", lspace=u"0em", rspace=u"0em") # RightFloor
createEntry (content=u"\u2063", form=u"infix", separator=u"true", lspace=u"0em", rspace=u"0em") # InvisibleComma
createEntry (content=u",", form=u"infix", separator=u"true", lspace=u"0em", rspace=u"verythickmathspace")
createEntry (content=u"\u2500", form=u"infix", stretchy=u"true", scaling="horizontal", minsize=u"0", lspace=u"0em", rspace=u"0em") # HorizontalLine
# Commented out: collides with '|'. See http://lists.w3.org/Archives/Public/www-math/2004Mar/0028.html
# createEntry (content=u"|", form=u"infix", stretchy=u"true", scaling="vertical", minsize=u"0", lspace=u"0em", rspace=u"0em") # VerticalLine 
createEntry (content=u";", form=u"infix", separator=u"true", lspace=u"0em", rspace=u"thickmathspace")
createEntry (content=u";", form=u"postfix", separator=u"true", lspace=u"0em", rspace=u"0em")
createEntry (content=u":=", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace")
createEntry (content=u"\u2254", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # Assign
createEntry (content=u"\u2235", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # Because
createEntry (content=u"\u2234", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # Therefore
createEntry (content=u"\u2758", form=u"infix", stretchy=u"true", scaling="vertical", lspace=u"thickmathspace", rspace=u"thickmathspace") # VerticalSeparator
createEntry (content=u"//", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace")
# Commented out: collides with Proportional
# createEntry (content=u"\u2237", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # Colon
createEntry (content=u"&", form=u"prefix", lspace=u"0em", rspace=u"thickmathspace")
createEntry (content=u"&", form=u"postfix", lspace=u"thickmathspace", rspace=u"0em")
createEntry (content=u"*=", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace")
createEntry (content=u"-=", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace")
createEntry (content=u"+=", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace")
createEntry (content=u"/=", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace")
createEntry (content=u"->", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace")
createEntry (content=u":", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace")
createEntry (content=u"..", form=u"postfix", lspace=u"mediummathspace", rspace=u"0em")
createEntry (content=u"...", form=u"postfix", lspace=u"mediummathspace", rspace=u"0em")
# Commented out: collides with ReverseElement
# createEntry (content=u"\u220B", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # SuchThat
createEntry (content=u"\u2AE4", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # DoubleLeftTee
createEntry (content=u"\u22A8", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # DoubleRightTee
createEntry (content=u"\u22A4", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # DownTee
createEntry (content=u"\u22A3", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # LeftTee
createEntry (content=u"\u22A2", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # RightTee
# Commented out: collides with DoubleRightArrow
# createEntry (content=u"\u21D2", form=u"infix", stretchy=u"true", scaling="horizontal", lspace=u"thickmathspace", rspace=u"thickmathspace") # Implies
createEntry (content=u"\u2970", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # RoundImplies
createEntry (content=u"|", form=u"infix", stretchy=u"true", scaling="vertical", lspace=u"thickmathspace", rspace=u"thickmathspace")
createEntry (content=u"||", form=u"infix", lspace=u"mediummathspace", rspace=u"mediummathspace")
createEntry (content=u"\u2A54", form=u"infix", stretchy=u"true", scaling="uniform", lspace=u"mediummathspace", rspace=u"mediummathspace") # Or
createEntry (content=u"&&", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace")
createEntry (content=u"\u2A53", form=u"infix", stretchy=u"true", scaling="uniform", lspace=u"mediummathspace", rspace=u"mediummathspace") # And
createEntry (content=u"&", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace")
createEntry (content=u"!", form=u"prefix", lspace=u"0em", rspace=u"thickmathspace")
createEntry (content=u"\u2AEC", form=u"prefix", lspace=u"0em", rspace=u"thickmathspace") # Not
createEntry (content=u"\u2203", form=u"prefix", lspace=u"0em", rspace=u"thickmathspace") # Exists
createEntry (content=u"\u2200", form=u"prefix", lspace=u"0em", rspace=u"thickmathspace") # ForAll
createEntry (content=u"\u2204", form=u"prefix", lspace=u"0em", rspace=u"thickmathspace") # NotExists
createEntry (content=u"\u2208", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # Element
createEntry (content=u"\u2209", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # NotElement
createEntry (content=u"\u220C", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # NotReverseElement
createEntry (content=u"\u228F\u0338", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # NotSquareSubset
createEntry (content=u"\u22E2", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # NotSquareSubsetEqual
createEntry (content=u"\u2290\u0338", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # NotSquareSuperset
createEntry (content=u"\u22E3", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # NotSquareSupersetEqual
createEntry (content=u"\u2282\u20D2", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # NotSubset
createEntry (content=u"\u2288", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # NotSubsetEqual
createEntry (content=u"\u2283\u20D2", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # NotSuperset
createEntry (content=u"\u2289", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # NotSupersetEqual
createEntry (content=u"\u220B", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # ReverseElement
createEntry (content=u"\u228F", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # SquareSubset
createEntry (content=u"\u2291", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # SquareSubsetEqual
createEntry (content=u"\u2290", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # SquareSuperset
createEntry (content=u"\u2292", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # SquareSupersetEqual
createEntry (content=u"\u22D0", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # Subset
createEntry (content=u"\u2286", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # SubsetEqual
createEntry (content=u"\u2283", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # Superset
createEntry (content=u"\u2287", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # SupersetEqual
createEntry (content=u"\u21D0", form=u"infix", stretchy=u"true", scaling="horizontal", lspace=u"thickmathspace", rspace=u"thickmathspace") # DoubleLeftArrow
createEntry (content=u"\u21D4", form=u"infix", stretchy=u"true", scaling="horizontal", lspace=u"thickmathspace", rspace=u"thickmathspace") # DoubleLeftRightArrow
createEntry (content=u"\u21D2", form=u"infix", stretchy=u"true", scaling="horizontal", lspace=u"thickmathspace", rspace=u"thickmathspace") # DoubleRightArrow
createEntry (content=u"\u2950", form=u"infix", stretchy=u"true", scaling="horizontal", lspace=u"thickmathspace", rspace=u"thickmathspace") # DownLeftRightVector
createEntry (content=u"\u295E", form=u"infix", stretchy=u"true", scaling="horizontal", lspace=u"thickmathspace", rspace=u"thickmathspace") # DownLeftTeeVector
createEntry (content=u"\u21BD", form=u"infix", stretchy=u"true", scaling="horizontal", lspace=u"thickmathspace", rspace=u"thickmathspace") # DownLeftVector
createEntry (content=u"\u2956", form=u"infix", stretchy=u"true", scaling="horizontal", lspace=u"thickmathspace", rspace=u"thickmathspace") # DownLeftVectorBar
createEntry (content=u"\u295F", form=u"infix", stretchy=u"true", scaling="horizontal", lspace=u"thickmathspace", rspace=u"thickmathspace") # DownRightTeeVector
createEntry (content=u"\u21C1", form=u"infix", stretchy=u"true", scaling="horizontal", lspace=u"thickmathspace", rspace=u"thickmathspace") # DownRightVector
createEntry (content=u"\u2957", form=u"infix", stretchy=u"true", scaling="horizontal", lspace=u"thickmathspace", rspace=u"thickmathspace") # DownRightVectorBar
createEntry (content=u"\u2190", form=u"infix", stretchy=u"true", scaling="horizontal", lspace=u"thickmathspace", rspace=u"thickmathspace") # LeftArrow
createEntry (content=u"\u21E4", form=u"infix", stretchy=u"true", scaling="horizontal", lspace=u"thickmathspace", rspace=u"thickmathspace") # LeftArrowBar
createEntry (content=u"\u21C6", form=u"infix", stretchy=u"true", scaling="horizontal", lspace=u"thickmathspace", rspace=u"thickmathspace") # LeftArrowRightArrow
createEntry (content=u"\u2194", form=u"infix", stretchy=u"true", scaling="horizontal", lspace=u"thickmathspace", rspace=u"thickmathspace") # LeftRightArrow
createEntry (content=u"\u294E", form=u"infix", stretchy=u"true", scaling="horizontal", lspace=u"thickmathspace", rspace=u"thickmathspace") # LeftRightVector
createEntry (content=u"\u21A4", form=u"infix", stretchy=u"true", scaling="horizontal", lspace=u"thickmathspace", rspace=u"thickmathspace") # LeftTeeArrow
createEntry (content=u"\u295A", form=u"infix", stretchy=u"true", scaling="horizontal", lspace=u"thickmathspace", rspace=u"thickmathspace") # LeftTeeVector
createEntry (content=u"\u21BC", form=u"infix", stretchy=u"true", scaling="horizontal", lspace=u"thickmathspace", rspace=u"thickmathspace") # LeftVector
createEntry (content=u"\u2952", form=u"infix", stretchy=u"true", scaling="horizontal", lspace=u"thickmathspace", rspace=u"thickmathspace") # LeftVectorBar
createEntry (content=u"\u2199", form=u"infix", stretchy=u"true", scaling="horizontal", lspace=u"thickmathspace", rspace=u"thickmathspace") # LowerLeftArrow
createEntry (content=u"\u2198", form=u"infix", stretchy=u"true", scaling="horizontal", lspace=u"thickmathspace", rspace=u"thickmathspace") # LowerRightArrow
createEntry (content=u"\u2192", form=u"infix", stretchy=u"true", scaling="horizontal", lspace=u"thickmathspace", rspace=u"thickmathspace") # RightArrow
createEntry (content=u"\u21E5", form=u"infix", stretchy=u"true", scaling="horizontal", lspace=u"thickmathspace", rspace=u"thickmathspace") # RightArrowBar
createEntry (content=u"\u21C4", form=u"infix", stretchy=u"true", scaling="horizontal", lspace=u"thickmathspace", rspace=u"thickmathspace") # RightArrowLeftArrow
createEntry (content=u"\u21A6", form=u"infix", stretchy=u"true", scaling="horizontal", lspace=u"thickmathspace", rspace=u"thickmathspace") # RightTeeArrow
createEntry (content=u"\u295B", form=u"infix", stretchy=u"true", scaling="horizontal", lspace=u"thickmathspace", rspace=u"thickmathspace") # RightTeeVector
createEntry (content=u"\u21C0", form=u"infix", stretchy=u"true", scaling="horizontal", lspace=u"thickmathspace", rspace=u"thickmathspace") # RightVector
createEntry (content=u"\u2953", form=u"infix", stretchy=u"true", scaling="horizontal", lspace=u"thickmathspace", rspace=u"thickmathspace") # RightVectorBar
# Commented out: collides with LeftArrow
# createEntry (content=u"\u2190", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # ShortLeftArrow
# Commented out: collides with RightArrow
# createEntry (content=u"\u2192", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # ShortRightArrow
createEntry (content=u"\u2196", form=u"infix", stretchy=u"true", scaling="uniform", lspace=u"thickmathspace", rspace=u"thickmathspace") # UpperLeftArrow
createEntry (content=u"\u2197", form=u"infix", stretchy=u"true", scaling="uniform", lspace=u"thickmathspace", rspace=u"thickmathspace") # UpperRightArrow
createEntry (content=u"=", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace")
createEntry (content=u"<", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace")
createEntry (content=u">", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace")
createEntry (content=u"!=", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace")
createEntry (content=u"==", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace")
createEntry (content=u"<=", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace")
createEntry (content=u">=", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace")
createEntry (content=u"\u2261", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # Congruent
createEntry (content=u"\u224D", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # CupCap
createEntry (content=u"\u2250", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # DotEqual
createEntry (content=u"\u2225", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # DoubleVerticalBar
createEntry (content=u"\u2A75", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # Equal
createEntry (content=u"\u2242", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # EqualTilde
createEntry (content=u"\u21CC", form=u"infix", stretchy=u"true", scaling="horizontal", lspace=u"thickmathspace", rspace=u"thickmathspace") # Equilibrium
createEntry (content=u"\u2265", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # GreaterEqual
createEntry (content=u"\u22DB", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # GreaterEqualLess
createEntry (content=u"\u2267", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # GreaterFullEqual
createEntry (content=u"\u2AA2", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # GreaterGreater
createEntry (content=u"\u2277", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # GreaterLess
createEntry (content=u"\u2A7E", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # GreaterSlantEqual
createEntry (content=u"\u2273", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # GreaterTilde
createEntry (content=u"\u224E", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # HumpDownHump
createEntry (content=u"\u224F", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # HumpEqual
createEntry (content=u"\u22B2", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # LeftTriangle
createEntry (content=u"\u29CF", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # LeftTriangleBar
createEntry (content=u"\u22B4", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # LeftTriangleEqual
createEntry (content=u"\u2264", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # le
createEntry (content=u"\u22DA", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # LessEqualGreater
createEntry (content=u"\u2266", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # LessFullEqual
createEntry (content=u"\u2276", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # LessGreater
createEntry (content=u"\u2AA1", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # LessLess
createEntry (content=u"\u2A7D", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # LessSlantEqual
createEntry (content=u"\u2272", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # LessTilde
createEntry (content=u"\u226B", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # NestedGreaterGreater
createEntry (content=u"\u226A", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # NestedLessLess
createEntry (content=u"\u2262", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # NotCongruent
createEntry (content=u"\u226D", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # NotCupCap
createEntry (content=u"\u2226", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # NotDoubleVerticalBar
createEntry (content=u"\u2260", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # NotEqual
createEntry (content=u"\u2242\u0338", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # NotEqualTilde
createEntry (content=u"\u226F", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # NotGreater
createEntry (content=u"\u2271", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # NotGreaterEqual
createEntry (content=u"\u2266\u0338", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # NotGreaterFullEqual
createEntry (content=u"\u226B\u0338", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # NotGreaterGreater
createEntry (content=u"\u2279", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # NotGreaterLess
createEntry (content=u"\u2A7E\u0338", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # NotGreaterSlantEqual
createEntry (content=u"\u2275", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # NotGreaterTilde
createEntry (content=u"\u224E\u0338", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # NotHumpDownHump
createEntry (content=u"\u224F\u0338", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # NotHumpEqual
createEntry (content=u"\u22EA", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # NotLeftTriangle
createEntry (content=u"\u29CF\u0338", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # NotLeftTriangleBar
createEntry (content=u"\u22EC", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # NotLeftTriangleEqual
createEntry (content=u"\u226E", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # NotLess
createEntry (content=u"\u2270", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # NotLessEqual
createEntry (content=u"\u2278", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # NotLessGreater
createEntry (content=u"\u226A\u0338", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # NotLessLess
createEntry (content=u"\u2A7D\u0338", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # NotLessSlantEqual
createEntry (content=u"\u2274", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # NotLessTilde
createEntry (content=u"\u2AA2\u0338", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # NotNestedGreaterGreater
createEntry (content=u"\u2AA1\u0338", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # NotNestedLessLess
createEntry (content=u"\u2280", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # NotPrecedes
createEntry (content=u"\u2AAF\u0338", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # NotPrecedesEqual
createEntry (content=u"\u22E0", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # NotPrecedesSlantEqual
createEntry (content=u"\u22EB", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # NotRightTriangle
createEntry (content=u"\u29D0\u0338", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # NotRightTriangleBar
createEntry (content=u"\u22ED", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # NotRightTriangleEqual
createEntry (content=u"\u2281", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # NotSucceeds
createEntry (content=u"\u2AB0\u0338", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # NotSucceedsEqual
createEntry (content=u"\u22E1", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # NotSucceedsSlantEqual
createEntry (content=u"\u227F\u0338", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # NotSucceedsTilde
createEntry (content=u"\u2241", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # NotTilde
createEntry (content=u"\u2244", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # NotTildeEqual
createEntry (content=u"\u2247", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # NotTildeFullEqual
createEntry (content=u"\u2249", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # NotTildeTilde
createEntry (content=u"\u2224", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # NotVerticalBar
createEntry (content=u"\u227A", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # Precedes
createEntry (content=u"\u2AAF", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # PrecedesEqual
createEntry (content=u"\u227C", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # PrecedesSlantEqual
createEntry (content=u"\u227E", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # PrecedesTilde
createEntry (content=u"\u2237", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # Proportion
createEntry (content=u"\u221D", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # Proportional
createEntry (content=u"\u21CB", form=u"infix", stretchy=u"true", scaling="horizontal", lspace=u"thickmathspace", rspace=u"thickmathspace") # ReverseEquilibrium
createEntry (content=u"\u22B3", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # RightTriangle
createEntry (content=u"\u29D0", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # RightTriangleBar
createEntry (content=u"\u22B5", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # RightTriangleEqual
createEntry (content=u"\u227B", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # Succeeds
createEntry (content=u"\u2AB0", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # SucceedsEqual
createEntry (content=u"\u227D", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # SucceedsSlantEqual
createEntry (content=u"\u227F", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # SucceedsTilde
createEntry (content=u"\u223C", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # Tilde
createEntry (content=u"\u2243", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # TildeEqual
createEntry (content=u"\u2245", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # TildeFullEqual
createEntry (content=u"\u2248", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # TildeTilde
createEntry (content=u"\u22A5", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # UpTee
createEntry (content=u"\u2223", form=u"infix", lspace=u"thickmathspace", rspace=u"thickmathspace") # VerticalBar
createEntry (content=u"\u2294", form=u"infix", stretchy=u"true", scaling="uniform", lspace=u"mediummathspace", rspace=u"mediummathspace") # SquareUnion
createEntry (content=u"\u22C3", form=u"infix", stretchy=u"true", scaling="uniform", lspace=u"mediummathspace", rspace=u"mediummathspace") # Union
createEntry (content=u"\u228E", form=u"infix", stretchy=u"true", scaling="uniform", lspace=u"mediummathspace", rspace=u"mediummathspace") # UnionPlus
createEntry (content=u"-", form=u"infix", lspace=u"mediummathspace", rspace=u"mediummathspace")
# Added an entry for minus sign, separate from hyphen
createEntry (content=u"\u2212", form=u"infix", lspace=u"mediummathspace", rspace=u"mediummathspace")
createEntry (content=u"+", form=u"infix", lspace=u"mediummathspace", rspace=u"mediummathspace")
createEntry (content=u"\u22C2", form=u"infix", stretchy=u"true", scaling="uniform", lspace=u"mediummathspace", rspace=u"mediummathspace") # Intersection
createEntry (content=u"\u2213", form=u"infix", lspace=u"mediummathspace", rspace=u"mediummathspace") # MinusPlus
createEntry (content=u"\u00B1", form=u"infix", lspace=u"mediummathspace", rspace=u"mediummathspace") # PlusMinus
createEntry (content=u"\u2293", form=u"infix", stretchy=u"true", scaling="uniform", lspace=u"mediummathspace", rspace=u"mediummathspace") # SquareIntersection
createEntry (content=u"\u22C1", form=u"prefix", largeop=u"true", movablelimits=u"true", stretchy=u"true", scaling="uniform", lspace=u"0em", rspace=u"thinmathspace") # Vee
createEntry (content=u"\u2296", form=u"prefix", largeop=u"true", movablelimits=u"true", lspace=u"0em", rspace=u"thinmathspace") # CircleMinus
createEntry (content=u"\u2295", form=u"prefix", largeop=u"true", movablelimits=u"true", lspace=u"0em", rspace=u"thinmathspace") # CirclePlus
createEntry (content=u"\u2211", form=u"prefix", largeop=u"true", movablelimits=u"true", stretchy=u"true", scaling="uniform", lspace=u"0em", rspace=u"thinmathspace") # Sum
createEntry (content=u"\u22C3", form=u"prefix", largeop=u"true", movablelimits=u"true", stretchy=u"true", scaling="uniform", lspace=u"0em", rspace=u"thinmathspace") # Union
createEntry (content=u"\u228E", form=u"prefix", largeop=u"true", movablelimits=u"true", stretchy=u"true", scaling="uniform", lspace=u"0em", rspace=u"thinmathspace") # UnionPlus
createEntry (content=u"lim", form=u"prefix", movablelimits=u"true", lspace=u"0em", rspace=u"thinmathspace")
createEntry (content=u"max", form=u"prefix", movablelimits=u"true", lspace=u"0em", rspace=u"thinmathspace")
createEntry (content=u"min", form=u"prefix", movablelimits=u"true", lspace=u"0em", rspace=u"thinmathspace")
createEntry (content=u"\u2296", form=u"infix", lspace=u"thinmathspace", rspace=u"thinmathspace") # CircleMinus
createEntry (content=u"\u2295", form=u"infix", lspace=u"thinmathspace", rspace=u"thinmathspace") # CirclePlus
createEntry (content=u"\u2232", form=u"prefix", largeop=u"true", stretchy=u"true", scaling="uniform", lspace=u"0em", rspace=u"0em") # ClockwiseContourIntegral
createEntry (content=u"\u222E", form=u"prefix", largeop=u"true", stretchy=u"true", scaling="uniform", lspace=u"0em", rspace=u"0em") # ContourIntegral
createEntry (content=u"\u2233", form=u"prefix", largeop=u"true", stretchy=u"true", scaling="uniform", lspace=u"0em", rspace=u"0em") # CounterClockwiseContourIntegral
createEntry (content=u"\u222F", form=u"prefix", largeop=u"true", stretchy=u"true", scaling="uniform", lspace=u"0em", rspace=u"0em") # DoubleContourIntegral
createEntry (content=u"\u222B", form=u"prefix", largeop=u"true", stretchy=u"true", scaling="uniform", lspace=u"0em", rspace=u"0em") # Integral
createEntry (content=u"\u22D3", form=u"infix", lspace=u"thinmathspace", rspace=u"thinmathspace") # Cup
createEntry (content=u"\u22D2", form=u"infix", lspace=u"thinmathspace", rspace=u"thinmathspace") # Cap
createEntry (content=u"\u2240", form=u"infix", lspace=u"thinmathspace", rspace=u"thinmathspace") # VerticalTilde
createEntry (content=u"\u22C0", form=u"prefix", largeop=u"true", movablelimits=u"true", stretchy=u"true", scaling="uniform", lspace=u"0em", rspace=u"thinmathspace") # Wedge
createEntry (content=u"\u2297", form=u"prefix", largeop=u"true", movablelimits=u"true", lspace=u"0em", rspace=u"thinmathspace") # CircleTimes
createEntry (content=u"\u2210", form=u"prefix", largeop=u"true", movablelimits=u"true", stretchy=u"true", scaling="uniform", lspace=u"0em", rspace=u"thinmathspace") # Coproduct
createEntry (content=u"\u220F", form=u"prefix", largeop=u"true", movablelimits=u"true", stretchy=u"true", scaling="uniform", lspace=u"0em", rspace=u"thinmathspace") # Product
createEntry (content=u"\u22C2", form=u"prefix", largeop=u"true", movablelimits=u"true", stretchy=u"true", scaling="uniform", lspace=u"0em", rspace=u"thinmathspace") # Intersection
createEntry (content=u"\u2210", form=u"infix", lspace=u"thinmathspace", rspace=u"thinmathspace") # Coproduct
createEntry (content=u"\u22C6", form=u"infix", lspace=u"thinmathspace", rspace=u"thinmathspace") # Star
createEntry (content=u"\u2299", form=u"prefix", largeop=u"true", movablelimits=u"true", lspace=u"0em", rspace=u"thinmathspace") # CircleDot
createEntry (content=u"*", form=u"infix", lspace=u"thinmathspace", rspace=u"thinmathspace")
createEntry (content=u"\u2062", form=u"infix", lspace=u"0em", rspace=u"0em") # InvisibleTimes
createEntry (content=u"\u00B7", form=u"infix", lspace=u"thinmathspace", rspace=u"thinmathspace") # CenterDot
createEntry (content=u"\u2297", form=u"infix", lspace=u"thinmathspace", rspace=u"thinmathspace") # CircleTimes
createEntry (content=u"\u22C1", form=u"infix", lspace=u"thinmathspace", rspace=u"thinmathspace") # Vee
createEntry (content=u"\u22C0", form=u"infix", lspace=u"thinmathspace", rspace=u"thinmathspace") # Wedge
createEntry (content=u"\u22C4", form=u"infix", lspace=u"thinmathspace", rspace=u"thinmathspace") # Diamond
createEntry (content=u"\u2216", form=u"infix", stretchy=u"true", scaling="uniform", lspace=u"thinmathspace", rspace=u"thinmathspace") # Backslash
createEntry (content=u"/", form=u"infix", stretchy=u"true", scaling="uniform", lspace=u"thinmathspace", rspace=u"thinmathspace")
createEntry (content=u"-", form=u"prefix", lspace=u"0em", rspace=u"veryverythinmathspace")
# Added an entry for minus sign, separate from hyphen
createEntry (content=u"\u2212", form=u"prefix", lspace=u"0em", rspace=u"veryverythinmathspace")
createEntry (content=u"+", form=u"prefix", lspace=u"0em", rspace=u"veryverythinmathspace")
createEntry (content=u"\u2213", form=u"prefix", lspace=u"0em", rspace=u"veryverythinmathspace") # MinusPlus
createEntry (content=u"\u00B1", form=u"prefix", lspace=u"0em", rspace=u"veryverythinmathspace") # PlusMinus
createEntry (content=u".", form=u"infix", lspace=u"0em", rspace=u"0em")
createEntry (content=u"\u2A2F", form=u"infix", lspace=u"verythinmathspace", rspace=u"verythinmathspace") # Cross
createEntry (content=u"**", form=u"infix", lspace=u"verythinmathspace", rspace=u"verythinmathspace")
createEntry (content=u"\u2299", form=u"infix", lspace=u"verythinmathspace", rspace=u"verythinmathspace") # CircleDot
createEntry (content=u"\u2218", form=u"infix", lspace=u"verythinmathspace", rspace=u"verythinmathspace") # SmallCircle
createEntry (content=u"\u25A1", form=u"prefix", lspace=u"0em", rspace=u"verythinmathspace") # Square
createEntry (content=u"\u2207", form=u"prefix", lspace=u"0em", rspace=u"verythinmathspace") # Del
createEntry (content=u"\u2202", form=u"prefix", lspace=u"0em", rspace=u"verythinmathspace") # PartialD
createEntry (content=u"\u2145", form=u"prefix", lspace=u"0em", rspace=u"verythinmathspace") # CapitalDifferentialD
createEntry (content=u"\u2146", form=u"prefix", lspace=u"0em", rspace=u"verythinmathspace") # DifferentialD
createEntry (content=u"\u221A", form=u"prefix", stretchy=u"true", scaling="uniform", lspace=u"0em", rspace=u"verythinmathspace") # Sqrt
createEntry (content=u"\u21D3", form=u"infix", stretchy=u"true", scaling="vertical", lspace=u"verythinmathspace", rspace=u"verythinmathspace") # DoubleDownArrow
createEntry (content=u"\u27F8", form=u"infix", stretchy=u"true", scaling="horizontal", lspace=u"verythinmathspace", rspace=u"verythinmathspace") # DoubleLongLeftArrow
createEntry (content=u"\u27FA", form=u"infix", stretchy=u"true", scaling="horizontal", lspace=u"verythinmathspace", rspace=u"verythinmathspace") # DoubleLongLeftRightArrow
createEntry (content=u"\u27F9", form=u"infix", stretchy=u"true", scaling="horizontal", lspace=u"verythinmathspace", rspace=u"verythinmathspace") # DoubleLongRightArrow
createEntry (content=u"\u21D1", form=u"infix", stretchy=u"true", scaling="vertical", lspace=u"verythinmathspace", rspace=u"verythinmathspace") # DoubleUpArrow
createEntry (content=u"\u21D5", form=u"infix", stretchy=u"true", scaling="vertical", lspace=u"verythinmathspace", rspace=u"verythinmathspace") # DoubleUpDownArrow
createEntry (content=u"\u2193", form=u"infix", stretchy=u"true", scaling="vertical", lspace=u"verythinmathspace", rspace=u"verythinmathspace") # DownArrow
createEntry (content=u"\u2913", form=u"infix", stretchy=u"true", scaling="vertical", lspace=u"verythinmathspace", rspace=u"verythinmathspace") # DownArrowBar
createEntry (content=u"\u21F5", form=u"infix", stretchy=u"true", scaling="vertical", lspace=u"verythinmathspace", rspace=u"verythinmathspace") # DownArrowUpArrow
createEntry (content=u"\u21A7", form=u"infix", stretchy=u"true", scaling="vertical", lspace=u"verythinmathspace", rspace=u"verythinmathspace") # DownTeeArrow
createEntry (content=u"\u2961", form=u"infix", stretchy=u"true", scaling="uniform", lspace=u"verythinmathspace", rspace=u"verythinmathspace") # LeftDownTeeVector
createEntry (content=u"\u21C3", form=u"infix", stretchy=u"true", scaling="uniform", lspace=u"verythinmathspace", rspace=u"verythinmathspace") # LeftDownVector
createEntry (content=u"\u2959", form=u"infix", stretchy=u"true", scaling="uniform", lspace=u"verythinmathspace", rspace=u"verythinmathspace") # LeftDownVectorBar
createEntry (content=u"\u2951", form=u"infix", stretchy=u"true", scaling="uniform", lspace=u"verythinmathspace", rspace=u"verythinmathspace") # LeftUpDownVector
createEntry (content=u"\u2960", form=u"infix", stretchy=u"true", scaling="uniform", lspace=u"verythinmathspace", rspace=u"verythinmathspace") # LeftUpTeeVector
createEntry (content=u"\u21BF", form=u"infix", stretchy=u"true", scaling="uniform", lspace=u"verythinmathspace", rspace=u"verythinmathspace") # LeftUpVector
createEntry (content=u"\u2958", form=u"infix", stretchy=u"true", scaling="uniform", lspace=u"verythinmathspace", rspace=u"verythinmathspace") # LeftUpVectorBar
createEntry (content=u"\u27F5", form=u"infix", stretchy=u"true", scaling="horizontal", lspace=u"verythinmathspace", rspace=u"verythinmathspace") # LongLeftArrow
createEntry (content=u"\u27F7", form=u"infix", stretchy=u"true", scaling="horizontal", lspace=u"verythinmathspace", rspace=u"verythinmathspace") # LongLeftRightArrow
createEntry (content=u"\u27F6", form=u"infix", stretchy=u"true", scaling="horizontal", lspace=u"verythinmathspace", rspace=u"verythinmathspace") # LongRightArrow
createEntry (content=u"\u296F", form=u"infix", stretchy=u"true", scaling="horizontal", lspace=u"verythinmathspace", rspace=u"verythinmathspace") # ReverseUpEquilibrium
createEntry (content=u"\u295D", form=u"infix", stretchy=u"true", scaling="horizontal", lspace=u"verythinmathspace", rspace=u"verythinmathspace") # RightDownTeeVector
createEntry (content=u"\u21C2", form=u"infix", stretchy=u"true", scaling="horizontal", lspace=u"verythinmathspace", rspace=u"verythinmathspace") # RightDownVector
createEntry (content=u"\u2955", form=u"infix", stretchy=u"true", scaling="horizontal", lspace=u"verythinmathspace", rspace=u"verythinmathspace") # RightDownVectorBar
createEntry (content=u"\u294F", form=u"infix", stretchy=u"true", scaling="horizontal", lspace=u"verythinmathspace", rspace=u"verythinmathspace") # RightUpDownVector
createEntry (content=u"\u295C", form=u"infix", stretchy=u"true", scaling="horizontal", lspace=u"verythinmathspace", rspace=u"verythinmathspace") # RightUpTeeVector
createEntry (content=u"\u21BE", form=u"infix", stretchy=u"true", scaling="horizontal", lspace=u"verythinmathspace", rspace=u"verythinmathspace") # RightUpVector
createEntry (content=u"\u2954", form=u"infix", stretchy=u"true", scaling="horizontal", lspace=u"verythinmathspace", rspace=u"verythinmathspace") # RightUpVectorBar
# Commented out: collides with DownArrow
# createEntry (content=u"\u2193", form=u"infix", lspace=u"verythinmathspace", rspace=u"verythinmathspace") # ShortDownArrow
# Commented out: collides with UpArrow
# createEntry (content=u"\u2191", form=u"infix", lspace=u"verythinmathspace", rspace=u"verythinmathspace") # ShortUpArrow
createEntry (content=u"\u2191", form=u"infix", stretchy=u"true", scaling="vertical", lspace=u"verythinmathspace", rspace=u"verythinmathspace") # UpArrow
createEntry (content=u"\u2912", form=u"infix", stretchy=u"true", scaling="vertical", lspace=u"verythinmathspace", rspace=u"verythinmathspace") # UpArrowBar
createEntry (content=u"\u21C5", form=u"infix", stretchy=u"true", scaling="vertical", lspace=u"verythinmathspace", rspace=u"verythinmathspace") # UpArrowDownArrow
createEntry (content=u"\u2195", form=u"infix", stretchy=u"true", scaling="vertical", lspace=u"verythinmathspace", rspace=u"verythinmathspace") # UpDownArrow
createEntry (content=u"\u296E", form=u"infix", stretchy=u"true", scaling="vertical", lspace=u"verythinmathspace", rspace=u"verythinmathspace") # UpEquilibrium
createEntry (content=u"\u21A5", form=u"infix", stretchy=u"true", scaling="vertical", lspace=u"verythinmathspace", rspace=u"verythinmathspace") # UpTeeArrow
createEntry (content=u"^", form=u"infix", lspace=u"verythinmathspace", rspace=u"verythinmathspace")
createEntry (content=u"<>", form=u"infix", lspace=u"verythinmathspace", rspace=u"verythinmathspace")
createEntry (content=u"'", form=u"postfix", lspace=u"verythinmathspace", rspace=u"0em")
# Added an entry for prime, separate from apostrophe
createEntry (content=u"\u2032", form=u"postfix", lspace=u"verythinmathspace", rspace=u"0em")
createEntry (content=u"!", form=u"postfix", lspace=u"verythinmathspace", rspace=u"0em")
createEntry (content=u"!!", form=u"postfix", lspace=u"verythinmathspace", rspace=u"0em")
createEntry (content=u"~", form=u"infix", lspace=u"verythinmathspace", rspace=u"verythinmathspace")
createEntry (content=u"@", form=u"infix", lspace=u"verythinmathspace", rspace=u"verythinmathspace")
createEntry (content=u"--", form=u"postfix", lspace=u"verythinmathspace", rspace=u"0em")
createEntry (content=u"--", form=u"prefix", lspace=u"0em", rspace=u"verythinmathspace")
createEntry (content=u"++", form=u"postfix", lspace=u"verythinmathspace", rspace=u"0em")
createEntry (content=u"++", form=u"prefix", lspace=u"0em", rspace=u"verythinmathspace")
createEntry (content=u"\u2061", form=u"infix", lspace=u"0em", rspace=u"0em") # ApplyFunction
createEntry (content=u"?", form=u"infix", lspace=u"verythinmathspace", rspace=u"verythinmathspace")
createEntry (content=u"_", form=u"infix", lspace=u"verythinmathspace", rspace=u"verythinmathspace")
createEntry (content=u"\u02D8", form=u"postfix", accent=u"true", lspace=u"0em", rspace=u"0em") # Breve
createEntry (content=u"\u00B8", form=u"postfix", accent=u"true", lspace=u"0em", rspace=u"0em") # Cedilla
createEntry (content=u"`", form=u"postfix", accent=u"true", lspace=u"0em", rspace=u"0em") # DiacriticalGrave
createEntry (content=u"\u02D9", form=u"postfix", accent=u"true", lspace=u"0em", rspace=u"0em") # DiacriticalDot
createEntry (content=u"\u02DD", form=u"postfix", accent=u"true", lspace=u"0em", rspace=u"0em") # DiacriticalDoubleAcute
createEntry (content=u"\u2190", form=u"postfix", accent=u"true", stretchy=u"true", scaling="horizontal", lspace=u"0em", rspace=u"0em") # LeftArrow
createEntry (content=u"\u2194", form=u"postfix", accent=u"true", stretchy=u"true", scaling="horizontal", lspace=u"0em", rspace=u"0em") # LeftRightArrow
createEntry (content=u"\u294E", form=u"postfix", accent=u"true", stretchy=u"true", scaling="horizontal", lspace=u"0em", rspace=u"0em") # LeftRightVector
createEntry (content=u"\u21BC", form=u"postfix", accent=u"true", stretchy=u"true", scaling="horizontal", lspace=u"0em", rspace=u"0em") # LeftVector
createEntry (content=u"\u00B4", form=u"postfix", accent=u"true", lspace=u"0em", rspace=u"0em") # DiacriticalAcute
createEntry (content=u"\u2192", form=u"postfix", accent=u"true", stretchy=u"true", scaling="horizontal", lspace=u"0em", rspace=u"0em") # RightArrow
createEntry (content=u"\u21C0", form=u"postfix", accent=u"true", stretchy=u"true", scaling="horizontal", lspace=u"0em", rspace=u"0em") # RightVector
createEntry (content=u"\u02DC", form=u"postfix", accent=u"true", stretchy=u"true", scaling="horizontal", lspace=u"0em", rspace=u"0em") # DiacriticalTilde
createEntry (content=u"\u00A8", form=u"postfix", accent=u"true", lspace=u"0em", rspace=u"0em") # DoubleDot
createEntry (content=u"\u0311", form=u"postfix", accent=u"true", lspace=u"0em", rspace=u"0em") # DownBreve
createEntry (content=u"\u02C7", form=u"postfix", accent=u"true", stretchy=u"true", scaling="horizontal", lspace=u"0em", rspace=u"0em") # Hacek
createEntry (content=u"^", form=u"postfix", accent=u"true", stretchy=u"true", scaling="horizontal", lspace=u"0em", rspace=u"0em") # Hat
createEntry (content=u"\u00AF", form=u"postfix", accent=u"true", stretchy=u"true", scaling="horizontal", lspace=u"0em", rspace=u"0em") # OverBar
createEntry (content=u"\uFE37", form=u"postfix", accent=u"true", stretchy=u"true", scaling="horizontal", lspace=u"0em", rspace=u"0em") # OverBrace
createEntry (content=u"\u23B4", form=u"postfix", accent=u"true", stretchy=u"true", scaling="horizontal", lspace=u"0em", rspace=u"0em") # OverBracket
createEntry (content=u"\uFE35", form=u"postfix", accent=u"true", stretchy=u"true", scaling="horizontal", lspace=u"0em", rspace=u"0em") # OverParenthesis
createEntry (content=u"\u20DB", form=u"postfix", accent=u"true", lspace=u"0em", rspace=u"0em") # TripleDot
createEntry (content=u"\u0332", form=u"postfix", accent=u"true", stretchy=u"true", scaling="horizontal", lspace=u"0em", rspace=u"0em") # UnderBar
createEntry (content=u"\uFE38", form=u"postfix", accent=u"true", stretchy=u"true", scaling="horizontal", lspace=u"0em", rspace=u"0em") # UnderBrace
createEntry (content=u"\u23B5", form=u"postfix", accent=u"true", stretchy=u"true", scaling="horizontal", lspace=u"0em", rspace=u"0em") # UnderBracket
createEntry (content=u"\uFE36", form=u"postfix", accent=u"true", stretchy=u"true", scaling="horizontal", lspace=u"0em", rspace=u"0em") # UnderParenthesis
