"""Methods to set up the context for a MathML tree node.

The module contains two kinds of methods to set up context:
   - context creators process the context of the current node;
   - child context setters alter the context of a child."""
   
import sys, mathnode, operators

#######################################################################
#### CONTEXT CREATORS 

def default_context (node): 
    """Default context creator for a MathML tree node."""
    if node.parent is not None:         
        node.mathsize = node.parent.mathsize
        node.fontSize = node.parent.fontSize
        node.metriclist = node.parent.metriclist
        node.scriptlevel = node.parent.scriptlevel
        node.tightspaces = node.parent.tightspaces
        node.displaystyle = node.parent.displaystyle
        node.color = node.parent.color

        node.fontfamilies = node.parent.fontfamilies
        node.fontweight = node.parent.fontweight
        node.fontstyle = node.parent.fontstyle

        node.defaults = node.parent.defaults
        node.parent.makeChildContext(node)
    else:
        node.mathsize = node.parseLength(node.defaults[u"mathsize"])
        node.fontSize = node.mathsize
        node.metriclist = None
        node.scriptlevel = node.parseInt(node.defaults[u"scriptlevel"])
        node.tightspaces = False
        node.displaystyle = (node.defaults[u"displaystyle"] == u"true")
        node.color = node.defaults[u"mathcolor"]

        defaultVariant = node.config.variants.get(node.defaults[u"mathvariant"])
        if defaultVariant is None:
            raise sax.SAXException("Default mathvariant not defined in configuration file: configuration is unusable")
        (node.fontweight, node.fontstyle, node.fontfamilies) = defaultVariant
        
    processFontAttributes(node)   

    # Set the rest of properties that need immediate initialization
    node.width = 0
    node.height = 0
    node.depth = 0
    node.ascender = 0
    node.descender = 0
    node.leftspace = 0
    node.rightspace = 0
    node.alignToAxis = False
    node.base = node
    node.core = node
    node.stretchy = False
    node.accent = False
    node.moveLimits = False
    node.textShift = 0
    node.textStretch = 1
    node.leftBearing = 0
    node.rightBearing = 0
    node.isSpace = False
    # Reset metrics list to None (so far, we used metrics from the parent)
    node.metriclist = None
    node.nominalMetric = None


def context_math(node):
    default_context(node)
    # Display style: set differently on 'math'
    attr = node.attributes.get(u"display")
    if attr is not None:
       node.displaystyle = (attr == u"block")
    else:
       attr = node.attributes.get(u"mode")
       node.displaystyle = (attr == u"display")         


def context_mstyle(node):
    default_context(node)
    # Avoid redefinition of mathsize - it is inherited anyway.
    # This serves to preserve values of 'big', 'small', and 'normal'
    # throughout the MathML instance.
    if node.attributes and u"mathsize" in node.attributes.keys():
        del node.attributes[u"mathsize"] 
    if node.attributes:
        node.defaults = node.defaults.copy()
        node.defaults.update(node.attributes)
    

def context_mtable(node):
    default_context(node)
    # Display style: no inheritance, default is 'false' unless redefined in 'mstyle'
    node.displaystyle = (node.getProperty(u"displaystyle") == u"true")


def context_mi(node):
    # If the identifier is a single character, make it italic by default.
    # Don't forget surrogate pairs here!
    if len(node.text) == 1 or ( len(node.text) == 2 
                            and mathnode.isHighSurrogate(node.text[0])
                            and mathnode.isLowSurrogate(node.text[1]) ):
        node.attributes.setdefault(u"fontstyle", u"italic")
    default_context(node)


def context_mo(node):
    # Apply special formatting to operators
    extra_style = node.config.opstyles.get(node.text);
    if extra_style:
        for (prop, value) in extra_style.items():    
            node.attributes.setdefault(prop, value)

    # Consult the operator dictionary, and set the appropriate defaults
    form = u"infix"
    if node.parent is None: pass
    elif node.parent.elementName in [u"mrow", u"mstyle", u"msqrt", 
                                     u"merror", u"mpadded", u"mphantom",
                                     u"menclose", u"mtd", u"math"]:
        def isNonSpaceNode(x): return x.elementName != u"mspace"
        
        prevSiblings = node.parent.children[:node.nodeIndex]
        prevSiblings = filter (isNonSpaceNode, prevSiblings)
        
        nextSiblings = node.parent.children[node.nodeIndex+1:]
        nextSiblings = filter (isNonSpaceNode, nextSiblings)
        
        if len(prevSiblings) == 0 and len(nextSiblings) > 0: form = u"prefix"
        if len(nextSiblings) == 0 and len(prevSiblings) > 0: form = u"postfix"
 
    form = node.attributes.get(u"form", form)
    
    node.opdefaults = operators.lookup(node.text, form)        
    default_context(node)
    stretchyattr = node.getProperty(u"stretchy", node.opdefaults.get(u"stretchy"))        
    node.stretchy = (stretchyattr == u"true")
    symmetricattr = node.getProperty(u"symmetric", node.opdefaults.get(u"symmetric"))        
    node.symmetric = (symmetricattr == u"true")
    node.scaling = node.opdefaults.get(u"scaling") 
    if not node.tightspaces:
        lspaceattr = node.getProperty(u"lspace", node.opdefaults.get(u"lspace"))
        node.leftspace = node.parseSpace(lspaceattr)
        rspaceattr = node.getProperty(u"rspace", node.opdefaults.get(u"rspace"))
        node.rightspace = node.parseSpace(rspaceattr)

    if node.displaystyle:
        value = node.opdefaults.get(u"largeop")
        if node.getProperty(u"largeop", value) == u"true": 
            node.fontSize *= 1.41    
    else:
        value = node.opdefaults.get(u"movablelimits")
        node.moveLimits = (node.getProperty(u"movablelimits", value) == u"true")


