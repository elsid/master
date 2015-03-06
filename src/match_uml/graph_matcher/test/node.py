#!/usr/bin/env python
# coding: utf-8

from unittest import TestCase
from hamcrest import assert_that, equal_to
from graph_matcher.node import Node


class MakeNode(TestCase):
    def test_make_single_should_succeed(self):
        node = Node('node')
        assert_that(node.obj, equal_to('node'))
        assert_that(node.connected_to, equal_to(set()))
        assert_that(node.connected_from, equal_to(set()))
        assert_that(node.self_connection, equal_to(False))
        assert_that(node.neighbors(), equal_to(set()))
        assert_that(node.count_connected_from(), equal_to(0))
        assert_that(node.count_connected_to(), equal_to(0))
        assert_that(node.equivalent_pattern(node), equal_to(True))
        assert_that(repr(node), equal_to('[node]'))
        assert_that(str(node), equal_to(str('node')))
        assert_that(hash(node), equal_to(id('node')))
        assert_that(node < node, equal_to(False))

    def test_make_with_connected_to_should_succeed(self):
        nodes_count = 3
        other_objs = ['node_%d' % n for n in range(nodes_count)]
        other_nodes = [Node(obj) for obj in other_objs]
        node = Node('node', connected_to=other_nodes)
        assert_that(node.connected_to, equal_to(set(other_nodes)))
        assert_that(node.connected_from, equal_to(set()))
        assert_that(node.self_connection, equal_to(False))
        assert_that(node.neighbors(), equal_to(set(other_nodes)))
        assert_that(node.count_connected_to(), equal_to(len(other_nodes)))
        assert_that(node.count_connected_from(), equal_to(0))
        assert_that(node.equivalent_pattern(node), equal_to(True))
        assert_that(repr(node), equal_to('[node] -> node_0, node_1, node_2'))

    def test_make_with_connected_from_should_succeed(self):
        nodes_count = 3
        other_objs = ['node_%d' % n for n in range(nodes_count)]
        other_nodes = [Node(obj) for obj in other_objs]
        node = Node('node', connected_from=other_nodes)
        assert_that(node.connected_to, equal_to(set()))
        assert_that(node.connected_from, equal_to(set(other_nodes)))
        assert_that(node.self_connection, equal_to(False))
        assert_that(node.neighbors(), equal_to(set(other_nodes)))
        assert_that(node.count_connected_to(), equal_to(0))
        assert_that(node.count_connected_from(), equal_to(len(other_nodes)))
        assert_that(node.equivalent_pattern(node), equal_to(True))
        assert_that(repr(node), equal_to('node_0, node_1, node_2 -> [node]'))

    def test_make_with_connected_should_succeed(self):
        nodes_count = 3
        other_objs = ['node_%d' % n for n in range(nodes_count)]
        other_nodes = [Node(obj) for obj in other_objs]
        node = Node('node', connected_to=other_nodes,
                    connected_from=other_nodes)
        assert_that(node.connected_to, equal_to(set(other_nodes)))
        assert_that(node.connected_from, equal_to(set(other_nodes)))
        assert_that(node.self_connection, equal_to(False))
        assert_that(node.neighbors(), equal_to(set(other_nodes)))
        assert_that(node.count_connected_to(), equal_to(len(other_nodes)))
        assert_that(node.count_connected_from(), equal_to(len(other_nodes)))
        assert_that(node.equivalent_pattern(node), equal_to(True))
        assert_that(repr(node), equal_to('node_0, node_1, node_2 -> [node]'
                                         ' -> node_0, node_1, node_2'))
