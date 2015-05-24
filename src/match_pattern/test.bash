#!/usr/bin/env bash

python -m unittest $@ \
    graph_matcher.test \
    java_source_parser.test \
    pattern_matcher.test
