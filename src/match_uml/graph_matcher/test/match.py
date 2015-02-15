#!/usr/bin/env python3
#coding: utf-8

from unittest import TestCase, main
from itertools import permutations
from hamcrest import assert_that, equal_to, contains_inanyorder
from graph_matcher.match import match
from graph_matcher.graph import Graph

def replace_node_by_obj(variants):
    return [[tuple((p[0].obj, p[1].obj)) for p in v] for v in variants]

class MatchTest(TestCase):
    def test_match_empty_should_succeed(self):
        assert_that(list(match(Graph(), Graph())), equal_to([]))

    def test_match_with_one_node_should_succeed(self):
        first = Graph({1})
        second = Graph({'a'})
        first_variants = replace_node_by_obj(match(first, second))
        assert_that(first_variants, equal_to([[(1, 'a')]]))
        second_variants = replace_node_by_obj(match(second, first))
        assert_that(second_variants, equal_to([[('a', 1)]]))

    def test_match_with_one_edge_should_succeed(self):
        first = Graph({(1, 2)})
        second = Graph({('a', 'b')})
        first_variants = replace_node_by_obj(match(first, second))
        assert_that(first_variants, equal_to([[(1, 'a'), (2, 'b')]]))
        second_variants = replace_node_by_obj(match(second, first))
        assert_that(second_variants, equal_to([[('a', 1), ('b', 2)]]))

    def test_match_with_self_connected_nodes_should_succeed(self):
        first = Graph({(1, 1)})
        second = Graph({('a', 'a')})
        first_variants = replace_node_by_obj(match(first, second))
        assert_that(first_variants, equal_to([[(1, 'a')]]))
        second_variants = replace_node_by_obj(match(second, first))
        assert_that(second_variants, equal_to([[('a', 1)]]))

    def test_match_complete_graphs_and_should_succeed(self):
        first = Graph([(p[0], p[1]) for p in permutations((1, 2, 3, 4))])
        second = Graph([(p[0], p[1]) for p in permutations('abcd')])
        variants = replace_node_by_obj(match(first, second))
        assert_that(variants, contains_inanyorder(
            [(1, 'a'), (2, 'b'), (3, 'c'), (4, 'd')],
            [(1, 'a'), (2, 'b'), (3, 'd'), (4, 'c')],
            [(1, 'a'), (2, 'c'), (3, 'b'), (4, 'd')],
            [(1, 'a'), (2, 'c'), (3, 'd'), (4, 'b')],
            [(1, 'a'), (2, 'd'), (3, 'b'), (4, 'c')],
            [(1, 'a'), (2, 'd'), (3, 'c'), (4, 'b')],
            [(1, 'b'), (2, 'a'), (3, 'c'), (4, 'd')],
            [(1, 'b'), (2, 'a'), (3, 'd'), (4, 'c')],
            [(1, 'b'), (2, 'c'), (3, 'a'), (4, 'd')],
            [(1, 'b'), (2, 'c'), (3, 'd'), (4, 'a')],
            [(1, 'b'), (2, 'd'), (3, 'a'), (4, 'c')],
            [(1, 'b'), (2, 'd'), (3, 'c'), (4, 'a')],
            [(1, 'c'), (2, 'a'), (3, 'b'), (4, 'd')],
            [(1, 'c'), (2, 'a'), (3, 'd'), (4, 'b')],
            [(1, 'c'), (2, 'b'), (3, 'a'), (4, 'd')],
            [(1, 'c'), (2, 'b'), (3, 'd'), (4, 'a')],
            [(1, 'c'), (2, 'd'), (3, 'a'), (4, 'b')],
            [(1, 'c'), (2, 'd'), (3, 'b'), (4, 'a')],
            [(1, 'd'), (2, 'a'), (3, 'b'), (4, 'c')],
            [(1, 'd'), (2, 'a'), (3, 'c'), (4, 'b')],
            [(1, 'd'), (2, 'b'), (3, 'a'), (4, 'c')],
            [(1, 'd'), (2, 'b'), (3, 'c'), (4, 'a')],
            [(1, 'd'), (2, 'c'), (3, 'a'), (4, 'b')],
            [(1, 'd'), (2, 'c'), (3, 'b'), (4, 'a')],
        ))

    def test_match_different_graphs_should_succeed(self):
        first = Graph({(1, 2), (2, 3), (3, 4)})
        second = Graph({('a', 'b'), ('b', 'c'), ('c', 'a')})
        variants = replace_node_by_obj(match(first, second))
        assert_that(variants, equal_to([]))

if __name__ == '__main__':
    main()
