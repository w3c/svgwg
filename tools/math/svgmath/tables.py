"""Table-related formatting functions.

This module contains functions called from measurers.py to format tables."""
import sys, mathnode

def getByIndexOrLast(lst, idx):
    if idx < len(lst): return lst[idx]
    else: return lst[-1]

class CellDescriptor:
    """Descriptor of a single cell in a table"""
    def __init__(self, content, halign, valign, colspan, rowspan):
        self.content = content
        self.halign = halign
        self.valign = valign
        self.colspan = colspan
        self.rowspan = rowspan

class ColumnDescriptor:
    """Descriptor of a single column in a table"""
    def __init__(self):
        self.auto = True
        self.fit = False
        self.width = 0
        self.spaceAfter = 0
        self.lineAfter = None

class RowDescriptor:
    """Descriptor of a single row in a table; contains cells"""
    def __init__(self, node, cells, rowalign, columnaligns, busycells):
        self.alignToAxis = (rowalign == u"axis")
        self.height = 0
        self.depth  = 0
        self.spaceAfter = 0
        self.lineAfter = None
        self.cells = []
        for c in cells:
            # Find the first free cell
            while len(busycells) > len(self.cells) and busycells[len(self.cells)] > 0:
                self.cells.append(None)

            halign = getByIndexOrLast(columnaligns, len(self.cells))
            valign = rowalign
            colspan = 1
            rowspan = 1

            if c.elementName == u"mtd":
                halign = c.attributes.get(u"columnalign", halign)
                valign = c.attributes.get(u"rowalign", valign)
                colspan = node.parseInt(c.attributes.get(u"colspan", u"1"))
                rowspan = node.parseInt(c.attributes.get(u"rowspan", u"1"))

            while len(self.cells) >= len(node.columns):
                node.columns.append(ColumnDescriptor())
            self.cells.append(CellDescriptor(c, halign, valign, colspan, rowspan))

            for i in range (1, colspan): self.cells.append(None)
            while len(self.cells) > len(node.columns):
                node.columns.append(ColumnDescriptor())

def arrangeCells(node):
    node.rows = []
    node.columns = []    
    busycells = []

    # Read table-level alignment properties      
    table_rowaligns = node.getListProperty(u"rowalign")
    table_columnaligns = node.getListProperty(u"columnalign")

    for ch in node.children:
        rowalign = getByIndexOrLast(table_rowaligns, len(node.rows))
        row_columnaligns = table_columnaligns
        if ch.elementName == u"mtr" or ch.elementName == "mlabeledtr":
            cells = ch.children
            rowalign = ch.attributes.get(u"rowalign", rowalign)
            if u"columnalign" in ch.attributes.keys():
                columnaligns = node.getListProperty(u"columnalign", ch.attributes.get(u"columnalign"))
        else:
            cells = [ch]

        row = RowDescriptor(node, cells, rowalign, row_columnaligns, busycells)
        node.rows.append(row)
        # busycells passes information about cells spanning multiple rows 
        busycells = [max (0, n - 1) for n in busycells]
        while len(busycells) < len(row.cells): busycells.append(0)
        for i in range (len(row.cells)):
            cell = row.cells[i] 
            if cell is None: continue
            if cell.rowspan > 1: 
                for j in range(i, i + cell.colspan): 
                    busycells[j] = cell.rowspan - 1

    # Pad the table with empty rows until no spanning cell protrudes
    while max(busycells) > 0:
        rowalign = getByIndexOrLast(table_rowaligns, len(node.rows))
        node.rows.append(RowDescriptor(node, [], rowalign, table_columnaligns, busycells))
        busycells = [max (0, n - 1) for n in busycells]

