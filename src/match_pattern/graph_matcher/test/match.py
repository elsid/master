#!/usr/bin/env python
# coding: utf-8

from types import GeneratorType
from unittest import TestCase, main
from itertools import permutations, combinations, izip, product
from hamcrest import assert_that, equal_to, empty, contains_inanyorder
from graph_matcher.configuration import Isomorphic
from graph_matcher.match import match as original_match, replace_node_by_obj
from graph_matcher.graph import Graph
from graph_matcher.check import check
from graph_matcher.test.arc_types import Red, Blue


def to_list(value):
    if isinstance(value, GeneratorType):
        return [to_list(x) for x in value]
    else:
        return value


class Mask(object):
    def __init__(self, values):
        self.__values = values

    def __iter__(self):
        return iter(self.__values)

    def __le__(self, other):
        try:
            return next(False for a, b in izip(self, other) if a > b)
        except StopIteration:
            return True


def mask_filter(mask, values):
    return (x for x, present in izip(values, mask) if present)


def generate_graphs(nodes_count):
    nodes = range(1, nodes_count + 1)
    arcs = list(combinations(nodes, 2))

    def sym(x):
        return chr(ord('a') + int(x) - 1)

    def sym_iter(iterable):
        return type(iterable)(sym(x) for x in iterable)

    for target_mask in product({True, False}, repeat=len(arcs)):
        target = Graph(mask_filter(target_mask, arcs))
        for pattern_mask in product({True, False}, repeat=len(arcs)):
            if Mask(pattern_mask) <= Mask(target_mask):
                pattern = Graph(sym_iter(x)
                                for x in mask_filter(pattern_mask, arcs))
                yield target, pattern


def match(target, pattern):
    return (x for x in original_match(target, pattern) if check(x))


