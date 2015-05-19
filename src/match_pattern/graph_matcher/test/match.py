#!/usr/bin/env python
# coding: utf-8

from types import GeneratorType
from unittest import TestCase, main
from itertools import permutations, combinations, izip, product
from hamcrest import assert_that, equal_to, empty, contains_inanyorder
from graph_matcher.match import Equivalent, match, replace_node_by_obj
from graph_matcher.graph import Graph


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

    def make_graph(mask):
        return Graph(frozenset(mask_filter(mask, arcs)))

    for target_mask in product({True, False}, repeat=len(arcs)):
        target = make_graph(target_mask)
        for pattern_mask in product({True, False}, repeat=len(arcs)):
            if Mask(pattern_mask) <= Mask(target_mask):
                pattern = make_graph(pattern_mask)
                for node in pattern.nodes:
                    node.obj = chr(ord('a') + int(node.obj) - 1)
                yield target, pattern


class Match(TestCase):
    def test_match_empty_should_succeed(self):
        assert_that(list(match(Graph(), Graph())), empty())

    def test_match_with_one_node_should_succeed(self):
        first = Graph({1})
        second = Graph({'a'})
        first_variants = to_list(replace_node_by_obj(match(first, second)))
        assert_that(first_variants, equal_to(
            [[Equivalent(target=1, pattern='a')]]))
        second_variants = to_list(replace_node_by_obj(match(second, first)))
        assert_that(second_variants, equal_to(
            [[Equivalent(target='a', pattern=1)]]))

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

    def test_match_different_graphs_should_succeed(self):
        first = Graph({(1, 2), (2, 3), (3, 4)})
        second = Graph({('a', 'b'), ('b', 'c'), ('c', 'a')})
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

    def test_check_current_equivalence_before_add_to_visited(self):
        target = Graph({
            ('FormattedCommandAlias', 'Command'),
            ('Command', 'Command::create'),
            ('FormattedCommandAlias', 'FormattedCommandAlias::create'),
            ('PluginCommand', 'PluginCommand::create'),
            ('Command::create', 'Type(CommandSender)'),
            ('FormattedCommandAlias::create', 'Type(CommandSender)'),
            ('PluginCommand::create', 'Type(CommandSender)'),
        })
        pattern = Graph({
            ('ConcreteFactory', 'AbstractFactory'),
            ('AbstractFactory', 'AbstractFactory::create'),
            ('ConcreteFactory', 'ConcreteFactory::create'),
            ('AbstractFactory::create', 'Type(AbstractProduct)'),
            ('ConcreteFactory::create', 'Type(AbstractProduct)'),
        })
        variants = to_list(replace_node_by_obj(match(target, pattern)))
        assert_that(variants, equal_to([[
            ('Command', 'AbstractFactory'),
            ('Command::create', 'AbstractFactory::create'),
            ('FormattedCommandAlias', 'ConcreteFactory'),
            ('FormattedCommandAlias::create', 'ConcreteFactory::create'),
            ('Type(CommandSender)', 'Type(AbstractProduct)'),
        ]]))

    def test_match_generated_graphs_should_succeed(self):
        for nodes_count in xrange(2, 5):
            for target, pattern in generate_graphs(nodes_count):
                if target.nodes and pattern.nodes:
                    target = Graph(nodes=target.largest_connected_component())
                    pattern = Graph(nodes=pattern.largest_connected_component())
                    for v in replace_node_by_obj(match(target, pattern)):
                        assert_that({x.pattern for x in v},
                                    equal_to({x.obj for x in pattern.nodes}))


if __name__ == '__main__':
    main()
