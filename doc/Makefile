SHELL = bash
DIR = $(shell pwd)

PDFLATEX = pdflatex -interaction=nonstopmode -shell-escape
SVG2PDF = inkscape -z
FORMAT_TEST_LOG = $(DIR)/utils/format_test_log.py
PATTERN_MODEL = ../src/match_pattern/pattern_model.py
MODEL_GRAPH_TO_DOT = ../src/match_pattern/model_graph_to_dot.py

PATTERN = $(shell $(PATTERN_MODEL))

GRAPH = $(patsubst %, %-graph, $(PATTERN))

DOT += $(wildcard inc/*.dot)
DOT += $(patsubst %, inc/%.dot, $(GRAPH))

SVG += $(wildcard inc/*.svg)
SVG += $(patsubst %, inc/%.svg, $(GRAPH))

TEX += doc.tex
TEX += $(wildcard tex/*.tex)

GEN_PDF += $(patsubst inc/%.svg, inc/%.pdf, $(SVG))
GEN_PDF += $(patsubst inc/%.dot, inc/%.pdf, $(DOT))

PDF += $(GEN_PDF)
PDF += inc/title.pdf
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
	sed 's/lengthAdjust="spacingAndGlyphs" *//g' > $@

inc/%.svg: inc/%.dot
	dot -T svg $< > $@

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

inc/%-graph.dot:
	$(PATTERN_MODEL) $* | $(MODEL_GRAPH_TO_DOT) > $@

clean:
	rm -f $(GEN_PDF) \
	doc.pdf \
	doc.aux \
	doc.log \
	doc.out \
	doc.toc \
	doc.idx \
	tex/*.aux \
	inc/*.tex \
	tex/*.log \
	inc/*.conv.svg