class Match(TestCase):
    def test_match_empty_should_succeed(self):
        assert_that(list(match(Graph(), Graph())), empty())

    def test_match_with_one_node_should_succeed(self):
        first = Graph({1})
        second = Graph({'a'})
        first_variants = to_list(replace_node_by_obj(match(first, second)))
        assert_that(first_variants, equal_to(
            [[Isomorphic(target=1, pattern='a')]]))
        second_variants = to_list(replace_node_by_obj(match(second, first)))
        assert_that(second_variants, equal_to(
            [[Isomorphic(target='a', pattern=1)]]))

    def test_match_with_one_and_with_two_components_should_succeed(self):
        first = Graph({1})
        second = Graph({'a', 'b'})
        first_variants = to_list(replace_node_by_obj(match(first, second)))
        assert_that(first_variants, equal_to([[(1, 'a')], [(1, 'b')]]))
        second_variants = to_list(replace_node_by_obj(match(second, first)))
        assert_that(second_variants, equal_to([[('a', 1)], [('b', 1)]]))

    def test_match_with_two_components_should_succeed(self):
        first = Graph({1, 2})
        second = Graph({'a', 'b'})
        first_variants = to_list(replace_node_by_obj(match(first, second)))
        assert_that(first_variants, equal_to([
            [(1, 'a'), (2, 'b')], [(1, 'b'), (2, 'a')]
        ]))
        second_variants = to_list(replace_node_by_obj(match(second, first)))
        assert_that(second_variants, equal_to([
            [('a', 1), ('b', 2)], [('a', 2), ('b', 1)]
        ]))

    def test_match_with_two_and_three_components_should_succeed(self):
        first = Graph({1, 2})
        second = Graph({'a', 'b', 'c'})
        first_variants = to_list(replace_node_by_obj(match(first, second)))
        assert_that(first_variants, equal_to([
            [(1, 'a'), (2, 'c')], [(1, 'c'), (2, 'a')], [(1, 'a'), (2, 'b')],
            [(1, 'b'), (2, 'a')], [(1, 'c'), (2, 'b')], [(1, 'b'), (2, 'c')],
        ]))
        second_variants = to_list(replace_node_by_obj(match(second, first)))
        assert_that(second_variants, equal_to([
            [('a', 1), ('c', 2)], [('a', 2), ('c', 1)], [('a', 1), ('b', 2)],
            [('a', 2), ('b', 1)], [('b', 2), ('c', 1)], [('b', 1), ('c', 2)],
        ]))

    def test_match_with_one_arc_should_succeed(self):
        first = Graph({(1, 2)})
        second = Graph({('a', 'b')})
        first_variants = to_list(replace_node_by_obj(match(first, second)))
        assert_that(first_variants, equal_to([[(1, 'a'), (2, 'b')]]))
        second_variants = to_list(replace_node_by_obj(match(second, first)))
        assert_that(second_variants, equal_to([[('a', 1), ('b', 2)]]))

    def test_match_with_self_connected_nodes_should_succeed(self):
        first = Graph({(1, 1)})
        second = Graph({('a', 'a')})
        first_variants = to_list(replace_node_by_obj(match(first, second)))
        assert_that(first_variants, equal_to([[(1, 'a')]]))
        second_variants = to_list(replace_node_by_obj(match(second, first)))
        assert_that(second_variants, equal_to([[('a', 1)]]))

    def test_match_complete_graphs_and_should_succeed(self):
        target_nodes = (1, 2, 3, 4)
        pattern_nodes = ('a', 'b', 'c', 'd')
        first = Graph((p[0], p[1]) for p in permutations(target_nodes))
        second = Graph((p[0], p[1]) for p in permutations(pattern_nodes))
        actual_variants = to_list(replace_node_by_obj(match(first, second)))

        def generate_expected_variants():
            for pattern in permutations(pattern_nodes, len(target_nodes)):
                yield zip(target_nodes, pattern)

        expected_variants = list(generate_expected_variants())
        assert_that(actual_variants, contains_inanyorder(*expected_variants))

    def test_match_different_graphs_should_be_empty_result(self):
        first = Graph({(1, 2), (2, 3)})
        second = Graph({('a', 'b'), ('b', 'a')})
        variants = to_list(replace_node_by_obj(match(first, second)))
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

            def __hash__(self):
                return hash(self.value)

            def __lt__(self, other):
                return hash(self) < hash(other)

        first = Graph({(Node(1, {'a'}), Node(2, {'b'})), (Node(3), Node(4))})
        second = Graph({(Node('a', {1}), Node('b', {2})), Node('c'), Node('d')})
        first_variants = to_list(replace_node_by_obj(match(first, second)))
        assert_that(len(first_variants), equal_to(1))
        assert_that(first_variants[0], equal_to([(1, 'a'), (2, 'b')]))
        second_variants = to_list(replace_node_by_obj(match(second, first)))
        assert_that(len(second_variants), equal_to(1))
        assert_that(second_variants[0], equal_to([('a', 1), ('b', 2)]))

    def test_check_current_isomorphism_before_add_to_visited(self):
        target = Graph({
            Red(1, 3),
            Red(1, 4),
            Red(2, 3),
            Blue(5, 4),
            Blue(6, 3),
            Blue(2, 4),
        })
        pattern = Graph({
            Red('a', 'b'),
            Red('a', 'c'),
            Blue('d', 'b'),
            Blue('e', 'c'),
        })
        variants = to_list(replace_node_by_obj(match(target, pattern)))
        assert_that(variants, equal_to([
            [(1, 'a'), (2, 'e'), (3, 'b'), (4, 'c'), (6, 'd')],
            [(1, 'a'), (3, 'b'), (4, 'c'), (5, 'e'), (6, 'd')],
            [(1, 'a'), (2, 'd'), (3, 'c'), (4, 'b'), (6, 'e')],
            [(1, 'a'), (3, 'c'), (4, 'b'), (5, 'd'), (6, 'e')],
        ]))
        # without is_current_valid() check
        # variants = to_list(replace_node_by_obj(original_match(target,
        #                                                       pattern)))
        # assert_that(variants, equal_to([
        #     [(1, 'a'), (2, 'e'), (3, 'c'), (4, 'b'), (5, 'd')],  # error
        #     [(1, 'a'), (2, 'e'), (3, 'b'), (4, 'c'), (6, 'd')],  # ok
        #     [(1, 'a'), (2, 'd'), (3, 'b'), (4, 'c'), (5, 'e')],  # error
        #     [(1, 'a'), (3, 'b'), (4, 'c'), (5, 'e'), (6, 'd')],  # ok
        #     [(1, 'a'), (2, 'd'), (3, 'c'), (4, 'b'), (6, 'e')],  # ok
        #     [(1, 'a'), (3, 'c'), (4, 'b'), (5, 'd'), (6, 'e')],  # ok
        # ]))

    def test_match_generated_graphs_should_succeed(self):
        for nodes_count in xrange(2, 5):
            for target, pattern in generate_graphs(nodes_count):
                if target.nodes and pattern.nodes:
                    t = Graph(nodes=target.largest_connected_component())
                    p = Graph(nodes=pattern.largest_connected_component())
                    for i in replace_node_by_obj(match(t, p)):
                        assert_that({x.pattern for x in i},
                                    equal_to({x.obj for x in p.nodes}))

    def test_match_chain_of_two_in_chain_of_three_should_succeed(self):
        target = Graph({(1, 2), (2, 3)})
        pattern = Graph({('a', 'b')})
        variants = to_list(replace_node_by_obj(match(target, pattern)))
        assert_that(variants, equal_to([
            [(1, 'a'), (2, 'b')],
            [(2, 'a'), (3, 'b')],
        ]))

    def test_match_two_components_in_one_should_succeed(self):
        target = Graph({(1, 2), (2, 3), (3, 4)})
        pattern = Graph({('a', 'b'), ('c', 'd')})
        variants = to_list(replace_node_by_obj(match(target, pattern)))
        assert_that(variants, equal_to([
            [(1, 'a'), (2, 'b')],
            [(2, 'a'), (3, 'b')],
            [(3, 'a'), (4, 'b')],
            [(1, 'c'), (2, 'd')],
            [(2, 'c'), (3, 'd')],
            [(3, 'c'), (4, 'd')],
        ]))
        # FIXME: must be
        # assert_that(variants, equal_to([
        #     [(1, 'a'), (2, 'b'), (3, 'c'), (4, 'd')],
        #     [(2, 'a'), (3, 'b')],
        #     [(1, 'c'), (2, 'd'), (3, 'a'), (4, 'b')],
        #     [(2, 'c'), (3, 'd')],
        # ]))

    def test_match_one_component_in_two_should_succeed(self):
        target = Graph({(1, 2), (3, 4)})
        pattern = Graph({('a', 'b')})
        variants = to_list(replace_node_by_obj(match(target, pattern)))
        assert_that(variants, equal_to([
            [(1, 'a'), (2, 'b')],
            [(3, 'a'), (4, 'b')],
        ]))

    def test_match_with_one_explicit_labeled_arc_should_succeed(self):
        first = Graph({Red(1, 2)})
        second = Graph({Red('a', 'b')})
        first_variants = to_list(replace_node_by_obj(match(first, second)))
        assert_that(first_variants, equal_to([[(1, 'a'), (2, 'b')]]))
        second_variants = to_list(replace_node_by_obj(match(second, first)))
        assert_that(second_variants, equal_to([[('a', 1), ('b', 2)]]))

    def test_match_with_one_different_labeled_arcs_should_be_empty_result(self):
        first = Graph({Red(1, 2)})
        second = Graph({Blue('a', 'b')})
        variants = to_list(replace_node_by_obj(match(first, second)))
        assert_that(variants, empty())


if __name__ == '__main__':
    main()
