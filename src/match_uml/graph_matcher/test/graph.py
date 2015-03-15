# coding: utf-8

from unittest import TestCase
from hamcrest import assert_that, equal_to, empty, contains_inanyorder
from graph_matcher.graph import Graph


def replace_node_by_obj(nodes):
    return set(n.obj for n in nodes)


class MakeGraph(TestCase):
    def test_make_empty_should_succeed(self):
        graph = Graph()
        assert_that(graph.nodes, equal_to(set()))
        assert_that(repr(graph), equal_to(''))

    def test_make_with_one_node_should_succeed(self):
        graph = Graph({1})
        assert_that(replace_node_by_obj(graph.nodes), equal_to({1}))
        assert_that(repr(graph), equal_to('[1]'))

    def test_make_with_one_edge_should_succeed(self):
        graph = Graph({(1, 2)})
        assert_that(replace_node_by_obj(graph.nodes), equal_to({1, 2}))
        assert_that(repr(graph), equal_to(      '[1] -> 2' '\n'
                                           '1 -> [2]'))

    def test_make_self_connected_node_should_succeed(self):
        graph = Graph({(1, 1)})
        assert_that(replace_node_by_obj(graph.nodes), equal_to({1}))
        assert_that(repr(graph), equal_to('[1*]'))

    def test_make_complex_should_succeed(self):
        graph = Graph({(1, 2), (2, 4), (3, 2), (4, 3)})
        assert_that(replace_node_by_obj(graph.nodes), equal_to({1, 2, 3, 4}))
        assert_that(repr(graph), equal_to(        '[1] -> 2' '\n'
                                          '1, 3 -> [2] -> 4' '\n'
                                             '4 -> [3] -> 2' '\n'
                                             '2 -> [4] -> 3'))


def get_connected_components(graph):
    return [replace_node_by_obj(x) for x in graph.get_connected_components()]


class GraphGetConnectedComponents(TestCase):
    def test_empty_should_succeed(self):
        assert_that(get_connected_components(Graph()), empty())

    def test_two_not_connected_should_succeed(self):
        assert_that(get_connected_components(Graph({1, 2})),
                    contains_inanyorder({1}, {2}))

    def test_two_connected_should_succeed(self):
        assert_that(get_connected_components(Graph([(1, 2)])),
                    equal_to([{1, 2}]))

    def test_two_double_connected_should_succeed(self):
        assert_that(get_connected_components(Graph([{1, 2}])),
                    equal_to([{1, 2}]))

    def test_three_connected_should_succeed(self):
        assert_that(get_connected_components(Graph({(1, 2), (2, 3)})),
                    equal_to([{1, 2, 3}]))

    def test_two_components_should_succeed(self):
        assert_that(get_connected_components(Graph({(1, 2), (3, 4)})),
                    contains_inanyorder({1, 2}, {3, 4}))