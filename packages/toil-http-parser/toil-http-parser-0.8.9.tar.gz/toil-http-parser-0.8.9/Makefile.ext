# This file is renamed to "Makefile.ext" in release tarballs so that
# setup.py won't try to run it.  If you want setup.py to run "make"
# automatically, rename it back to "Makefile".

all: toil_http_parser/parser.c

toil_http_parser/parser.c: toil_http_parser/parser.pyx
	cython -o toil_http_parser.parser.c toil_http_parser/parser.pyx
	mv toil_http_parser.parser.c toil_http_parser/parser.c

clean:
	rm -f toil_http_parser/parser.c


.PHONY: clean all
