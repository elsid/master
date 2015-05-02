# coding: utf-8

from graph_matcher.match import match
from graph_matcher.node import Node


def get_color(arc_type):
    return (None if arc_type in frozenset({tuple, set, frozenset})
            else arc_type.__name__)


def generate_nodes(nodes_and_arcs):
    nodes_dict = {}

    def get_node(node):
        if isinstance(node, Node):
            nodes_dict[id(node)] = node
            return node
        elif isinstance(node, (str, int, float)):
            if node not in nodes_dict:
                nodes_dict[node] = Node(node)
            return nodes_dict[node]
        else:
            if id(node) not in nodes_dict:
                nodes_dict[id(node)] = Node(node)
            return nodes_dict[id(node)]

    def make_arc(src_node, dst_node, arc_type):
        color = get_color(arc_type)
        src_node = get_node(src_node)
        dst_node = get_node(dst_node)
        if src_node == dst_node:
            src_node.self_connections.add(color)
        else:
            src_node.connections[color].outgoing.add(dst_node)
            dst_node.connections[color].incoming.add(src_node)

    nodes = set()
    for node_or_arc in nodes_and_arcs:
        arc = node_or_arc
        if isinstance(arc, (tuple, set, frozenset)) and len(arc) == 2:
            src, dst = arc
            if isinstance(arc, (set, frozenset)):
                make_arc(dst, src, type(arc))
            make_arc(src, dst, type(arc))
        else:
            nodes.add(get_node(node_or_arc))
    nodes |= set(nodes_dict.values())
    return nodes


class Graph(object):
    def __init__(self, nodes_or_arcs=tuple(), nodes=None):
        self.nodes = nodes or generate_nodes(nodes_or_arcs)

    def match(self, pattern):
        return match(self, pattern)

    def get_connected_components(self):
        nodes_components = {}
        for node in self.nodes:
            if node not in nodes_components:
                component = node.get_connected_component()
                for component_node in component:
                    nodes_components[component_node] = component
                yield component

    def get_node_by_obj_attr_value(self, attr, value):
        for node in self.nodes:
            if hasattr(node.obj, attr) and getattr(node.obj, attr) == value:
                return node

    def __repr__(self):
        return '\n'.join(repr(node) for node in sorted(self.nodes)
                         if repr(node))
