all: index.html

index.html: index.bs
	bikeshed -f spec index.bs

online:
	curl https://api.csswg.org/bikeshed/ -F file=@index.bs -F force=1 > index.html