def arrangeLines(node):
    # Get spacings and line styles; expand to cover the table fully        
    spacings = map(node.parseLength, node.getListProperty(u"rowspacing"))
    lines = node.getListProperty(u"rowlines")
    
    for i in range(len(node.rows) - 1):
        node.rows[i].spaceAfter = getByIndexOrLast(spacings, i)
        line = getByIndexOrLast(lines, i) 
        if line != u"none": 
           node.rows[i].lineAfter = line
           node.rows[i].spaceAfter += node.lineWidth

    spacings = map(node.parseSpace, node.getListProperty(u"columnspacing"))
    lines = node.getListProperty(u"columnlines")
    
    for i in range(len(node.columns) - 1):
        node.columns[i].spaceAfter = getByIndexOrLast(spacings, i)        
        line = getByIndexOrLast(lines, i)
        if line != u"none": 
           node.columns[i].lineAfter = line
           node.columns[i].spaceAfter += node.lineWidth
    
    node.framespacings = [0, 0]
    node.framelines = [None, None]
    spacings = map(node.parseSpace, node.getListProperty(u"framespacing"))
    lines = node.getListProperty(u"frame")
    for i in range(2): 
        line = getByIndexOrLast(lines, i)
        if line != u"none": 
            node.framespacings[i] = getByIndexOrLast(spacings, i)
            node.framelines[i] = line

def calculateColumnWidths(node):
    # Get total width
    fullwidthattr = node.attributes.get(u"width", u"auto")
    if fullwidthattr == u"auto": 
        fullwidth = None
    else:
        fullwidth = node.parseLength(fullwidthattr)
        if fullwidth <= 0: fullwidth = None

    # Fill fixed column widths
    columnwidths = node.getListProperty(u"columnwidth")
    for i in range(len(node.columns)):
        column = node.columns[i]
        attr = getByIndexOrLast(columnwidths, i)
        if attr in [u"auto", u"fit"]: 
            column.fit = (attr == u"fit")
        elif attr.endswith(u'%'):
            if fullwidth is None: 
                node.error("Percents in column widths supported only in tables with explicit width; width of column %d treated as 'auto'" % (i+1))
            else:
                value = node.parseFloat(attr[:-1])
                if value and value > 0: 
                    column.width = fullwidth * value / 100 
                    column.auto = False
        else:
            column.width = node.parseSpace(attr)
            column.auto = False
    
    # Set  initial auto widths for cells with colspan == 1
    for r in node.rows:
        for i in range(len(r.cells)):
            c = r.cells[i]
            if c is None or c.content is None or c.colspan > 1: continue
            column = node.columns[i]
            if column.auto: column.width = max(column.width, c.content.width)
    
    # Calculate auto widths for cells with colspan > 1
    while True:
        adjustedColumns = []
        adjustedWidth = 0
        
        for r in node.rows:
            for i in range(len(r.cells)):
                c = r.cells[i]
                if c is None or c.content is None or c.colspan == 1: continue
                
                columns = node.columns[i : i + c.colspan]
                autoColumns = [x for x in columns if x.auto]
                if len(autoColumns) == 0: continue   # nothing to adjust                
                fixedColumns = [x for x in columns if not x.auto]
                
                fixedWidth = sum([x.spaceAfter for x in columns[:-1]])
                if len(fixedColumns) > 0: 
                    fixedWidth += sum ([x.width for x in fixedColumns])
                autoWidth = sum ([x.width for x in autoColumns])
                if c.content.width <= fixedWidth + autoWidth: continue # already fits
                
                requiredWidth = c.content.width - fixedWidth
                unitWidth = requiredWidth / len(autoColumns)
                
                while True:
                    oversizedColumns = [x for x in autoColumns if x.width >= unitWidth]
                    if len(oversizedColumns) == 0: break
                    
                    autoColumns = [x for x in autoColumns if x.width < unitWidth]
                    if len(autoColumns) == 0: break  # weird rounding effects
                    requiredWidth -=  sum ([x.width for x in oversizedColumns])
                    unitWidth = requiredWidth / len(autoColumns)
                if len(autoColumns) == 0: continue; # protection against arithmetic overflow
                
                # Store the maximum unit width
                if unitWidth > adjustedWidth:
                    adjustedWidth = unitWidth
                    adjustedColumns = autoColumns
                
        if len(adjustedColumns) == 0: break;
        for col in adjustedColumns: col.width = adjustedWidth
    
    if node.getProperty(u"equalcolumns") == u"true":
        globalWidth = max([col.width for col in node.columns if col.auto])
        for col in node.columns: 
            if col.auto: col.width = globalWidth
            
    if fullwidth is not None:
        delta = fullwidth 
        delta -= sum ([x.width for x in node.columns])
        delta -= sum ([x.spaceAfter for x in node.columns[:-1]]) 
        delta -= 2 * node.framespacings[0]
        if delta != 0:        
            sizableColumns = [x for x in node.columns if x.fit]
            if len(sizableColumns) == 0: 
                sizableColumns = [x for x in node.columns if x.auto]
            if len(sizableColumns) == 0: 
                node.error("Overconstrained table layout: explicit table width specified, but no column has automatic width; table width attribute ignored")
            else:
                delta /= len(sizableColumns)
                for col in sizableColumns: col.width += delta         
    
