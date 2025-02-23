#!/bin/sh
rm $1.aux
rm $1.bbl
rm $1.blg
rm $1.out
rm $1.log
rm $1.pdf

lualatex $1.tex

# da Zotero fare xport bibtex NON biblatex!
bibtex $1.aux
lualatex $1.tex
lualatex $1.tex
