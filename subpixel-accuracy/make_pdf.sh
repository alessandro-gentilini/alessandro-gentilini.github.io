#!/bin/sh
rm subpixel-accuracy.aux
rm subpixel-accuracy.bbl
rm subpixel-accuracy.blg
rm subpixel-accuracy.out
rm subpixel-accuracy.log

pdflatex subpixel-accuracy.tex
bibtex subpixel-accuracy.aux
pdflatex subpixel-accuracy.tex
pdflatex subpixel-accuracy.tex

rm subpixel-accuracy.aux
rm subpixel-accuracy.bbl
rm subpixel-accuracy.blg
rm subpixel-accuracy.out
rm subpixel-accuracy.log
