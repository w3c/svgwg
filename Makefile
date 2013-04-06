# Makefile for SVG 1.1 Second Edition.

all-with-tools-check : tools-check all

all-specs : all
	@for spec in specs/*; do [ -f $$spec/Makefile ] && make -C $$spec/ all; done

tools-check :
	@bash -c "REMOTE_REV=$$(hg id -i http://svgwg.org/hg/svg2-tools); [ \$$? = 0 -o \"\$$REMOTE_REV\" != \"\" ] || exit 0; LOCAL_REV=$$(hg id -i ../svg2-tools); [ \"\$$LOCAL_REV\" = \"\$$REMOTE_REV\" -o \"\$$LOCAL_REV\" = \"\$$REMOTE_REV\"+ ] || (echo \"You must update your svg2-tools repository! (Remote repository has revision \$$REMOTE_REV, but you are at \$$LOCAL_REV.)\"; exit 1)"

all :
	@../svg2-tools/build.py

pdf : all
	prince --no-author-style -s build/publish/style/svg-style.css -s http://www.w3.org/StyleSheets/TR/W3C-REC -s build/publish/style/svg-style-print.css build/publish/single-page.html -o build/publish/single-page.pdf

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

clean :
	@../svg2-tools/build.py -c

