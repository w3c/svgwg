# Make the w3c.github.io/svgwg build machine prefer the online version of Bikeshed.
all : $(if $(BUILD_MACHINE),online,local)

local : index.bs
	bikeshed -f spec index.bs

online : index.bs
	curl -s https://www.w3.org/publications/spec-generator/ -F file=@index.bs -F type=bikeshed-spec -F die-on=nothing > index.html

clean :
	rm -f index.html

.PHONY : all local online clean
