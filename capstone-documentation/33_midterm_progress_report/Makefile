LATEX	= pdflatex -shell-escape

SRC	:= $(shell egrep -l '^[^%]*\\begin\{document\}' *.tex)
PDF	= $(SRC:%.tex=%.pdf)

pdf: $(PDF)
	rm -f *.out *.log *.aux *.bbl *.blg *.toc *.lof

$(PDF): %.pdf: %.tex
	$(LATEX) $<
	$(LATEX) $<

all: pdf

clean:
	rm -f *.pdf *.out *.log *.aux *.bbl *.blg *.toc *.lof

.PHONY: all clean pdf
