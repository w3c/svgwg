# Makefile for specs under https://github.com/w3c/svgwg/tree/main/specs.

TOOLS?=../../tools

all :
	@$(TOOLS)/build.py

clean :
	@$(TOOLS)/build.py -c

stabilize-issues :
	@$(TOOLS)/build.py -s

list-external-links :
	@$(TOOLS)/build.py -L

lint :
	@$(TOOLS)/build.py -l

.PHONY : all clean stabilize-issues list-external-links lint
