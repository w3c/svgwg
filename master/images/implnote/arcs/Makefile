# Makefile for generating SVGs and PNGs from the MathML documents in this directory.

SVG2PNG=java -jar ../../../../../../tools/batik/batik-rasterizer.jar

# This directory relative to tools/math/.
THISDIR=../../profiles/1.1F2/master/images/implnote/arcs

MML_FILES=$(wildcard *.mml)

all : $(MML_FILES:%.mml=%.png)

%.svg : %.mml
	cd ../../../../../../tools/math && ./math2svg.py -o $(THISDIR)/$@ $(THISDIR)/$<

%.png : %.svg
	$(SVG2PNG) -cssUser 'data:text/css,svg{text-rendering:geometricPrecision}' -d $@ $<
clean :
	rm -f $(MML_FILES:%.mml=%.png) $(MML_FILES:%.mml=%.svg)

.PRECIOUS : %.svg
.PHONY : all clean
