# coding: utf-8

from unittest import TestCase, main
from hamcrest import assert_that, equal_to, empty
from graph_matcher.graph import Graph
from graph_matcher.test.arc_types import Red, Blue


def replace_node_by_obj(nodes):
    return set(n.obj for n in nodes)


class MakeGraph(TestCase):
    def test_make_empty_should_succeed(self):
        graph = Graph()
        assert_that(graph.nodes, equal_to(tuple()))
        assert_that(repr(graph), equal_to(''))
        assert_that(graph.connections_types(), equal_to(frozenset()))

    def test_make_with_one_node_should_succeed(self):
        graph = Graph({1})
        assert_that(replace_node_by_obj(graph.nodes), equal_to({1}))
        assert_that(repr(graph), equal_to('[1]'))
        assert_that(graph.connections_types(), equal_to(frozenset()))

    def test_make_with_one_arc_should_succeed(self):
        graph = Graph({(1, 2)})
        assert_that(replace_node_by_obj(graph.nodes), equal_to({1, 2}))
        assert_that(repr(graph), equal_to('[1] ---> 2'))
        assert_that(graph.connections_types(), equal_to({tuple}))

    def test_make_with_one_labeled_arc_should_succeed(self):
        graph = Graph({Red(1, 2)})
        assert_that(replace_node_by_obj(graph.nodes), equal_to({1, 2}))
        assert_that(repr(graph), equal_to('[1] -Red-> 2'))

    def test_make_self_connected_node_should_succeed(self):
        graph = Graph({(1, 1)})
        assert_that(replace_node_by_obj(graph.nodes), equal_to({1}))
        assert_that(repr(graph), equal_to('[1] *'))
        assert_that(graph.connections_types(), equal_to({tuple}))

    def test_make_self_connected_by_labeled_arc_node_should_succeed(self):
        graph = Graph({Red(1, 1)})
        assert_that(replace_node_by_obj(graph.nodes), equal_to({1}))
        assert_that(repr(graph), equal_to('[1] * Red'))
        assert_that(graph.connections_types(), equal_to({Red}))

    def test_make_one_node_and_one_arc_should_succeed(self):
        graph = Graph({1, (2, 3)})
        assert_that(replace_node_by_obj(graph.nodes), equal_to({1, 2, 3}))
        assert_that(repr(graph), equal_to('[1]' '\n'
                                          '[2] ---> 3'))

    def test_make_one_node_and_one_labeled_arc_should_succeed(self):
        graph = Graph({1, Red(2, 3)})
        assert_that(replace_node_by_obj(graph.nodes), equal_to({1, 2, 3}))
        assert_that(repr(graph), equal_to('[1]' '\n'
                                          '[2] -Red-> 3'))
        assert_that(graph.connections_types(), equal_to({Red}))

    def test_make_one_node_and_one_arc_with_duplication_should_succeed(self):
        graph = Graph({1, (1, 2)})
        assert_that(replace_node_by_obj(graph.nodes), equal_to({1, 2}))
        assert_that(repr(graph), equal_to('[1] ---> 2'))
        assert_that(graph.connections_types(), equal_to({tuple}))

    def test_make_complex_should_succeed(self):
        graph = Graph([Red(1, 2), (1, 2), Blue(2, 4), Blue(3, 2), (4, 3)])
        assert_that(replace_node_by_obj(graph.nodes), equal_to({1, 2, 3, 4}))
        assert_that(repr(graph), equal_to('[1] ---> 2'    '\n'
                                          '[1] -Red-> 2'  '\n'
                                          '[2] -Blue-> 4' '\n'
                                          '[3] -Blue-> 2' '\n'
                                          '[4] ---> 3'))
        assert_that(graph.connections_types(), equal_to({tuple, Red, Blue}))


def get_connected_components(graph):
    return [replace_node_by_obj(x) for x in graph.get_connected_components()]


class GraphGetConnectedComponents(TestCase):
    def test_empty_should_succeed(self):
        assert_that(get_connected_components(Graph()), empty())

    def test_two_not_connected_should_succeed(self):
        assert_that(get_connected_components(Graph({1, 2})),
                    equal_to([{1}, {2}]))

    def test_two_connected_should_succeed(self):
        assert_that(get_connected_components(Graph([(1, 2)])),
                    equal_to([{1, 2}]))

    def test_two_labeled_connected_should_succeed(self):
        assert_that(get_connected_components(Graph([Red(1, 2)])),
                    equal_to([{1, 2}]))

    def test_two_twice_labeled_connected_should_succeed(self):
        assert_that(get_connected_components(Graph([Red(1, 2), Blue(1, 2)])),
                    equal_to([{1, 2}]))

    def test_two_double_connected_should_succeed(self):
        assert_that(get_connected_components(Graph([{1, 2}])),
                    equal_to([{1, 2}]))

    def test_three_connected_should_succeed(self):
        assert_that(get_connected_components(Graph({(1, 2), (2, 3)})),
                    equal_to([{1, 2, 3}]))

    def test_two_components_should_succeed(self):
        assert_that(get_connected_components(Graph({(1, 2), (3, 4)})),
                    equal_to([{1, 2}, {3, 4}]))


if __name__ == '__main__':
    main()
