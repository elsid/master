# coding: utf-8

from collections import deque
from graph_matcher.cached_eq import cached_eq


class Node(object):
    obj_equivalent_pattern = None

    def __init__(self, obj, connected_to=tuple(), connected_from=tuple()):
        self.obj = obj
        self.connected_to = set(connected_to).difference({self})
        self.connected_from = set(connected_from).difference({self})
        self.self_connection = self in connected_to and self in connected_from
        if hasattr(self.obj, 'equiv_pattern'):
            self.obj_equivalent_pattern = self.obj.equiv_pattern

    def neighbors(self):
        return self.connected_to.union(self.connected_from)

    def count_connected_from(self):
        return len(self.connected_from)

    def count_connected_to(self):
        return len(self.connected_to)

    @cached_eq
    def equiv_pattern(self, pattern):
        return (self.count_connected_from() >= pattern.count_connected_from()
                and self.count_connected_to() >= pattern.count_connected_to()
                and type(self) == type(pattern)
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
        left = ', '.join((str(n.obj) for n in self.connected_from))
        right = ', '.join((str(n.obj) for n in self.connected_to))
        result = '[%s%s]' % (self.obj, '*' if self.self_connection else '')
        if left:
            result = '{1} -> {0}'.format(result, left)
        if right:
            result = '{0} -> {1}'.format(result, right)
        return result

    def __str__(self):
        return str(self.obj)

    def __hash__(self):
        return id(self.obj)

    def __lt__(self, other):
        return self.obj < other.obj
