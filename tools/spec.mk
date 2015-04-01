# Makefile for specs under https://github.com/w3c/svgwg/tree/master/specs.

TOOLS=../../tools

all :
	@$(TOOLS)/build.py

clean :
	@$(TOOLS)/build.py -c

stabilize-issues :
	@$(TOOLS)/build.py -s

.PHONY : all clean stabilize-issues
