"""Functions to determine size and position of MathML elements"""
import sys, math, mathnode, operators, tables, enclosures

# Handy constant to draw fraction bars
defaultSlope = 1.383

def default_measure (node): pass 

def measure_none (node): pass

def measure_mprescripts (node): pass

def measure_math (node): measure_mrow (node)

def measure_mphantom (node): measure_mrow (node)

def measure_mstyle (node):
    measure_mrow(node)  # processed in the constructor

def measure_maction (node): 
    selectionattr = node.attributes.get(u"selection", u"1")
    selection = node.parseInt(selectionattr)
    node.base = None
    if selection <= 0:
        node.error("Invalid value '%s' for 'selection' attribute - not a positive integer" % selectionattr)
    elif len(node.children) == 0:        
        node.error("No valid subexpression inside maction element - element ignored" % selectionattr)
    else:
        if selection > len(node.children):
            node.error("Invalid value '%d' for 'selection' attribute - there are only %d expression descendants in the element" % (selection, len(node.children)))
            selection = 1
        setNodeBase(node, node.children[selection - 1])
        node.width = node.base.width
        node.height = node.base.height
        node.depth = node.base.depth
        node.ascender = node.base.ascender
        node.descender = node.base.descender

def measure_mpadded (node):
    createImplicitRow(node)

    def parseDimension(attr, startvalue, canUseSpaces):
        if attr.endswith(" height"):
            basevalue = node.base.height
            attr = attr [:-7]
        elif attr.endswith(" depth"):
            basevalue = node.base.depth
            attr = attr [:-6]
        elif attr.endswith(" width"):
            basevalue = node.base.width
            attr = attr [:-6]
        else: basevalue = startvalue
        
        if attr.endswith (u'%'): 
            attr = attr[:-1]
            basevalue /= 100.0
        
        if canUseSpaces:
            return node.parseSpace(attr, basevalue)
        else:
            return node.parseLength(attr, basevalue)
        
    def getDimension(attname, startvalue, canUseSpaces):
        attr = node.attributes.get(attname)
        if attr is None: return startvalue
        attr = " ".join(attr.split())
        if attr.startswith(u'+'): 
            return startvalue + parseDimension(attr[1:], startvalue, canUseSpaces)
        elif attr.startswith(u'+'): 
            return startvalue - parseDimension(attr[1:], startvalue, canUseSpaces)
        else: 
            return parseDimension(attr, startvalue, canUseSpaces)
    
    node.height = getDimension(u"height", node.base.height, False) 
    node.depth = getDimension(u"depth", node.base.depth, False)
    node.ascender = node.base.ascender
    node.descender = node.base.descender
    node.leftpadding = getDimension(u"lspace", 0, True)
    node.width = getDimension(u"width", node.base.width + node.leftpadding, True)
    if node.width < 0: node.width = 0
    node.leftspace = node.base.leftspace
    node.rightspace = node.base.rightspace
    

def measure_mfenced (node):
    old_children = node.children
    node.children = []

    # Add fences and separators, and process as a mrow
    openingFence = node.getProperty(u"open")
    openingFence = " ".join(openingFence.split())
    if len(openingFence) > 0:
        opening = mathnode.MathNode (u"mo", {u"fence": u"true", u"form": u"prefix"}, 
                                     None, node.config, node)
        opening.text = openingFence
        opening.measure()

    separators = "".join(node.getProperty(u"separators").split())
    sepindex = 0
    lastsep = len(separators) - 1 
    
    for ch in old_children:
        if len(node.children) > 1 and lastsep >= 0:
            sep = mathnode.MathNode (u"mo", {u"separator": u"true", u"form": u"infix"}, 
                                     None, node.config, node)
            sep.text = separators[sepindex]
            sep.measure()
            sepindex  = min (sepindex+1, lastsep)
        node.children.append(ch)    

    closingFence = node.getProperty(u"close")
    closingFence = " ".join(closingFence.split())
    if len(closingFence) > 0:
        closing = mathnode.MathNode (u"mo", {u"fence": u"true", u"form": u"postfix"}, 
                                     None, node.config, node)
        closing.text = closingFence
        closing.measure()

    measure_mrow(node)

