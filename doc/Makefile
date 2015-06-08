SHELL = bash
DIR = $(shell pwd)

PDFLATEX = pdflatex -interaction=nonstopmode -shell-escape
SVG2PDF = inkscape -z
FORMAT_TEST_LOG = $(DIR)/utils/format_test_log.py

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

TEST_LOG += inc/graph_matcher_test.log
TEST_LOG += inc/java_source_parser_test.log
TEST_LOG += inc/pattern_matcher_test.log
TEST_LOG += inc/java_bytecode_model_test.log
TEST_LOG += inc/match_pattern_test.log

all: doc.pdf

doc.pdf: $(TEX) $(PDF) $(TEST_LOG)
	$(PDFLATEX) doc.tex &> /dev/null && \
	$(PDFLATEX) doc.tex &> /dev/null

inc/%.pdf: inc/%.conv.svg
	$(SVG2PDF) --export-pdf=$@ --file=$<

inc/%.conv.svg: inc/%.svg
	cat $< | \
	sed 's/textLength="[^"]*" *//g' | \
	sed 's/font-size="[^"]*"/font-size="14"/g' | \
	sed 's/lengthAdjust="spacingAndGlyphs" *//g' | \
	sed 's/font-family="[^"]*"/font-family="Times New Roman"/g' > $@

inc/%.svg: inc/%.dot
	dot -Tsvg $< > $@

inc/graph_matcher_test.log:
	cd ../src/match_pattern && py.test -v graph_matcher/test/*.py | $(FORMAT_TEST_LOG) > ../../doc/inc/graph_matcher_test.log

inc/java_source_parser_test.log:
	cd ../src/match_pattern && py.test -v java_source_parser/test/*.py | $(FORMAT_TEST_LOG) > ../../doc/inc/java_source_parser_test.log

inc/pattern_matcher_test.log:
	cd ../src/match_pattern && py.test -v pattern_matcher/test/*.py | $(FORMAT_TEST_LOG) > ../../doc/inc/pattern_matcher_test.log

inc/java_bytecode_model_test.log:
	cd ../src/test && py.test -v java_bytecode_model.py | $(FORMAT_TEST_LOG) > ../../doc/inc/java_bytecode_model_test.log

inc/match_pattern_test.log:
	cd ../src/test && py.test -v match_pattern.py | $(FORMAT_TEST_LOG) > ../../doc/inc/match_pattern_test.log

clean:
	rm -rf $(GEN_PDF) doc.pdf doc.aux doc.log doc.out doc.toc doc.idx \
		tex/*.aux inc/fsm.* inc/*.tex tex/*.log inc/*.conv.svg inc/*.log
