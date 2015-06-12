# coding: utf-8

from collections import deque, defaultdict, namedtuple
from pydot import Node as DotNode
from graph_matcher.cached_eq import cached_eq


Arc = namedtuple('Arc', ('source', 'target', 'label'))


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

    @property
    def neighbors(self):

        def generate():
            for v in self.connections.itervalues():
                for node in v.incoming:
                    yield node
                for node in v.outgoing:
                    yield node

        return frozenset(generate())

    @property
    def connections_types(self):
        return (frozenset(self.self_connections)
                | frozenset(x for x in self.connections.iterkeys()))

    @property
    def connected_component(self):
        nodes = deque((self,))
        visited = set()
        while nodes:
            node = nodes.pop()
            if node not in visited:
                visited.add(node)
                for neighbor in node.neighbors:
                    if neighbor not in visited:
                        nodes.append(neighbor)
        return visited

    @property
    def outgoing_arcs(self):
        for label, connections in self.connections.iteritems():
            for target in sorted(connections.outgoing):
                yield Arc(self, target, label)

    def count_connections(self):
        return sum(len(x.incoming) + len(x.outgoing)
                   for x in self.connections.values())

    def count_incoming_connections(self, label):
        return (len(self.connections[label].incoming)
                if label in self.connections else 0)

    def count_outgoing_connections(self, label):
        return (len(self.connections[label].outgoing)
                if label in self.connections else 0)

    @cached_eq
    def equiv_pattern(self, pattern):

        def equiv_connections_count():
            connections_labels = pattern.connections.keys()

            def generate():
                for label in connections_labels:
                    yield (self.count_incoming_connections(label) >=
                           pattern.count_incoming_connections(label)
                           and self.count_outgoing_connections(label) >=
                           pattern.count_outgoing_connections(label))

            return sum(generate()) == len(connections_labels)

        return (isinstance(pattern, Node)
                and equiv_connections_count()
                and (self.obj_equivalent_pattern is None
                     or self.obj_equivalent_pattern(pattern.obj)))

    def as_dot(self):
        if hasattr(self.obj, 'full_name'):
            obj_label = '"<<%s>>\n%s"' % (type(self.obj).__name__,
                                          self.obj.full_name)
            return DotNode('"%s"' % str(self.obj), label=obj_label, shape='box')
        else:
            return DotNode('"%s"' % str(self.obj), shape='box')

    def __repr__(self):

        def generate():
            if not self.connections and not self.self_connections:
                yield '[%s]' % self.obj
                return
            for k, v in self.connections.iteritems():
                if v.outgoing:
                    yield '[%s] -%s-> %s' % (
                        self.obj, k.__name__ if k != tuple else '-',
                        ', '.join(str(n.obj) for n in v.outgoing))
            for c in self.self_connections:
                yield '[%s] *%s' % (self.obj, ' %s' % c.__name__
                                    if c != tuple else '')

        return '\n'.join(sorted(generate()))

    def __str__(self):
        return str(self.obj)

    def __hash__(self):
        return hash(self.obj)

    def __lt__(self, other):
        return self.obj < other.obj