def measure_mo (node): 
    # Normalize operator glyphs
    # Use minus instead of hyphen
    if node.hasGlyph(0x2212): node.text = node.text.replace(u'-', u'\u2212')
    # Use prime instead of apostrophe
    if node.hasGlyph(0x2032): node.text = node.text.replace(u'\'', u'\u2032')
    # Invisible operators produce space nodes
    if node.text in [u'\u2061', u'\u2062', u'\u2063']: node.isSpace = True
    else: node.measureText()
    
    # Align the operator along the mathematical axis for the respective font 
    node.alignToAxis = True
    node.textShift = - node.axis()
    node.height += node.textShift
    node.ascender += node.textShift
    node.depth -= node.textShift    
    node.descender -= node.textShift    

def measure_mn (node): 
    node.measureText()    

def measure_mi (node): 
    node.measureText()
        
def measure_mtext (node): 
    node.measureText()
    spacing = node.parseSpace(u"thinmathspace")    
    node.leftspace = spacing
    node.rightspace = spacing

def measure_merror (node):
    createImplicitRow(node)
    
    node.borderWidth = node.nominalLineWidth()
    node.width =  node.base.width + 2 * node.borderWidth
    node.height = node.base.height + node.borderWidth    
    node.depth = node.base.depth + node.borderWidth    
    node.ascender = node.base.ascender
    node.descender = node.base.descender

def measure_ms (node): 
    lq = node.getProperty(u"lquote")
    rq = node.getProperty(u"rquote")
    if lq: node.text = node.text.replace(lq, u"\\"+lq)
    if rq and rq != lq: node.text = node.text.replace(rq, u"\\"+rq)
    node.text = lq + node.text + rq
    node.measureText()
    spacing = node.parseSpace(u"thinmathspace")    
    node.leftspace = spacing
    node.rightspace = spacing

def measure_mspace (node): 
    node.height = node.parseLength(node.getProperty(u"height"))
    node.depth = node.parseLength(node.getProperty(u"depth"))
    node.width = node.parseSpace(node.getProperty(u"width"))

    # Add ascender/descender values
    node.ascender = node.nominalAscender()
    node.descender = node.nominalDescender()

def measure_mrow (node):
    if len(node.children) == 0: return

    # Determine alignment type for the row. If there is a non-axis-aligned,
    # non-space child in the row, the whole row is non-axis-aligned. The row
    # that consists of just spaces is considered a space itself
    node.alignToAxis = True 
    node.isSpace = True
    for ch in node.children:
        if not ch.isSpace:
            node.alignToAxis = node.alignToAxis and ch.alignToAxis
            node.isSpace = False

    # Process non-marking operators
    for i in range(len(node.children)):
        ch = node.children[i]
        if ch.core.elementName != u'mo': continue    
        if ch.text in [u'\u2061', u'\u2062', u'\u2063']:
            ch.text = u""
            def longtext(n): 
                if n is None: return False
                if n.isSpace: return False
                if n.core.elementName == u"ms": return True
                if n.core.elementName in [u"mo", u"mi", u"mtext"]: return (len(n.core.text) > 1)
                return False
            ch_prev = None; ch_next = None;                           
            if i > 0: ch_prev = node.children[i-1]
            if i + 1 < len(node.children): ch_next = node.children[i+1]
            if longtext(ch_prev) or longtext(ch_next):
                ch.width = ch.parseSpace("thinmathspace")

    # Calculate extent for vertical stretching
    (node.ascender, node.descender) = getVerticalStretchExtent(node.children, node.alignToAxis, node.axis())

    # Grow sizeable operators 
    for ch in node.children:
        if ch.core.stretchy:
            desiredHeight = node.ascender; desiredDepth = node.descender
            if ch.alignToAxis and not node.alignToAxis:
                desiredHeight -= node.axis(); desiredDepth += node.axis()
            desiredHeight -= ch.core.ascender - ch.core.height  
            desiredDepth -= ch.core.descender - ch.core.depth  
            stretch(ch, toHeight=desiredHeight, 
                        toDepth=desiredDepth, 
                        symmetric=node.alignToAxis)

    # Recalculate height/depth after growing operators
    (node.height, node.depth, node.ascender, node.descender) = getRowVerticalExtent(node.children, node.alignToAxis, node.axis())
    
    # Finally, calculate width and spacings
    for ch in node.children:
        node.width += ch.width + ch.leftspace + ch.rightspace 
    node.leftspace = node.children[0].leftspace
    node.rightspace = node.children[-1].rightspace
    node.width -= node.leftspace + node.rightspace 
    
