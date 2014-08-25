"""Drawing methods for MathML elements"""
import sys, math, mathnode
from xml import sax
from xml.sax import xmlreader

# SVG namespace
SVGNS = u"http://www.w3.org/2000/svg"
# SVGMath proprietary namespace - used in metadata
SVGMathNS = u"http://www.grigoriev.ru/svgmath"

# Use namespace-aware (SAX2) or plain (SAX1) callbacks 
useNamespaces = True
# Output extra linefeeds to improve readability
readable = False

# Handy mapping of horizontal alignment keywords
alignKeywords = { u"left": 0, u"center": 0.5, u"right": 1 }

def startElement(output, localname, namespace, prefix, attrs):
    """Wrapper to emit a start tag"""
    if readable: output.characters(u"\n") # for readability
    
    if useNamespaces:    
        nsAttrs = {}
        for (att, value) in attrs.items(): nsAttrs[(None, att)] = value
        qnames = attrs.keys()
        output.startElementNS((namespace, localname), 
                              prefix+localname, 
                              xmlreader.AttributesNSImpl(nsAttrs, qnames))
    else:
        output.startElement(prefix+localname, 
                            xmlreader.AttributesImpl(attrs))
     
def  endElement(output, localname, namespace, prefix):
    """Wrapper to emit an end tag"""
    if useNamespaces:    
        output.endElementNS((namespace, localname), prefix+localname)
    else:
        output.endElement(prefix+localname)

    if readable: output.characters(u"\n") # for readability    

def startSVGElement(output, localname, attrs):
    startElement(output, localname, SVGNS, u"svg:", attrs)

def endSVGElement(output, localname):
    endElement(output, localname, SVGNS, u"svg:")

def drawImage(node, output):
    """Top-level draw function: prepare the canvas, then call the draw method of the root node"""
    # The zero level of the viewbox is always aligned on the alphabetic baseline
    baseline = 0
    if node.alignToAxis: baseline = node.axis();
    
    height = max(node.height, node.ascender);
    depth = max(node.depth, node.descender);
    vsize = height + depth;
    
    attrs = {u"width": (u"%fpt" % node.width), 
             u"height": (u"%fpt" % vsize), 
             u"viewBox": (u"0 %f %f %f" % (-(height+baseline), node.width, vsize))}    

    if useNamespaces: 
        output.startPrefixMapping(u'svg', SVGNS)
        output.startPrefixMapping(u'svgmath', SVGMathNS)
    else:
        attrs[u"xmlns:svg"] = SVGNS
        attrs[u"xmlns:svgmath"] = SVGMathNS

    startSVGElement(output, u'svg', attrs)

    # Prints baseline table as metadata    
    startSVGElement(output, u'metadata', {})
    startElement(output, 
                 "metrics", SVGMathNS, "svgmath:", 
                 { u"baseline": depth - baseline, 
                   u"axis": depth - baseline + node.axis(),
                   u"top": depth + node.height,
                   u"bottom": depth - node.depth } )
    endElement(output, "metrics", SVGMathNS, "svgmath:") 
    
    endSVGElement(output, u'metadata')

    drawTranslatedNode(node, output, 0, - baseline)
    endSVGElement(output, u'svg')    

    if useNamespaces: 
        output.endPrefixMapping(u'svg')
        output.endPrefixMapping(u'svgmath')

def default_draw (node, output): pass

def draw_math (node, output): draw_mrow (node, output)
 
def draw_mrow (node, output):
    drawBox(node, output)
    if len(node.children) == 0: return

    offset = - node.children[0].leftspace
    for ch in node.children:
        offset += ch.leftspace 
        baseline = 0
        if ch.alignToAxis and not node.alignToAxis: baseline = - node.axis()        
        drawTranslatedNode(ch, output, offset, baseline)
        offset += ch.width + ch.rightspace

def draw_mphantom (node, output): pass  

def draw_none (node, output): pass

def draw_maction (node, output):
    if node.base is not None: node.base.draw(output)

def draw_mprescripts (node, output): pass

