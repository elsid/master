# coding: utf-8

from graph_matcher.match import match
from graph_matcher.node import Node


def get_label(arc_type):
    return (tuple if arc_type in frozenset({tuple, set, frozenset})
            else arc_type)


def generate_nodes(nodes_and_arcs):
    nodes_dict = {}

    def get_node(node):
        if isinstance(node, Node):
            if node.obj in nodes_dict:
                return nodes_dict[node.obj]
            else:
                nodes_dict[node.obj] = node
            return node
        else:
            if node not in nodes_dict:
                nodes_dict[node] = Node(node)
            return nodes_dict[node]

    def make_arc(src_node, dst_node, arc_type):
        label = get_label(arc_type)
        src_node = get_node(src_node)
        dst_node = get_node(dst_node)
        if src_node == dst_node:
            src_node.self_connections.add(label)
        else:
            src_node.connections[label].outgoing.add(dst_node)
            dst_node.connections[label].incoming.add(src_node)

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
        self.__nodes = tuple(sorted(frozenset(nodes)
                             if nodes else generate_nodes(nodes_or_arcs)))

    @property
    def nodes(self):
        return self.__nodes

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
        return '\n'.join(sorted(repr(node) for node in self.nodes
                                if repr(node)))

    def largest_connected_component(self):
        return max(self.get_connected_components(), key=len)

    def least_connected_node(self):
        return min(self.nodes, key=Node.count_connections)

    def connections_types(self):
        return reduce(frozenset.union,
                      (x.connections_types() for x in self.nodes), frozenset())