def measure_mfrac (node): 
    if len(node.children) != 2:
        node.error("Invalid content of 'mfrac' element: element should have exactly two children")
        if len(node.children) < 2:
            measure_mrow (node); return
    
    (node.enumerator, node.denominator) = node.children[:2]
    node.alignToAxis = True
    
    ruleWidthKeywords = {u"medium": "1",
                         u"thin": "0.5",
                         u"thick": "2"}
                         
    widthAttr = node.getProperty(u"linethickness")
    widthAttr = ruleWidthKeywords.get(widthAttr, widthAttr)
    unitWidth = node.nominalLineWidth()
    node.ruleWidth = node.parseLength(widthAttr, unitWidth)

    node.ruleGap = node.nominalLineGap()
    if node.tightspaces: node.ruleGap /= 1.41 # more compact style if in scripts/limits

    if node.getProperty(u"bevelled") == u"true":    
        eh = node.enumerator.height + node.enumerator.depth
        dh = node.denominator.height + node.denominator.depth
        vshift = min (eh, dh) / 2
        node.height = (eh + dh - vshift) / 2
        node.depth = node.height

        node.slope = defaultSlope  
        node.width = node.enumerator.width + node.denominator.width
        node.width += vshift / node.slope
        node.width += (node.ruleWidth + node.ruleGap) * math.sqrt(1 + node.slope**2)
        node.leftspace = node.enumerator.leftspace
        node.rightspace = node.denominator.rightspace
    else:
        node.height = node.ruleWidth / 2 + node.ruleGap + node.enumerator.height + node.enumerator.depth
        node.depth  = node.ruleWidth / 2 + node.ruleGap + node.denominator.height + node.denominator.depth
        node.width = max(node.enumerator.width, node.denominator.width) + 2 * node.ruleWidth
        node.leftspace = node.ruleWidth
        node.rightspace = node.ruleWidth

    node.ascender = node.height
    node.descender = node.depth

def measure_msqrt(node):
    # Create an explicit mrow if there's more than one child
    createImplicitRow(node)
    enclosures.addRadicalEnclosure(node)

def measure_mroot(node):
    if len(node.children) != 2:
        node.error("Invalid content of 'mroot' element: element should have exactly two children")

    if len(node.children) < 2:            
        node.rootindex = None
        measure_msqrt(node)
    else:
        setNodeBase(node, node.children[0])
        node.rootindex = node.children[1]
        enclosures.addRadicalEnclosure(node)
        node.width += max(0, node.rootindex.width - node.cornerWidth)
        node.height += max(0, node.rootindex.height + node.rootindex.depth - node.cornerHeight)        
        node.ascender = node.height
    
def measure_msub (node): 
    if len(node.children) != 2:
        node.error("Invalid content of 'msub' element: element should have exactly two children")
        if len(node.children) < 2:
            measure_mrow (node); return
    measureScripts(node, [node.children[1]], None)
    
def measure_msup (node): 
    if len(node.children) != 2:
        node.error("Invalid content of 'msup' element: element should have exactly two children")
        if len(node.children) < 2:
            measure_mrow (node); return
    measureScripts(node, None, [node.children[1]])

def measure_msubsup (node):
    if len(node.children) != 3:
        node.error("Invalid content of 'msubsup' element: element should have exactly three children")
        if len(node.children) == 2:
            measure_msub (node); return
        elif len(node.children) < 2:
            measure_mrow (node); return
    measureScripts(node, [node.children[1]], [node.children[2]])

def measure_munder (node): 
    if len(node.children) != 2:
        node.error("Invalid content of 'munder' element: element should have exactly two children")
        if len(node.children) < 2:
            measure_mrow (node); return
    measureLimits(node, node.children[1], None)
            
    
def measure_mover (node): 
    if len(node.children) != 2:
        node.error("Invalid content of 'mover' element: element should have exactly two children")
        if len(node.children) < 2:
            measure_mrow (node); return
    measureLimits(node, None, node.children[1])

def measure_munderover (node):
    if len(node.children) != 3:
        node.error("Invalid content of 'munderover' element: element should have exactly three children")
        if len(node.children) == 2:
            measure_munder (node); return
        elif len(node.children) < 2:
            measure_mrow (node); return
    measureLimits(node, node.children[1], node.children[2])


