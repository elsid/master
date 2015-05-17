SHELL = bash

PDFLATEX = pdflatex -interaction=nonstopmode -shell-escape
SVG2PDF = inkscape -z

TEX += doc.tex
TEX += $(wildcard tex/*.tex)
SVG += $(wildcard inc/*.svg)
DEF += $(wildcard ../src/*.def)

#PDF += inc/title.pdf
PDF += $(patsubst inc/%.svg, inc/%.pdf, $(SVG))

MAKEFILE += Makefile

all: doc.pdf

doc.pdf: $(TEX) $(PDF) $(MAKEFILE)
	$(PDFLATEX) doc.tex &> /dev/null && \
	$(PDFLATEX) doc.tex &> /dev/null

inc/%.pdf: inc/%.conv.svg $(MAKEFILE)
	$(SVG2PDF) --export-pdf=$@ --file=$<

inc/%.conv.svg: inc/%.svg $(MAKEFILE)
	cat $< | \
	sed 's/textLength="[^"]*" *//g' | \
	sed 's/font-size="[^"]*"/font-size="14"/g' | \
	sed 's/lengthAdjust="spacingAndGlyphs" *//g' | \
	sed 's/font-family="[^"]*"/font-family="Times New Roman"/g' > $@

clean:
	rm -rf $(PDF) doc.pdf doc.aux doc.log doc.out doc.toc doc.idx tex/*.aux \
		inc/fsm.* inc/*.pdf inc/*.tex tex/*.log inc/*.conv.svg