def draw_mstyle (node, output): draw_mrow (node, output)

def draw_mfenced (node, output):  draw_mrow (node, output)
    
def draw_merror (node, output):
    drawBox(node, output, node.borderWidth, u"red")
    drawTranslatedNode(node.base, output,  node.borderWidth, 0)

def draw_mpadded (node, output):
    drawBox(node, output)
    drawTranslatedNode(node.base, output, node.leftpadding, 0)
    
def draw_menclose (node, output):
    if node.decoration is None:
        node.base.draw(output)
    elif node.decoration == "strikes":
        drawStrikesEnclosure(node, output)
    elif node.decoration == "borders":
        drawBordersEnclosure(node, output)
    elif node.decoration == "box":
        drawBoxEnclosure(node, output)
    elif node.decoration == "roundedbox":
        r = (node.width - node.base.width + 
             node.height - node.base.height +
             node.depth - node.base.depth) / 4
        drawBoxEnclosure(node, output, r)
    elif node.decoration == "circle":
        drawCircleEnclosure(node, output)
    else:
        node.error("Internal error: unhandled decoration %s", str(node.decoration))
        node.base.draw(output)
        
def draw_mfrac (node, output):
    drawBox(node, output)

    if node.getProperty(u"bevelled") == u"true":
        drawTranslatedNode(node.enumerator, output,
                0, 
                node.enumerator.height - node.height)        
        drawTranslatedNode(node.denominator, output, 
                node.width - node.denominator.width,
                node.depth - node.denominator.depth) 
    else:
        enumalign = getAlign(node, u"enumalign")
        denomalign = getAlign(node, u"denomalign")        
        drawTranslatedNode(node.enumerator, output,
                node.ruleWidth + (node.width - 2 * node.ruleWidth - node.enumerator.width) * enumalign, 
                node.enumerator.height - node.height)        
        drawTranslatedNode(node.denominator, output, 
                node.ruleWidth + (node.width - 2 * node.ruleWidth - node.denominator.width) * denomalign,
                node.depth - node.denominator.depth) 
    
    if node.ruleWidth:
        if node.getProperty(u"bevelled") == u"true":
            eh = node.enumerator.height + node.enumerator.depth
            dh = node.denominator.height + node.denominator.depth

            # Determine a point lying on the rule
            ruleX = (node.width + node.enumerator.width - node.denominator.width) / 2.0
            if eh < dh:
                ruleY = 0.75 * eh - node.height 
            else:
                ruleY = node.depth - 0.75 * dh          
            
            x1 = max(0, ruleX - (node.depth - ruleY) / node.slope )
            x2 = min(node.width, ruleX + (ruleY + node.height) / node.slope)
            y1 = min(node.depth, ruleY + ruleX * node.slope)
            y2 = max(-node.height, ruleY - (node.width - ruleX) * node.slope)
            
        else:
            x1 = 0
            y1 = 0
            x2 = node.width
            y2 = 0
        
        drawLine(output, node.color, node.ruleWidth, 
                 x1, y1, x2, y2, {u"stroke-linecap": u"butt"}) 
        
def draw_mo (node, output):
    drawSVGText(node, output)    

def draw_mi (node, output):  
    drawSVGText(node, output)    

def draw_mn (node, output):  
    drawSVGText(node, output)    

def draw_mtext (node, output):  
    drawSVGText(node, output)    

def draw_ms (node, output):  
    drawSVGText(node, output)

def draw_mspace (node, output):
    drawBox (node, output)