def measure_mmultiscripts (node):
    if len(node.children) == 0:
        measure_mrow (node); return
    
    # Sort children into sub- and superscripts
    subscripts = [] 
    superscripts = []
    presubscripts = []
    presuperscripts = []
    
    isPre = False; isSub = True
    for ch in node.children[1:]:
        if ch.elementName == u"mprescripts":
            if isPre:
                node.error("Repeated 'mprescripts' element inside 'mmultiscripts\n")
            isPre = True; isSub = True; continue
        if isSub:
            if isPre: presubscripts.append(ch)
            else: subscripts.append(ch)
        else:
            if isPre: presuperscripts.append(ch)
            else: superscripts.append(ch)        
        isSub = not isSub
     
    measureScripts(node, subscripts, superscripts, presubscripts, presuperscripts)
    
def measure_menclose (node):
    def pushEnclosure():
        if node.decoration is None: return  # no need to push

        wrapChildren (node, u"menclose")
        setNodeBase(node.children[0], node.base)
        setNodeBase(node, node.children[0])
        node.base.decoration = node.decoration
        node.base.decorationData = node.decorationData
        node.decoration = None
        node.decorationData = None
        node.base.width = node.width
        node.base.height = node.height
        node.base.depth = node.depth
        node.base.borderWidth = node.borderWidth
        
    createImplicitRow(node)
    signs = node.getProperty(u"notation").split()
    node.width = node.base.width
    node.height = node.base.height
    node.depth = node.base.depth
    node.decoration = None
    node.decorationData = None
    node.borderWidth = node.nominalLineWidth()    
    node.hdelta = node.nominalLineGap() + node.borderWidth
    node.vdelta = node.nominalLineGap() + node.borderWidth
    
    # Radical sign - convert to msqrt for simplicity
    if u"radical" in signs:
        wrapChildren(node, u"msqrt")
        setNodeBase(node.children[0], node.base)
        setNodeBase(node, node.children[0])
        node.base.makeContext()
        node.base.measureNode()
        node.width = node.base.width
        node.height = node.base.height
        node.depth = node.base.depth        
        
    # Strikes
    strikes = [ u"horizontalstrike" in signs,
                u"verticalstrike" in signs,
                u"updiagonalstrike" in signs,
                u"downdiagonalstrike" in signs ]
    if True in strikes:
        pushEnclosure()
        node.decoration = "strikes"
        node.decorationData = strikes
        # no size change - really? 
    
    # Rounded box 
    if u"roundedbox" in signs:
        pushEnclosure()
        node.decoration = "roundedbox"
        enclosures.addBoxEnclosure(node)
    
    # Square box 
    if u"box" in signs:
        pushEnclosure()
        node.decoration = "box"
        enclosures.addBoxEnclosure(node)
    
    # Circle
    if u"circle" in signs:
        pushEnclosure()
        node.decoration = "circle"
        enclosures.addCircleEnclosure(node)

    # Borders    
    borders = [ u"left" in signs,
                u"right" in signs,
                u"top" in signs,
                u"bottom" in signs ]
    if True in borders:
        pushEnclosure()
        if False in borders:
            node.decoration = "borders"
            enclosures.addBorderEnclosure(node, borders)
        else:
            node.decoration = "box"
            enclosures.addBoxEnclosure(node)

    # Long division    
    if u"longdiv" in signs:
        pushEnclosure()
        node.decoration = "borders"
        enclosures.addBorderEnclosure(node, [True, False, True, False]) # left top for now

    # Actuarial    
    if u"actuarial" in signs:
        pushEnclosure()
        node.decoration = "borders"
        enclosures.addBorderEnclosure(node, [False, True, True, False]) # right top
               
