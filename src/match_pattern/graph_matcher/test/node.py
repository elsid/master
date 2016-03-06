#!/usr/bin/env python
# coding: utf-8

from unittest import TestCase, main
from hamcrest import assert_that, equal_to
from graph_matcher.node import Node
from graph_matcher.graph import Graph


class MakeNode(TestCase):
    def test_make_single_should_succeed(self):
        node = Node('node')
        assert_that(node.obj, equal_to('node'))
        assert_that(node.connections, equal_to(dict()))
        assert_that(node.self_connections, equal_to(set()))
        assert_that(node.neighbors, equal_to(set()))
        assert_that(node.equiv_pattern(node))
        assert_that(repr(node), equal_to('[node]'))
        assert_that(str(node), equal_to(str('node')))
        assert_that(hash(node), equal_to(hash('node')))
        assert_that(not node < node)
        assert_that(node.connections_types, equal_to(frozenset()))


class NodeGetConnectedComponent(TestCase):
    def test_empty_should_succeed(self):
        node = Node(1)
        assert_that(node.connected_component, {node})

    def test_two_not_connected_should_succeed(self):
        graph = Graph({1, 2})
        for node in graph.nodes:
            assert_that(node.connected_component, {node})

    def test_two_connected_should_succeed(self):
        graph = Graph({(1, 2)})
        for node in graph.nodes:
            assert_that(node.connected_component, graph.nodes)

    def test_two_double_connected_should_succeed(self):
        graph = Graph(({1, 2},))
        for node in graph.nodes:
            assert_that(node.connected_component, graph.nodes)

    def test_three_connected_should_succeed(self):
        graph = Graph({(1, 2), (2, 3)})
        for node in graph.nodes:
            assert_that(node.connected_component, graph.nodes)

    def test_two_components_should_succeed(self):
        graph = Graph({(1, 2), (3, 4)})
        nodes = {node.obj: node for node in graph.nodes}
        assert_that(nodes[1].connected_component, {nodes[1], nodes[2]})
        assert_that(nodes[2].connected_component, {nodes[1], nodes[2]})
        assert_that(nodes[3].connected_component, {nodes[3], nodes[4]})
        assert_that(nodes[4].connected_component, {nodes[3], nodes[4]})
