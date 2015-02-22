#coding: utf-8

from unittest import TestCase, main
from hamcrest import assert_that, equal_to
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

if __name__ == '__main__':
    main()
