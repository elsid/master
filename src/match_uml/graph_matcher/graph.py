# coding: utf-8

from graph_matcher.node import Node
from graph_matcher.match import match


def generate_nodes(nodes_or_edges):
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

    def make_edge(src_node, dst_node):
        src_node = get_node(src_node)
        dst_node = get_node(dst_node)
        if src_node == dst_node:
            src_node.self_connection = True
        else:
            src_node.connected_to.add(dst_node)
            dst_node.connected_from.add(src_node)

    nodes = set()
    for node_or_edge in nodes_or_edges:
        edge = node_or_edge
        if isinstance(edge, (tuple, set, frozenset)) and len(edge) == 2:
            src, dst = edge
            if isinstance(edge, (set, frozenset)):
                make_edge(dst, src)
            make_edge(src, dst)
        else:
            nodes.add(get_node(node_or_edge))
    nodes |= set(nodes_dict.values())
    return nodes


class Graph(object):
    def __init__(self, nodes_or_edges=tuple(), nodes=None):
        self.nodes = nodes or generate_nodes(nodes_or_edges)

    def match(self, pattern, limit=None):
        return match(self, pattern, limit)

    def get_connected_components(self):
        nodes_components = {}
        for node in self.nodes:
            if node not in nodes_components:
                component = node.get_connected_component()
                for component_node in component:
                    nodes_components[component_node] = component
                yield component

    def __repr__(self):
        return '\n'.join(repr(node) for node in sorted(self.nodes))