def calculateRowHeights(node):
    # Set  initial row heights for cells with rowspan == 1
    commonAxis = node.axis()
    for r in node.rows:
        r.height = 0
        r.depth  = 0
        for c in r.cells:
            if c is None or c.content is None or c.rowspan != 1: continue
            cellAxis = c.content.axis()            
            c.vshift = 0
            
            if c.valign == u"baseline":
                if r.alignToAxis: cell.vshift -= commonAxis           
                if c.content.alignToAxis: c.vshift += cellAxis
            
            elif c.valign == u"axis":
                if not r.alignToAxis: c.vshift += commonAxis           
                if not c.content.alignToAxis: c.vshift -= cellAxis
            
            else:
               c.vshift = (r.height - r.depth - c.content.height + c.content.depth) / 2

            r.height = max(r.height, c.content.height + c.vshift) 
            r.depth = max(r.depth, c.content.depth - c.vshift)

    # Calculate heights for cells with rowspan > 1
    while True:
        adjustedRows = []
        adjustedSize = 0
        for i in range(len(node.rows)):
            r = node.rows[i]
            for c in r.cells:
                if c is None or c.content is None or c.rowspan == 1: continue
                rows = node.rows[i : i + c.rowspan]
                
                requiredSize = c.content.height + c.content.depth
                requiredSize -= sum([x.spaceAfter for x in rows[:-1]])
                fullSize = sum ([x.height + x.depth for x in rows])
                if fullSize >= requiredSize: continue   
                
                unitSize = requiredSize / len(rows)
                while True:
                    oversizedRows = [x for x in rows if x.height + x.depth >= unitSize]
                    if len(oversizedRows) == 0: break

                    rows = [x for x in rows if x.height + x.depth < unitSize]
                    if len(rows) == 0: break  # weird rounding effects
                    requiredSize -= sum ([x.height + x.depth for x in oversizedRows])
                    unitSize = requiredSize / len(rows)  
                if len(rows) == 0: continue; # protection against arithmetic overflow
                    
                if unitSize > adjustedSize:
                    adjustedSize = unitSize
                    adjustedRows = rows
                
        if len(adjustedRows) == 0: break;
        for r in adjustedRows: 
            delta = (adjustedSize - r.height - r.depth) / 2
            r.height += delta; r.depth += delta

    if node.getProperty(u"equalrows") == u"true":
        maxvsize = max([r.height + r.depth for r in node.rows])
        for r in node.rows:
            delta = (maxvsize - r.height - r.depth) / 2
            r.height += delta; r.depth += delta
    
    
def getAlign(node):
    alignattr = node.getProperty(u"align").strip()
    if len(alignattr) == 0: alignattr = mathnode.globalDefaults[u"align"]
    
    splitalign = alignattr.split() 
    alignType = splitalign[0]

    if len(splitalign) == 1:
        alignRow = None
    else:
        alignRow = node.parseInt(splitalign[1])
        if alignrownumber == 0:
            node.error("Alignment row number cannot be zero")
            alignrownumber = None
        elif alignrownumber > len(node.rows):
            node.error("Alignment row number cannot exceed row count")
            alignrownumber = len(node.rows)
        elif alignrownumber < - len(node.rows):
            node.error("Negative alignment row number cannot exceed row count")
            alignrownumber = 1
        elif alignrownumber < 0:
            alignrownumber = len(node.rows) - alignrownumber + 1 

    return (alignType, alignRow)