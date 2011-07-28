# Makefile for SVG 1.1 Second Edition.

all :
	$(MAKE) -C images/implnote/arcs/
	@./build.pl

pdf : all
	prince --no-author-style -s ../publish/style/svg-style.css -s http://www.w3.org/StyleSheets/TR/W3C-REC -s ../publish/style/svg-style-print.css ../publish/single-page.html -o ../publish/single-page.pdf

ZIPDIR=REC-SVG11-20110802

zip : all
	rm -rf ../publish/$(ZIPDIR) ../publish/$(ZIPDIR).zip
	mkdir -p ../publish/$(ZIPDIR)/style
	cp ../publish/*.html ../publish/$(ZIPDIR)
	rm ../publish/$(ZIPDIR)/single-page.html
	cp ../publish/style/svg-style{,-extra}.css ../publish/$(ZIPDIR)/style/
	wget -O ../publish/$(ZIPDIR)/style/W3C-REC.css http://www.w3.org/StyleSheets/TR/W3C-REC.css
	wget -O ../publish/$(ZIPDIR)/style/logo-REC.png http://www.w3.org/StyleSheets/TR/logo-REC.png
	perl -i -pe 's{http://www.w3.org/StyleSheets/TR/logo-REC}{logo-REC.png}' ../publish/$(ZIPDIR)/style/W3C-REC.css
	perl -i -pe 's{http://www.w3.org/StyleSheets/TR/W3C-REC}{style/W3C-REC.css}' ../publish/$(ZIPDIR)/*.html
	cp -a ../publish/images ../publish/$(ZIPDIR)/
	find ../publish/$(ZIPDIR)/images/ -name CVS | xargs rm -rf
	cd ../publish/ && zip -r $(ZIPDIR).zip $(ZIPDIR)
	rm -rf ../publish/$(ZIPDIR)

clean :
	$(MAKE) -C images/implnote/arcs/ clean
	@./build.pl -c
