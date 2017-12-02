LATEX	= pdflatex -shell-escape
BIBTEX	= bibtex

SRC	:= $(shell egrep -l '^[^%]*\\begin\{document\}' *.tex)
TRG	= $(SRC:%.tex=%.dvi)
PSF	= $(SRC:%.tex=%.ps)
PDF	= $(SRC:%.tex=%.pdf)

pdf: $(PDF)
	rm -f *.out *.log *.aux *.bbl *.blg *.toc *.lof


$(PDF): %.pdf: %.tex
	$(LATEX) $<
	$(BIBTEX) $(<:%.tex=%.aux)
	$(LATEX) $<
	$(LATEX) $<

all: pdf

clean:
	rm -f *.pdf *.out *.log *.aux *.bbl *.blg *.toc *.lof

.PHONY: all clean pdf
