SHELL = bash

PDFLATEX = pdflatex -interaction=nonstopmode -shell-escape
SVG2PDF = inkscape -z

TEX += doc.tex
TEX += $(wildcard tex/*.tex)
SVG += $(wildcard inc/*.svg)
DOT += $(wildcard inc/*.dot)

GEN_PDF += $(patsubst inc/%.svg, inc/%.pdf, $(SVG))
GEN_PDF += $(patsubst inc/%.dot, inc/%.pdf, $(DOT))

#PDF += inc/title.pdf
PDF += $(GEN_PDF)
PDF += inc/idef0.pdf
PDF += inc/idef0-general.pdf
PDF += inc/idef0-specific.pdf

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

inc/%.svg: inc/%.dot $(MAKEFILE)
	dot -Tsvg $< > $@

clean:
	rm -rf $(GEN_PDF) doc.pdf doc.aux doc.log doc.out doc.toc doc.idx \
		tex/*.aux inc/fsm.* inc/*.tex tex/*.log inc/*.conv.svg