def draw_msqrt(node, output):
    drawBox(node, output)
    drawTranslatedNode(node.base, output, 
            node.width - node.base.width - node.gap, 0)

    # Basic contour            
    x1 = node.width - node.base.width - node.rootWidth - 2 * node.gap
    y1 = (node.rootDepth - node.rootHeight)/2
    
    x2 = x1 + node.rootWidth * 0.2
    y2 = y1
    
    x3 = x1 + node.rootWidth * 0.6
    y3 = node.rootDepth
    
    x4 = x1 + node.rootWidth 
    y4 = - node.rootHeight + node.lineWidth / 2
    
    x5 = node.width 
    y5 = y4

    # Thickening
    slopeA = (x2 - x3)/(y2 - y3)
    slopeB = (x3 - x4)/(y3 - y4)
    
    x2a = x2 + (node.thickLineWidth - node.lineWidth)
    y2a = y2 
    
    x2c = x2 + node.lineWidth * slopeA / 2
    y2c = y2 + node.lineWidth * 0.9
    
    x2b = x2c + (node.thickLineWidth - node.lineWidth) / 2
    y2b = y2c
    
    ytmp = y3 - node.lineWidth/2 
    xtmp = x3 - node.lineWidth * (slopeA + slopeB) / 4
    
    y3a = (y2a * slopeA - ytmp * slopeB + xtmp - x2a) / (slopeA - slopeB)
    x3a = xtmp + (y3a - ytmp) * slopeB
    
    y3b = (y2b * slopeA - ytmp * slopeB + xtmp - x2b) / (slopeA - slopeB)
    x3b = xtmp + (y3b - ytmp) * slopeB

    # Lean the left protrusion down
    y1 += (x2 - x1) * slopeA
            
    attrs = { u"stroke": node.color, u"fill": u"none",
              u"stroke-width": (u"%f" % node.lineWidth),
              u"stroke-linecap": u"butt", 
              u"stroke-linejoin": u"miter", 
              u"stroke-miterlimit": u"10", 
              u"d": (u"M %f %f L %f %f L %f %f L %f %f L %f %f L %f %f L %f %f L %f %f L %f %f" %
                       (x1,y1, x2a,y2a,x3a,y3a,x3b,y3b,x2b,y2b,x2c,y2c, x3,y3,  x4,y4,  x5,y5))}
    startSVGElement(output, u'path', attrs) 
    endSVGElement(output, u'path')    
    
def draw_mroot(node, output):
    draw_msqrt(node, output)
    if node.rootindex is not None:
        w = max(0, node.cornerWidth - node.rootindex.width) / 2
        h = - node.rootindex.depth - node.rootHeight + node.cornerHeight
        drawTranslatedNode(node.rootindex, output, w, h)
    
def draw_msub (node, output): drawScripts(node, output)

def draw_msup (node, output): drawScripts(node, output)
    
def draw_msubsup (node, output): drawScripts(node, output)

def draw_mmultiscripts(node, output): drawScripts(node, output)

def drawScripts (node, output):
    if len(node.children) < 2:
        draw_mrow (node); return

    subY = node.subShift
    superY = - node.superShift
    def adjustment (script):
        if script.alignToAxis: return script.axis()
        else: return 0
    
    drawBox(node, output)
    offset = 0
    for i in range(len(node.prewidths)):
        offset += node.prewidths[i]
        if i < len(node.presubscripts):
            presubscript = node.presubscripts[i]
            drawTranslatedNode(presubscript, output, 
                    offset - presubscript.width, subY - adjustment(presubscript))
        if i < len(node.presuperscripts):
            presuperscript = node.presuperscripts[i]
            drawTranslatedNode(presuperscript, output, 
                    offset - presuperscript.width, superY - adjustment(presuperscript))    
    
    drawTranslatedNode(node.base, output, offset, 0)
    offset += node.base.width
        
    for i in range(len(node.postwidths)):
        if i < len(node.subscripts):
            subscript = node.subscripts[i]
            drawTranslatedNode(subscript, output, 
                               offset, subY - adjustment(subscript))
        if i < len(node.superscripts):
            superscript = node.superscripts[i]
            drawTranslatedNode(superscript, output, 
                               offset, superY - adjustment(superscript))    
        offset += node.postwidths[i]

def draw_munder (node, output): drawLimits(node, output)

def draw_mover (node, output):   drawLimits(node, output)

def draw_munderover (node, output):  drawLimits(node, output)

