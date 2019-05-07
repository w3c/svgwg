# Make the svgwg.org build machine prefer the online version of Bikeshed.
all : $(if $(BUILD_MACHINE),online,local)

local : index.bs
	bikeshed -f spec index.bs

online : index.bs
	curl -s https://api.csswg.org/bikeshed/ -F file=@index.bs -F force=1 > index.html

clean :
	rm -f index.html

.PHONY : all local online clean
