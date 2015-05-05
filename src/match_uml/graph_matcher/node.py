# coding: utf-8

from collections import deque, defaultdict
from graph_matcher.cached_eq import cached_eq


class Connections(object):
    def __init__(self, incoming=None, outgoing=None):
        self.incoming = incoming or set()
        self.outgoing = outgoing or set()


class Node(object):
    obj_equivalent_pattern = None

    def __init__(self, obj, connections=None):
        self.obj = obj
        self.connections = (defaultdict(Connections, {
            k: Connections(set(v.incoming).difference({self}),
                           set(v.outgoing).difference({self}))
            for k, v in connections.iteritems()})
            if connections else defaultdict(Connections))
        self.self_connections = ({k for k, v in connections.iteritems()
                                 if self in v.incoming and self in v.outgoing}
                                 if connections else set())
        if hasattr(self.obj, 'equiv_pattern'):
            self.obj_equivalent_pattern = self.obj.equiv_pattern

    def neighbors(self):

        def generate():
            for k, v in self.connections.iteritems():
                for node in v.incoming:
                    yield node
                for node in v.outgoing:
                    yield node

        return frozenset(generate())

    def count_incoming_connections(self, color):
        return (len(self.connections[color].incoming)
                if color in self.connections else 0)

    def count_outgoing_connections(self, color):
        return (len(self.connections[color].outgoing)
                if color in self.connections else 0)

    @cached_eq
    def equiv_pattern(self, pattern):

        def equiv_connections_count():
            connections_colors = pattern.connections.keys()

            def generate():
                for color in connections_colors:
                    yield (self.count_incoming_connections(color) >=
                           pattern.count_incoming_connections(color)
                           and self.count_outgoing_connections(color) >=
                           pattern.count_outgoing_connections(color))

            return sum(generate()) == len(connections_colors)

        return (isinstance(pattern, Node)
                and equiv_connections_count()
                and (self.obj_equivalent_pattern is None
                     or self.obj_equivalent_pattern(pattern.obj)))

    def get_connected_component(self):
        nodes = deque((self,))
        visited = set()
        while nodes:
            node = nodes.pop()
            visited.add(node)
            for neighbor in node.neighbors():
                if neighbor not in visited:
                    nodes.append(neighbor)
                    visited.add(neighbor)
        return visited

    def __repr__(self):

        def generate():
            if not self.connections and not self.self_connections:
                yield '[%s]' % self.obj
                return
            for k, v in self.connections.iteritems():
                if v.outgoing:
                    yield '[%s] -%s-> %s' % (
                        self.obj, k or '-',
                        ', '.join(str(n.obj) for n in v.outgoing))
            for c in self.self_connections:
                yield '[%s] *%s' % (self.obj, ' %s' % c if c else '')

        return '\n'.join(generate())

    def __str__(self):
        return str(self.obj)

    def __hash__(self):
        return hash(self.obj)

    def __lt__(self, other):
        return self.obj < other.obj