def drawLimits (node, output):
    if len(node.children) < 2:
        draw_mrow (node); return
    if node.core.moveLimits:
        drawScripts(node, output);  return

    drawBox(node, output)
    drawTranslatedNode(node.base, output, 
            (node.width - node.base.width) / 2, 0)
    if node.underscript is not None:        
        drawTranslatedNode(node.underscript, output, 
                (node.width - node.underscript.width) / 2,
                node.depth - node.underscript.depth) 
    if node.overscript is not None:        
        drawTranslatedNode(node.overscript, output, 
                (node.width - node.overscript.width) / 2,
                node.overscript.height - node.height) 
                

def draw_mtd(node, output):
    draw_mrow(node, output)

def draw_mtr(node, output): pass

def draw_mlabeledtr(node, output): pass

def draw_mtable(node, output):
    drawBox (node, output)
    
    # Draw cells
    vshift = - node.height + node.framespacings[1]    
    for r in range (len(node.rows)):
        row = node.rows[r]
        vshift += row.height
        hshift = node.framespacings[0]
        for c in range (len(row.cells)):
            column = node.columns[c]
            cell = row.cells[c]
            if cell is not None and cell.content is not None:
                # Calculate horizontal alignment
                if cell.colspan > 1:
                    cellWidth = sum ([x.width for x in node.columns[c : c + cell.colspan]])
                    cellWidth += sum ([x.spaceAfter for x in node.columns[c : c + cell.colspan - 1]])
                else: cellWidth = column.width   
                hadjust = (cellWidth - cell.content.width) * alignKeywords.get(cell.halign, 0.5)
                
                # Calculate vertical alignment.
                if cell.rowspan > 1:
                    cellHeight = sum ([x.height + x.depth for x in node.rows[r : r + cell.rowspan]])
                    cellHeight += sum ([x.spaceAfter for x in node.rows[r : r + cell.rowspan - 1]])
                else:
                    cellHeight = row.height + row.depth

                if cell.valign == u"top":
                    vadjust = cell.content.height - row.height
                elif cell.valign == u"bottom":
                    vadjust = cellHeight - row.height - cell.content.depth
                elif cell.valign in [u"axis", u"baseline"] and cell.rowspan == 1:
                    vadjust = - cell.vshift # calculated in the measurer
                else: # the rest of cases is centered
                    vadjust = (cell.content.height - cell.content.depth + cellHeight) / 2 - row.height 
                   
                drawTranslatedNode (cell.content, output, hshift + hadjust, vshift + vadjust)
            hshift += column.width + column.spaceAfter
        vshift += row.depth + row.spaceAfter
        
    # Draw frame
    def drawBorder (x1, y1, x2, y2, linestyle):
        if linestyle is None: return
        if x1 == x2 and y1 == y2: return
        if linestyle == u"dashed":
            linelength = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
            dashoffset = 5 - ((linelength / node.lineWidth + 3) % 10) / 2
            extrastyle = { u"stroke-dasharray": (u"%f,%f" %(node.lineWidth * 7, node.lineWidth * 3)),
                           u"stroke-dashoffset": (u"%f" % (node.lineWidth * dashoffset)) }
        else:
            extrastyle = None
        drawLine(output, node.color, node.lineWidth, x1, y1, x2, y2, extrastyle)

    x1 = node.lineWidth / 2
    y1 = node.lineWidth / 2 - node.height
    x2 = node.width - node.lineWidth / 2
    y2 = node.depth - node.lineWidth / 2
    
    drawBorder(x1, y1, x1, y2, node.framelines[0])  
    drawBorder(x2, y1, x2, y2, node.framelines[0])
    drawBorder(x1, y1, x2, y1, node.framelines[1])
    drawBorder(x1, y2, x2, y2, node.framelines[1])
    
    # Draw intermediate lines
    # First, let's make a grid
    hshift = node.framespacings[0]
    hoffsets = []
    for c in range (len(node.columns)):
        spacing = node.columns[c].spaceAfter
        hshift += node.columns[c].width
        hoffsets.append (hshift + spacing / 2)
        hshift += spacing
    hoffsets[-1] = x2

    vshift = - node.height + node.framespacings[1]
    voffsets = []
    for r in range (len(node.rows)):
        spacing = node.rows[r].spaceAfter
        vshift += node.rows[r].height + node.rows[r].depth
        voffsets.append (vshift + spacing / 2)
        vshift += spacing    
    voffsets[-1] = y2
    
    vspans = [0] * len(node.columns)
    for r in range (len(node.rows) - 1):
        row = node.rows[r]
        if row.lineAfter is None: continue
        
        for c in range (len(row.cells)):
            cell = row.cells[c]
            if cell is None or cell.content is None: continue 
            for j in range(c, c + cell.colspan): vspans[j] = cell.rowspan
        vspans = [max (0, n - 1) for n in vspans]
        
        lineY = voffsets[r]
        startX = x1
        endX = x1
        for c in range (len(node.columns)):
            if vspans[c] > 0:
                drawBorder(startX, lineY, endX, lineY, row.lineAfter)
                startX = hoffsets[c] 
            endX = hoffsets[c]
        drawBorder(startX, lineY, endX, lineY, row.lineAfter)            
        
    hspans = [0] * len(node.rows)
    for c in range (len(node.columns) - 1):
        column = node.columns[c]
        if column.lineAfter is None: continue
        
        for r in range (len(node.rows)):
            row = node.rows[r]
            if len(row.cells) <= c : continue
            cell = row.cells[c]
            if cell is None or cell.content is None: continue 
            for j in range(r, r + cell.rowspan): hspans[j] = cell.colspan
        hspans = [max (0, n - 1) for n in hspans]

        lineX = hoffsets[c]
        startY = y1
        endY = y1
        for r in range (len(node.rows)):
            if hspans[r] > 0:
                drawBorder(lineX, startY, lineX, endY, column.lineAfter)
                startY = voffsets[r] 
            endY = voffsets[r]
        drawBorder(lineX, startY, lineX, endY, column.lineAfter)
 
