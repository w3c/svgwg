# Makefile for specs under http://svgwg.org/hg/svg2/specs/.

TOOLS=../../tools

all :
	@$(TOOLS)/build.py

clean :
	@$(TOOLS)/build.py -c

.PHONY : all clean
