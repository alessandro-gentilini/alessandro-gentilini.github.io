#!/bin/sh
rm appunti.aux
rm appunti.bbl
rm appunti.blg
rm appunti.out
rm appunti.log
rm apunti.pdf

pdflatex appunti.tex

# da Zotero fare xport bibtex NON biblatex!
bibtex appunti.aux
pdflatex appunti.tex
pdflatex appunti.tex