def measure_mtable (node):
    node.lineWidth = node.nominalLineWidth()    

    # For readability, most layout stuff is split into pieces and moved to tables.py
    tables.arrangeCells(node) 
    tables.arrangeLines(node)
    
    # Calculate column widths 
    tables.calculateColumnWidths(node)
    # Expand stretchy operators horizontally
    for r in node.rows:
        for i in range(len(r.cells)):
            c = r.cells[i]
            if c is None or c.content is None: continue
            content = c.content
            if content.elementName == u"mtd":
                if len(content.children) != 1: continue
                content = content.children[0]
                if content.core.stretchy: c.content = content
            if content.core.stretchy:
                if c.colspan == 1:
                    stretch(content, toWidth = node.columns[i].width)
                else:
                    spannedColumns = node.columns[i : i + c.colspan]
                    cellSize = sum([x.width for x in spannedColumns])
                    cellSize += sum([x.spaceAfter for x in spannedColumns[:-1]])
                    stretch(content, toWidth = cellSize)

    # Calculate row heights
    tables.calculateRowHeights(node)
    # Expand stretchy operators vertically in all cells
    for i in range(len(node.rows)):
        r = node.rows[i]
        for c in r.cells:
            if c is None or c.content is None: continue
            content = c.content
            if content.elementName == u"mtd":
                if len(content.children) != 1: continue
                content = content.children[0]
                if content.core.stretchy: c.content = content
            if content.core.stretchy:
                if c.rowspan == 1:
                    stretch(content, toHeight = r.height - c.vshift, 
                                     toDepth = r.depth + c.vshift)
                else:
                    spannedRows = node.rows[i : i + c.rowspan]
                    cellSize = sum([x.height + x.depth for x in spannedRows])
                    cellSize += sum([x.spaceAfter for x in spannedRows[:-1]])
                    stretch(content, toHeight = cellSize / 2, 
                                     toDepth = cellSize / 2)

    # Recalculate widths, to account for stretched cells
    tables.calculateColumnWidths(node)

    # Calculate total width of the table
    node.width  = sum([x.width + x.spaceAfter for x in node.columns])
    node.width += 2 * node.framespacings[0]
        
    # Calculate total height of the table
    vsize = sum([x.height + x.depth + x.spaceAfter for x in node.rows])
    vsize += 2 * node.framespacings[1]

    # Calculate alignment point
    (alignType, alignRow) = tables.getAlign(node)
    
    if alignRow is None:
       topLine = 0
       bottomLine = vsize
       axisLine = vsize / 2
       baseLine = axisLine + node.axis()
    else:
       row = node.rows[alignRow - 1]
       topLine = node.framespacings[1]
       for r in node.rows[0 : alignRow]: topLine += r.height + r.depth + r.spaceAfter 
       bottomLine = topLine + row.height + row.depth
       if row.alignToAxis: 
          axisLine = topLine + row.height
          baseLine = axisLine + node.axis()
       else:
          baseLine = topLine + row.height
          axisLine = baseLine - node.axis()   
    
    if alignType == u"axis":
        node.alignToAxis = True
        node.height = axisLine 
    elif alignType == u"baseline":
        node.alignToAxis = False
        node.height = baseLine
    elif alignType == u"center":
        node.alignToAxis = False
        node.height = (topLine + bottomLine) / 2    
    elif alignType == u"top":
        node.alignToAxis = False
        node.height = topLine
    elif alignType == u"bottom":    
        node.alignToAxis = False
        node.height = bottomLine
    else:
        node.error("Unrecognized or unsupported table alignment value: " + alignType)
        node.alignToAxis = True
        node.height = axisLine
    node.depth = vsize - node.height
    
    node.ascender = node.height
    node.descender = node.depth

def measure_mtr (node):
    if node.parent is None or node.parent.elementName != u"mtable":
        node.error("Misplaced '%s' element: should be child of 'mtable'" % node.elementName)
    pass # all processing is done on the table

def measure_mlabeledtr (node):
    # Strip the label and treat as an ordinary 'mtr'
    if len(node.children) == 0:
        node.error("Missing label in '%s' element" % node.elementName)
    else: 
        node.warning("MathML element '%s' is unsupported: label omitted" % node.elementName)
        node.children = node.children[1:]
    measure_mtr(node)    

def measure_mtd (node):
    if node.parent is None or node.parent.elementName not in [u"mtr", u"mlabeledtr", u"mtable"]:
        node.error("Misplaced '%s' element: should be child of 'mtr', 'mlabeledtr', or 'mtable'" % node.elementName)
    measure_mrow(node)

