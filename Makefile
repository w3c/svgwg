# Makefile for SVG 2.

TOOLS=./tools
include tools/spec.mk

all-specs : all
	@for spec in specs/*; do if [ -f $$spec/Makefile -a $$spec != 'specs/template' ]; then echo && echo "Building $$spec" && make -s -C $$spec/ all; fi; done

# Bikeshed version of SVG 2, built side by side with the current one.
# See tools/bikeshed/README.md.
bikeshed :
	./tools/bikeshed/build.sh

bikeshed-check : all bikeshed
	./tools/bikeshed/check.sh

# Unit tests of the conversion scripts: standard library only, no Bikeshed,
# no network, a few seconds. See "Tests" in tools/bikeshed/README.md.
bikeshed-test :
	python3 -m unittest discover -s tools/bikeshed/tests -t tools/bikeshed

.PHONY : bikeshed bikeshed-check bikeshed-test

pdf : all
	prince --no-author-style -s build/publish/style/svg-style.css -s http://www.w3.org/StyleSheets/TR/W3C-REC -s build/publish/style/svg-style-print.css build/publish/single-page.html -o build/publish/single-page.pdf

stabilize-issues-all-specs : stabilize-issues
	@for spec in specs/*; do if [ -f $$spec/Makefile -a $$spec != 'specs/template' -a $$spec != 'specs/svg-native' ]; then make -s -C $$spec/ stabilize-issues; fi; done

ZIPDIR=REC-SVG11-20110802

zip : all
	rm -rf build/publish/$(ZIPDIR) build/publish/$(ZIPDIR).zip
	mkdir -p build/publish/$(ZIPDIR)/style
	cp build/publish/*.html build/publish/$(ZIPDIR)
	rm build/publish/$(ZIPDIR)/single-page.html
	cp build/publish/style/svg-style.css build/publish/$(ZIPDIR)/style/
	wget -O build/publish/$(ZIPDIR)/style/W3C-REC.css http://www.w3.org/StyleSheets/TR/W3C-REC.css
	wget -O build/publish/$(ZIPDIR)/style/logo-REC.png http://www.w3.org/StyleSheets/TR/logo-REC.png
	perl -i -pe 's{http://www.w3.org/StyleSheets/TR/logo-REC}{logo-REC.png}' build/publish/$(ZIPDIR)/style/W3C-REC.css
	perl -i -pe 's{http://www.w3.org/StyleSheets/TR/W3C-REC}{style/W3C-REC.css}' build/publish/$(ZIPDIR)/*.html
	cp -a build/publish/images build/publish/$(ZIPDIR)/
	find build/publish/$(ZIPDIR)/images/ -name CVS | xargs rm -rf
	cd build/publish/ && zip -r $(ZIPDIR).zip $(ZIPDIR)
	rm -rf build/publish/$(ZIPDIR)
