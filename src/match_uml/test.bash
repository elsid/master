#!/usr/bin/env bash

python -m unittest $@ \
    graph_matcher.test \
    java_parser.test \
    uml_matcher.test