def measureScripts(node, subscripts, superscripts, 
                         presubscripts = None, presuperscripts = None):
    node.subscripts = subscripts or [] 
    node.superscripts = superscripts or []
    node.presubscripts = presubscripts or []
    node.presuperscripts = presuperscripts or []

    setNodeBase(node, node.children[0])
    node.width = node.base.width
    node.height = node.base.height
    node.depth = node.base.depth
    node.ascender = node.base.ascender
    node.descender = node.base.descender
    
    subs = node.subscripts + node.presubscripts
    supers = node.superscripts + node.presuperscripts
    node.subscriptAxis = max([0] + [x.axis() for x in subs])
    node.superscriptAxis = max([0] + [x.axis() for x in supers])
    gap = max ([x.nominalLineGap() for x in subs+supers])
    protrusion = node.parseLength("0.25ex")
    scriptMedian = node.axis()
    
    (subHeight, subDepth, subAscender, subDescender) = getRowVerticalExtent(subs, False, node.subscriptAxis)
    (superHeight, superDepth, superAscender, superDescender) = getRowVerticalExtent(supers, False, node.superscriptAxis)

    node.subShift = 0
    if len(subs) > 0:
        shiftAttr = node.getProperty(u"subscriptshift")
        if shiftAttr is None: shiftAttr = "0.5ex"
        node.subShift = node.parseLength(shiftAttr)  # positive shifts down
        node.subShift = max (node.subShift, subHeight - scriptMedian + gap)
        if node.alignToAxis: node.subShift += node.axis()
        node.subShift = max (node.subShift, node.base.depth + protrusion - subDepth)
        node.height = max (node.height, subHeight - node.subShift)
        node.depth = max (node.depth, subDepth + node.subShift)
        node.ascender = max (node.ascender, subAscender - node.subShift)
        node.descender = max (node.descender, subDescender + node.subShift)

    node.superShift = 0
    if len(supers) > 0:    
        shiftAttr = node.getProperty(u"superscriptshift")
        if shiftAttr is None: shiftAttr = "1ex"
        node.superShift = node.parseLength(shiftAttr)  # positive shifts up
        node.superShift = max (node.superShift, superDepth + scriptMedian + gap)
        if node.alignToAxis: node.superShift -= node.axis()
        node.superShift = max (node.superShift, node.base.height + protrusion - superHeight)
        node.height = max (node.height, superHeight + node.superShift)
        node.depth = max (node.depth, superDepth - node.superShift)
        node.ascender = max (node.ascender, superHeight + node.superShift)
        node.descender = max (node.descender, superDepth - node.superShift)

    def parallelWidths (nodes1, nodes2):
       widths = []
       for i in range (max(len(nodes1), len(nodes2))):
          w = 0
          if i < len(nodes1): w = max (w, nodes1[i].width) 
          if i < len(nodes2): w = max (w, nodes2[i].width)
          widths.append(w)
       return widths

    node.postwidths = parallelWidths(node.subscripts, node.superscripts)
    node.prewidths = parallelWidths(node.presubscripts, node.presuperscripts)
    node.width += sum(node.prewidths + node.postwidths)

def measureLimits(node, underscript, overscript):
    if node.children[0].core.moveLimits:
        subs = [] 
        supers = []
        if underscript is not None: subs = [underscript]
        if overscript is not None: supers = [overscript]
        measureScripts(node, subs, supers); return
        
    node.underscript = underscript 
    node.overscript = overscript
    setNodeBase(node, node.children[0])
    
    node.width = node.base.width
    if overscript is not None: node.width = max(node.width, overscript.width)
    if underscript is not None: node.width = max(node.width, underscript.width)    
    stretch (node.base, toWidth = node.width)
    stretch (overscript, toWidth = node.width)
    stretch (underscript, toWidth = node.width)

    gap = node.nominalLineGap()

    if overscript is not None:
        overscriptBaselineHeight = node.base.height + gap + overscript.depth
        node.height =  overscriptBaselineHeight + overscript.height
        node.ascender = node.height
    else:    
        node.height = node.base.height
        node.ascender = node.base.ascender

    if underscript is not None:
        underscriptBaselineDepth = node.base.depth + gap + underscript.height
        node.depth =  underscriptBaselineDepth + underscript.depth
        node.descender = node.depth
    else:    
        node.depth = node.base.depth
        node.descender = node.base.descender

