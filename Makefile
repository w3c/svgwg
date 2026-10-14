# Makefile for SVG 2 and the modules under specs/.
#
# SVG 2 is written in Bikeshed, in master/*.bs. The modules still use the
# old build (tools/build.py). See tools/svg2-build/README.md.

all :
	./tools/svg2-build/build.sh

all-specs : all
	@for spec in specs/*; do if [ -f $$spec/Makefile -a $$spec != 'specs/template' ]; then echo && echo "Building $$spec" && make -s -C $$spec/ all; fi; done

# Fails when the build lost an id that SVG 2 has published
# (tools/svg2-build/baseline/).
check : all
	./tools/svg2-build/check.sh

# Unit tests of the build scripts: standard library only, no Bikeshed,
# no network, a few seconds. See "Tests" in tools/svg2-build/README.md.
test :
	python3 -m unittest discover -s tools/svg2-build/tests -t tools/svg2-build

clean :
	rm -rf build/bikeshed

.PHONY : all all-specs check test clean

pdf : all
	prince build/bikeshed/svg2-draft/single-page.html -o build/bikeshed/svg2-draft/single-page.pdf

stabilize-issues-all-specs :
	@for spec in specs/*; do if [ -f $$spec/Makefile -a $$spec != 'specs/template' -a $$spec != 'specs/svg-native' ]; then make -s -C $$spec/ stabilize-issues; fi; done
