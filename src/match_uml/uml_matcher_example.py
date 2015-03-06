#!/usr/bin/env python
# coding: utf-8


from uml_matcher.test.diagram import (
    DecoratorPatternDiagramFactory, TargetDiagramFactory)


def print_graph_match_result(result):
    for index, variant in enumerate(result):
        print(index)
        for mapping in variant:
            print('\t', mapping)


def print_uml_match_result(result):
    print_graph_match_result(result.generalizations)
    print_graph_match_result(result.associations)

if __name__ == '__main__':
    pattern = DecoratorPatternDiagramFactory().diagram()
    target = TargetDiagramFactory().diagram()
    print(pattern)
    print(target)
    print_uml_match_result(target.match(pattern))