def stretch(node, toWidth=None, toHeight=None, toDepth=None, symmetric=False):
    if node is None: return
    if not node.core.stretchy: return
    if node is not node.base:
        if toWidth is not None:
            toWidth -= node.width - node.base.width
        stretch(node.base, toWidth, toHeight, toDepth, symmetric)
        node.measureNode()
    elif node.elementName == u"mo":
        if node.fontSize == 0: return 

        maxsizedefault = node.opdefaults.get(u"maxsize")
        maxsizeattr = node.getProperty(u"maxsize", maxsizedefault)
        if (maxsizeattr == u"infinity"): 
            maxScale = None
        else:
            maxScale = node.parseSpaceOrPercent(maxsizeattr, node.fontSize, node.fontSize) / node.fontSize

        minsizedefault = node.opdefaults.get(u"minsize")
        minsizeattr = node.getProperty(u"minsize", minsizedefault)
        minScale = node.parseSpaceOrPercent(minsizeattr, node.fontSize, node.fontSize) / node.fontSize        
        if toWidth is None:    
            stretchVertically(node, toHeight, toDepth, minScale, maxScale, symmetric) 
        else:
            stretchHorizontally(node, toWidth, minScale, maxScale) 
        
def stretchVertically(node, toHeight, toDepth, minScale, maxScale, symmetric):
    if node.ascender + node.descender == 0: return
    if node.scaling == u"horizontal": return
    
    if symmetric and node.symmetric:
        toHeight = (toHeight + toDepth) / 2
        toDepth = toHeight
    scale = (toHeight + toDepth) / (node.ascender + node.descender) 
        
    if minScale: scale = max (scale, minScale)
    if maxScale: scale = min (scale, maxScale)

    node.fontSize *= scale
    node.height *= scale
    node.depth *= scale
    node.ascender *= scale
    node.descender *= scale
    node.textShift *= scale

    extraShift = ((toHeight - node.ascender) - 
                  (toDepth - node.descender)) / 2
    node.textShift += extraShift
    node.height += extraShift
    node.ascender += extraShift
    node.depth -= extraShift
    node.descender -= extraShift

    if node.scaling == u"vertical":
        node.textStretch /= scale
    else:
        node.width *= scale
        node.leftBearing *= scale
        node.rightBearing *= scale
                            
def stretchHorizontally(node, toWidth, minScale, maxScale):        
    if node.width == 0: return
    if node.scaling != u"horizontal": return

    scale = toWidth / node.width 
    scale = max (scale, minScale)
    if maxScale: scale = min (scale, maxScale)

    node.width *= scale
    node.textStretch *= scale
    node.leftBearing *= scale
    node.rightBearing *= scale
 
def setNodeBase(node, base):
     node.base = base
     node.core = base.core
     node.alignToAxis = base.alignToAxis
     node.stretchy = base.stretchy

def wrapChildren(node, wrapperElement):
    old_children = node.children
    node.children = []
    base = mathnode.MathNode (wrapperElement, {}, None, node.config, node)
    base.children = old_children

def createImplicitRow(node):
    if len(node.children) != 1: 
        wrapChildren(node, u"mrow")
        node.children[0].makeContext();
        node.children[0].measureNode();
    setNodeBase(node, node.children[0])

def getVerticalStretchExtent(descendants, rowAlignToAxis, axis):
    ascender = 0; descender = 0 
    for ch in descendants:
        if ch.core.stretchy:
            asc = ch.core.ascender;  desc = ch.core.descender # 'cos it will grow         
        else:
            asc = ch.ascender;  desc = ch.descender
        if ch.alignToAxis and not rowAlignToAxis: 
            asc += axis; desc -= axis
        elif not ch.alignToAxis and rowAlignToAxis:
            chaxis = ch.axis()
            asc -= chaxis; desc += chaxis
        ascender = max (asc, ascender);  descender = max (desc, descender)
    return (ascender, descender)

        
def getRowVerticalExtent(descendants, rowAlignToAxis, axis):
    height = 0; depth = 0; ascender = 0; descender = 0
    for ch in descendants:
        h = ch.height;  d = ch.depth;  asc = ch.ascender; desc = ch.descender
        if ch.alignToAxis and not rowAlignToAxis: 
            h += axis; asc += axis; d -= axis; desc -= axis
        elif not ch.alignToAxis and rowAlignToAxis:
            chaxis = ch.axis()
            h -= chaxis; asc -= chaxis; d += chaxis; desc += chaxis
        height = max (h, height);  depth = max (d, depth)
        ascender = max (asc, ascender);  descender = max (desc, descender)
    return (height, depth, ascender, descender)
        