"""Functions to format enclosures around MathML elements."""
import sys, math, mathnode

def addRadicalEnclosure(node):
    # The below is full of heuristics
    node.lineWidth = node.nominalThinStrokeWidth() 
    node.thickLineWidth = node.nominalThickStrokeWidth()
    node.gap = node.nominalLineGap()
    if not node.displaystyle: node.gap /= 2 # more compact style if inline

    node.rootHeight = max (node.base.height, node.base.ascender)
    node.rootHeight = max (node.rootHeight, node.nominalAscender())
    node.rootHeight += node.gap + node.lineWidth
    node.height = node.rootHeight

    node.alignToAxis = node.base.alignToAxis
    # Root extends to baseline for elements aligned on the baseline,
    # and to the bottom for elements aligned on the axis. An extra
    # line width is added to the depth, to account for radical sign 
    # protruding below the baseline.
    if node.alignToAxis:
        node.rootDepth = max (0, node.base.depth - node.lineWidth) 
        node.depth = max(node.base.depth, node.rootDepth + node.lineWidth) 
    else: 
        node.rootDepth = 0
        node.depth = max(node.base.depth, node.lineWidth)
        
    node.rootWidth = (node.rootHeight + node.rootDepth) * 0.6    
    node.cornerWidth = node.rootWidth * 0.9 - node.gap - node.lineWidth / 2 
    node.cornerHeight = (node.rootHeight + node.rootDepth) * 0.5 - node.gap - node.lineWidth / 2

    node.width = node.base.width + node.rootWidth + 2 * node.gap
    node.ascender = node.height
    node.descender = node.base.descender
    node.leftspace = node.lineWidth
    node.rightspace = node.lineWidth
    
def addBoxEnclosure(node):
    node.width += 2 * node.hdelta
    node.height += node.vdelta
    node.depth += node.vdelta
    node.ascender = node.base.ascender
    node.descender = node.base.descender

def addCircleEnclosure(node):
    d = math.sqrt(node.width**2 + node.height**2)
    d = max (d, node.width + 2 * node.hdelta)
    d = max (d, node.height + node.depth + 2 * node.vdelta)
    cy = (node.height - node.depth) / 2
    node.width = d
    node.height = d / 2 + cy
    node.depth = d / 2 - cy
    node.ascender = node.base.ascender
    node.descender = node.base.descender

def addBorderEnclosure(node, borders):
    if borders[0]: node.width += node.hdelta #left
    if borders[1]: node.width += node.hdelta # right
    if borders[2]: node.height += node.vdelta # top
    if borders[3]: node.depth += node.vdelta # bottom
    node.decorationData = borders
    node.ascender = node.base.ascender
    node.descender = node.base.descender
    
