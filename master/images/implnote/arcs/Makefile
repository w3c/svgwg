# Makefile for generating SVGs and PNGs from the MathML documents in this directory.

THISDIR=$(abspath .)
TARGETDIR=$(abspath ../../../../build/publish/images/implnote/arcs)
TOOLSDIR=$(abspath ../../../../../svg2-tools)

SVG2PNG=java -jar $(TOOLSDIR)/batik/batik-rasterizer.jar

MML_FILES=$(wildcard *.mml)

all : $(MML_FILES:%.mml=$(TARGETDIR)/%.png)

$(TARGETDIR)/%.svg : %.mml
	mkdir -p $(TARGETDIR)
	cd $(TOOLSDIR)/math && ./math2svg.py -o $@ $(THISDIR)/$<

$(TARGETDIR)/%.png : $(TARGETDIR)/%.svg
	$(SVG2PNG) -cssUser 'data:text/css,svg{text-rendering:geometricPrecision}' -d $@ $<
clean :
	rm -f $(MML_FILES:%.mml=$(TARGETDIR)/%.png) $(MML_FILES:%.mml=$(TARGETDIR)/%.svg)

.PRECIOUS : $(TARGETDIR)/%.svg
.PHONY : all clean
