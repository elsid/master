# coding: utf-8

from graph_matcher.node import Node
from graph_matcher.match import match


class Graph(object):
    def __init__(self, nodes_or_edges=tuple()):
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

        def make_edge(src, dst):
            src = get_node(src)
            dst = get_node(dst)
            if src == dst:
                src.self_connection = True
            else:
                src.connected_to.add(dst)
                dst.connected_from.add(src)

        self.nodes = set()

        for node_or_edge in nodes_or_edges:
            edge = node_or_edge
            if ((isinstance(edge, tuple) or isinstance(edge, set))
                    and len(edge) == 2):
                src, dst = edge
                if isinstance(edge, set):
                    make_edge(dst, src)
                make_edge(src, dst)
            else:
                self.nodes.add(get_node(node_or_edge))

        self.nodes |= set(nodes_dict.values())

    def match(self, pattern, limit=None):
        return match(self, pattern, limit)

    def __repr__(self):
        return '\n'.join(repr(node) for node in sorted(self.nodes))
