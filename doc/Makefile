SHELL = bash
DIR = $(shell pwd)

PDFLATEX = pdflatex -interaction=nonstopmode -shell-escape
SVG2PDF = inkscape -z
FORMAT_TEST_LOG = $(DIR)/utils/format_test_log.py
PATTERN_MODEL = env PYTHONPATH=../src/match_pattern ../src/match_pattern/pattern_model.py
MODEL_GRAPH_TO_DOT = env PYTHONPATH=../src/match_pattern ../src/match_pattern/model_graph_to_dot.py
MATCH_PATTERN = env PYTHONPATH=../src/match_pattern ../src/match_pattern/match_pattern.py
JAVA_BYTECODE_MODEL = java -jar ../src/java_bytecode_model/target/java_bytecode_model-1.0-SNAPSHOT.jar

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

doc.pdf: $(TEX) $(PDF) $(TEST_LOG) inc/apache-bcel-adapter.pdf inc/apache-bcel-bridge.pdf
	$(PDFLATEX) doc.tex && \
	$(PDFLATEX) doc.tex

inc/%.pdf: inc/%.conv.svg
	$(SVG2PDF) --export-pdf=$@ --file=$<

inc/%.conv.svg: inc/%.svg
	cat $< | \
	sed 's/textLength="[^"]*" *//g' | \
	sed 's/lengthAdjust="spacingAndGlyphs" *//g' > $@

inc/%.svg: inc/%.dot
	dot -T svg $< > $@

inc/graph_matcher_test.log:
	cd ../src/match_pattern && python2 -m pytest -v graph_matcher/test/*.py | $(FORMAT_TEST_LOG) > ../../doc/inc/graph_matcher_test.log || \
		rm -f ../../doc/inc/graph_matcher_test.log

inc/java_source_parser_test.log:
	cd ../src/match_pattern && python2 -m pytest -v java_source_parser/test/*.py | $(FORMAT_TEST_LOG) > ../../doc/inc/java_source_parser_test.log || \
		rm -f ../../doc/inc/java_source_parser_test.log

inc/pattern_matcher_test.log:
	cd ../src/match_pattern && python2 -m pytest -v pattern_matcher/test/*.py | $(FORMAT_TEST_LOG) > ../../doc/inc/pattern_matcher_test.log || \
		rm -f ../../doc/inc/pattern_matcher_test.log

inc/java_bytecode_model_test.log: ../src/java_bytecode_model/target/java_bytecode_model-1.0-SNAPSHOT.jar
	cd ../src/test && python2 -m pytest -v java_bytecode_model.py | $(FORMAT_TEST_LOG) > ../../doc/inc/java_bytecode_model_test.log || \
		rm -f ../../doc/inc/java_bytecode_model_test.log

inc/match_pattern_test.log:
	cd ../src/test && python2 -m pytest -v match_pattern.py | $(FORMAT_TEST_LOG) > ../../doc/inc/match_pattern_test.log || \
		rm -f ../../doc/inc/match_pattern_test.log

inc/%-graph.dot:
	$(PATTERN_MODEL) $* | $(MODEL_GRAPH_TO_DOT) > $@

inc/apache-bcel-adapter.pdf: temp/matches/apache-bcel-adapter.svg
	$(SVG2PDF) --export-pdf=$@ --file=$<

inc/apache-bcel-bridge.pdf: temp/matches/apache-bcel-bridge.svg
	$(SVG2PDF) --export-pdf=$@ --file=$<

temp/matches/apache-bcel-adapter.svg: temp/models/bcel-6.0.yaml temp/patterns/adapter.yaml temp/matches
	$(MATCH_PATTERN) -t -v INFO -l 1 -f dot.svg temp/models/bcel-6.0.yaml temp/patterns/adapter.yaml > temp/matches/apache-bcel-adapter.svg || \
		rm -f temp/apache-bcel-adapter.svg

temp/matches/apache-bcel-bridge.svg: temp/models/bcel-6.0.yaml temp/patterns/bridge.yaml temp/matches
	$(MATCH_PATTERN) -t -v INFO -l 1 -f dot.svg temp/models/bcel-6.0.yaml temp/patterns/bridge.yaml > temp/matches/apache-bcel-bridge.svg || \
		rm -f temp/apache-bcel-bridge.svg

temp/models/bcel-6.0.yaml: temp/models src/bcel-6.0 ../src/java_bytecode_model/target/java_bytecode_model-1.0-SNAPSHOT.jar
	$(JAVA_BYTECODE_MODEL) src/bcel-6.0 > temp/models/bcel-6.0.yaml

temp/patterns/adapter.yaml: temp/patterns
	$(PATTERN_MODEL) Adapter > temp/patterns/adapter.yaml

temp/patterns/bridge.yaml: temp/patterns
	$(PATTERN_MODEL) Bridge > temp/patterns/bridge.yaml

temp/matches:
	mkdir -p temp/matches

temp/patterns:
	mkdir -p temp/patterns

temp/models:
	mkdir -p temp/models

../src/java_bytecode_model/target/java_bytecode_model-1.0-SNAPSHOT.jar:
	cd ../src/java_bytecode_model && mvn install

clean:
	rm -rf $(GEN_PDF) \
		doc.pdf \
		doc.aux \
		doc.log \
		doc.out \
		doc.toc \
		doc.idx \
		tex/*.aux \
		inc/*.tex \
		tex/*.log \
		inc/*.conv.svg \
		temp \