def drawBox(node, output, borderWidth = 0, borderColor = None, borderRadius = 0):
    background = getBackground(node)
    if background == u"none":
        if borderWidth is None or borderWidth == 0: return
    if borderColor is None: borderColor = node.color
    
    attrs = {u"fill": background,
             u"stroke": u"none",
             u"x": (u"%f" % (borderWidth / 2)),    
             u"y": (u"%f" % (borderWidth / 2 - node.height)), 
             u"width": (u"%f" % (node.width - borderWidth)), 
             u"height": (u"%f" % (node.height + node.depth - borderWidth))} 
    if borderWidth != 0 and borderColor is not None:
        attrs[u"stroke"] = borderColor;
        attrs[u"stroke-width"] = u"%f" % borderWidth
        if borderRadius != 0:   
            attrs[u"rx"] = u"%f" % borderRadius;
            attrs[u"ry"] = u"%f" % borderRadius;
                       
    startSVGElement(output, u'rect', attrs) 
    endSVGElement(output, u'rect')    

def drawLine(output, color, width, x1, y1, x2, y2, strokeattrs = None): 
    attrs = { u"fill": u"none", u"stroke": color, 
              u"stroke-width": (u"%f" % width),
              u"stroke-linecap": u"square",
              u"stroke-dasharray": u"none",
              u"x1": (u"%f" % x1), u"y1": (u"%f" % y1), 
              u"x2": (u"%f" % x2), u"y2": (u"%f" % y2) }
    if strokeattrs is not None: attrs.update(strokeattrs) 
          
    startSVGElement(output, u"line", attrs) 
    endSVGElement(output, u"line")    

def drawTranslatedNode(node, output, dx, dy):
    if dx != 0 or  dy != 0:
        startSVGElement(output, u'g', 
                 {u"transform": (u"translate(%f, %f)" % (dx, dy))})    
    node.draw(output)
    if dx != 0 or  dy != 0:
        endSVGElement(output, u'g')