def processFontAttributes(node):
    attr = node.attributes.get(u"displaystyle")
    if attr is not None: node.displaystyle = (attr == u"true")

    scriptlevelattr = node.attributes.get(u"scriptlevel")
    if scriptlevelattr is not None:
        scriptlevelattr = scriptlevelattr.strip()
        if scriptlevelattr.startswith(u"+"):
           node.scriptlevel += node.parseInt(scriptlevelattr[1:])
        elif scriptlevelattr.startswith(u"-"):
           node.scriptlevel -= node.parseInt(scriptlevelattr[1:])
        else:
           node.scriptlevel = node.parseInt(scriptlevelattr)
        node.scriptlevel = max(node.scriptlevel, 0)

    node.color = node.attributes.get(u"mathcolor", 
                                     node.attributes.get(u"color", node.color))        
    # Calculate font attributes
    mathvariantattr = node.attributes.get(u"mathvariant")
    if mathvariantattr is not None:
        mathvariant = node.config.variants.get(mathvariantattr)
        if mathvariant is None:
            node.error("Ignored mathvariant attribute: value '"+str(mathvariantattr)+"' not defined in the font configuration file")
        else:    
            (node.fontweight, node.fontstyle, node.fontfamilies) = mathvariant
    else:
        node.fontweight = node.attributes.get(u"fontweight", node.fontweight)
        node.fontstyle = node.attributes.get(u"fontstyle", node.fontstyle)
        familyattr = node.attributes.get(u"fontfamily")
        if familyattr is not None:
            node.fontfamilies = [" ".join(x.split()) for x in familyattr.split(u",")] 

    # Calculate font size
    mathsizeattr = node.attributes.get(u"mathsize")         
    if mathsizeattr is not None:
        if mathsizeattr == u"normal":
            node.mathsize = node.parseLength(node.defaults[u"mathsize"])
        elif mathsizeattr == u"big":
            node.mathsize = node.parseLength(node.defaults[u"mathsize"]) * 1.41
        elif mathsizeattr == u"small":
            node.mathsize = node.parseLength(node.defaults[u"mathsize"]) / 1.41
        else:
            mathsize = node.parseLengthOrPercent(mathsizeattr, node.mathsize)
            if mathsize > 0: 
                node.mathsize = mathsize
            else:
                node.error("Value of attribute 'mathsize' ignored - not a positive length: "+str(mathsizeattr))

    node.fontSize = node.mathsize
    if node.scriptlevel > 0:
        scriptsizemultiplier = node.parseFloat(node.defaults.get(u"scriptsizemultiplier"))
        if scriptsizemultiplier <= 0:
            node.error("Bad inherited value of 'scriptsizemultiplier' attribute: "+str(mathsizeattr)+"; using default value")
        scriptsizemultiplier = node.parseFloat(mathnode.globalDefaults.get(u"scriptsizemultiplier"))
        node.fontSize *= scriptsizemultiplier ** node.scriptlevel 

    fontsizeattr = node.attributes.get(u"fontsize")
    if fontsizeattr is not None and mathsizeattr is None:
        fontSizeOverride = node.parseLengthOrPercent(fontsizeattr, node.fontSize)            
        if fontSizeOverride > 0:
            node.mathsize *= fontSizeOverride / node.fontSize
            node.fontSize = fontSizeOverride
        else:
            node.error("Value of attribute 'fontsize' ignored - not a positive length: "+str(fontsizeattr))

    scriptminsize = node.parseLength(node.defaults.get(u"scriptminsize"))
    node.fontSize = max(node.fontSize, scriptminsize)
    node.originalFontSize = node.fontSize # save a copy - font size may change in scaling


#######################################################################
#### CHILD CONTEXT SETTERS 

def default_child_context (node, child): 
    """Default child context processing for a MathML tree node."""
    pass

    
def child_context_mfrac (node, child):
    if node.displaystyle: child.displaystyle = False
    else: child.scriptlevel += 1


def child_context_mroot (node, child):
    if child.nodeIndex == 1: 
        child.displaystyle = False
        child.scriptlevel += 2
        child.tightspaces = True


def child_context_msub (node, child): makeScriptContext(child)
def child_context_msup (node, child): makeScriptContext(child)
def child_context_msubsup (node, child): makeScriptContext(child)
def child_context_mmultiscripts (node, child): makeScriptContext(child)

    
def child_context_munder (node, child): 
    if child.nodeIndex == 1:
        makeLimitContext(node, child, u"accentunder")


def child_context_mover (node, child): 
    if child.nodeIndex == 1:
        makeLimitContext(node, child, u"accent")


def child_context_munderover (node, child): 
    if child.nodeIndex == 1:
        makeLimitContext(node, child, u"accentunder")
    if child.nodeIndex == 2:
        makeLimitContext(node, child, u"accent")


def makeScriptContext (child):
    if child.nodeIndex > 0: 
        child.displaystyle = False
        child.tightspaces = True
        child.scriptlevel += 1


def makeLimitContext (node, child, accentProperty):
    child.displaystyle = False
    child.tightspaces = True

    accentValue = node.getProperty(accentProperty)
    if accentValue is None:
        embellishments = [u"msub", u"msup", u"msubsup", 
                          u"munder", u"mover", u"munderover", u"mmultiscripts"]
        def getAccentValue(ch):
            if ch.elementName == u"mo":
                return ch.opdefaults.get(u"accent")
            elif ch.elementName in embellishments and len(ch.children) > 0:
                return getAccentValue(ch.children[0])
            else: return u"false"    
        accentValue  = getAccentValue(child)
    child.accent = (accentValue == u"true")
    if not child.accent: 
        child.scriptlevel += 1
