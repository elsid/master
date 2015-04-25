#!/usr/bin/env python
# coding: utf-8

from unittest import TestCase
from itertools import permutations
from hamcrest import assert_that, equal_to, contains_inanyorder, empty
from graph_matcher.match import Equivalent, match, replace_node_by_obj
from graph_matcher.graph import Graph


class Match(TestCase):
    def test_match_empty_should_succeed(self):
        assert_that(list(match(Graph(), Graph())), empty())

    def test_match_with_one_node_should_succeed(self):
        first = Graph({1})
        second = Graph({'a'})
        first_variants = replace_node_by_obj(match(first, second))
        assert_that(first_variants, equal_to(
            [[Equivalent(target=1, pattern='a')]]))
        second_variants = replace_node_by_obj(match(second, first))
        assert_that(second_variants, equal_to(
            [[Equivalent(target='a', pattern=1)]]))

    def test_match_with_one_and_with_two_components_should_succeed(self):
        first = Graph({1})
        second = Graph({'a', 'b'})
        first_variants = replace_node_by_obj(match(first, second))
        assert_that(first_variants, contains_inanyorder(
            [(1, 'a')], [(1, 'b')]
        ))
        second_variants = replace_node_by_obj(match(second, first))
        assert_that(second_variants, contains_inanyorder(
            [('a', 1)], [('b', 1)]
        ))

    def test_match_with_two_components_should_succeed(self):
        first = Graph({1, 2})
        second = Graph({'a', 'b'})
        first_variants = replace_node_by_obj(match(first, second))
        assert_that(first_variants, contains_inanyorder(
            [(1, 'a'), (2, 'b')], [(1, 'b'), (2, 'a')]
        ))
        second_variants = replace_node_by_obj(match(second, first))
        assert_that(second_variants, contains_inanyorder(
            [('a', 1), ('b', 2)], [('a', 2), ('b', 1)]
        ))

    def test_match_with_two_and_three_components_should_succeed(self):
        first = Graph({1, 2})
        second = Graph({'a', 'b', 'c'})
        first_variants = replace_node_by_obj(match(first, second))
        assert_that(first_variants, contains_inanyorder(
            [(1, 'c'), (2, 'b')], [(1, 'b'), (2, 'c')], [(1, 'c'), (2, 'a')],
            [(1, 'a'), (2, 'c')], [(1, 'b'), (2, 'a')], [(1, 'a'), (2, 'b')],
        ))
        second_variants = replace_node_by_obj(match(second, first))
        assert_that(second_variants, contains_inanyorder(
            [('b', 2), ('c', 1)], [('b', 1), ('c', 2)], [('a', 2), ('c', 1)],
            [('a', 1), ('c', 2)], [('a', 2), ('b', 1)], [('a', 1), ('b', 2)],
        ))

    def test_match_with_one_edge_should_succeed(self):
        first = Graph({(1, 2)})
        second = Graph({('a', 'b')})
        first_variants = replace_node_by_obj(match(first, second))
        assert_that(first_variants, contains_inanyorder([(1, 'a'), (2, 'b')]))
        second_variants = replace_node_by_obj(match(second, first))
        assert_that(second_variants, contains_inanyorder([('a', 1), ('b', 2)]))

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
        assert_that(variants, empty())

    def test_match_with_many_components_and_special_equiv_should_succeed(self):
        class Node(object):
            def __init__(self, value, equiv=None):
                self.value = value
                self.equiv = equiv or frozenset()

            def equiv_pattern(self, other):
                return other.value in self.equiv

            def __repr__(self):
                return repr(self.value)

            def __eq__(self, other):
                return (id(self) == id(other)
                        or (self.value == other.value if hasattr(other, 'value')
                            else self.value == other))

        first = Graph({(Node(1, {'a'}), Node(2, {'b'})), (Node(3), Node(4))})
        second = Graph({(Node('a', {1}), Node('b', {2})), Node('c'), Node('d')})
        first_variants = replace_node_by_obj(match(first, second))
        assert_that(len(first_variants), equal_to(1))
        assert_that(first_variants[0], contains_inanyorder((1, 'a'), (2, 'b')))
        second_variants = replace_node_by_obj(match(second, first))
        assert_that(len(second_variants), equal_to(1))
        assert_that(second_variants[0], contains_inanyorder(('a', 1), ('b', 2)))