def drawSVGText(node, output):
    drawBox(node, output)
    fontfamilies = [x.family for x in node.fontpool() if x.used]
    if len(fontfamilies) == 0: fontfamilies = node.fontfamilies
    attrs = {u"fill": node.color,
             u"font-family": u", ".join(fontfamilies),
             u"font-size": (u"%f" % node.fontSize),
             u"text-anchor": u"middle", 
             u"x": (u"%f" % ((node.width + node.leftBearing - node.rightBearing) / 2 / node.textStretch )), 
             u"y": (u"%f" % (- node.textShift))} 
    if node.fontweight != u"normal": 
        attrs[u"font-weight"] = node.fontweight
    if node.fontstyle != u"normal": 
        attrs[u"font-style"] = node.fontstyle
    if node.textStretch != 1:
        attrs[u"transform"] = (u"scale(%f, 1)" % node.textStretch)
    
    for oldchar, newchar in mathnode.specialChars.items():
       node.text = node.text.replace(oldchar, newchar)
    
    startSVGElement(output, u'text', attrs) 
    output.characters(node.text)
    endSVGElement(output, u'text')    

def getAlign(node, attrName):
    attrValue = node.getProperty(attrName, u"center")
    if attrValue not in alignKeywords.keys():
        node.error("Bad value %s for %s", attrValue, attrName)
    return alignKeywords.get(attrValue, 0.5) 


def drawBoxEnclosure(node, output, roundRadius = 0): 
    drawBox (node, output, node.borderWidth, None, roundRadius)
    drawTranslatedNode(node.base, output, (node.width - node.base.width)/2, 0)


def drawCircleEnclosure(node, output):   
    background = getBackground(node)
    
    r = (node.width - node.borderWidth) / 2
    cx = node.width / 2
    cy = (node.depth - node.height) / 2

    attrs = { u"fill": background, u"stroke": node.color, 
              u"stroke-width": (u"%f" % node.borderWidth),
              u"cx": (u"%f" % cx), u"cy": (u"%f" % cy), 
              u"r": (u"%f" % r) }    
    startSVGElement(output, u'circle', attrs) 
    endSVGElement(output, u'circle')
    
    drawTranslatedNode(node.base, output, (node.width - node.base.width)/2, 0)

    
def drawBordersEnclosure(node, output):
    def drawBorder (x1, y1, x2, y2):
        drawLine(output, node.color, node.borderWidth, x1, y1, x2, y2)

    drawBox(node, output)

    x1 = node.borderWidth / 2
    y1 = node.borderWidth / 2 - node.height
    x2 = node.width - node.borderWidth / 2
    y2 = node.depth - node.borderWidth / 2

    (left, right, top, bottom) = node.decorationData
    if left:   drawBorder(x1, y1, x1, y2)  
    if right:  drawBorder(x2, y1, x2, y2)
    if top:    drawBorder(x1, y1, x2, y1)
    if bottom: drawBorder(x1, y2, x2, y2)

    if left:
       offset = node.width - node.base.width
       if right: offset /= 2
    else: offset = 0
    drawTranslatedNode(node.base, output, offset, 0)

        
def drawStrikesEnclosure(node, output):
    def drawStrike (x1, y1, x2, y2):
        drawLine(output, node.color, node.borderWidth, x1, y1, x2, y2)

    drawBox(node, output)
    node.base.draw(output)
    
    mid_x = node.width / 2
    mid_y = (node.depth - node.height) / 2
    
    (horiz, vert, updiag, downdiag) = node.decorationData
    if horiz:    drawStrike(0, mid_y, node.width, mid_y)
    if vert:     drawStrike(mid_x, -node.height, mid_x, node.depth)
    if updiag:   drawStrike(0, node.depth, node.width, -node.height)
    if downdiag: drawStrike(0, -node.height, node.width, node.depth)

def getBackground(node):
    for attr in [u"mathbackground", u"background-color", u"background"]:
        value = node.attributes.get(attr)
        if value is not None: 
            if value == u"transparent": return u"none" 
            else: return value
    else: return u"none"
