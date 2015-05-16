# coding: utf-8

from copy import copy
from collections import namedtuple
from enum import Enum


class Equivalent(namedtuple('Equivalent', ('target', 'pattern'))):
    def __str__(self):
        return '%s === %s' % (self.target, self.pattern)

    def __repr__(self):
        return 'Equivalent(%s, %s)' % (repr(self.target), repr(self.pattern))


class EndType(Enum):
    INCOMING = 'incoming'
    OUTGOING = 'outgoing'

    def __str__(self):
        return self.value


class Configuration(object):
    def __init__(self, target_node, pattern_node):
        e = Equivalent(target_node, pattern_node)
        self.selected = [e]
        self.visited = {e}
        self.__current_index = 0

    def current(self):
        return self.selected[self.__current_index]

    def target(self):
        return self.current().target

    def pattern(self):
        return self.current().pattern

    def visited_targets(self):
        return frozenset(x.target for x in self.visited)

    def visited_patterns(self):
        return frozenset(x.pattern for x in self.visited)

    def copy(self):
        other = copy(self)
        other.selected = copy(self.selected)
        other.visited = copy(self.visited)
        return other

    def extend(self, pairs):
        self.selected.extend(pairs)

    def filter(self, pairs):
        return list(frozenset(pairs) - frozenset(self.selected))

    def step(self):
        visited_targets = self.visited_targets()
        visited_patterns = self.visited_patterns()

        def is_current_unvisited():
            return (self.target() not in visited_targets
                    and self.pattern() not in visited_patterns)

        def is_current_valid():
            target, pattern = self.current()

            def connections(neighbor, visited):
                for color, connection in visited.connections.iteritems():
                    if neighbor in connection.incoming:
                        yield (color, EndType.INCOMING)
                    if neighbor in connection.outgoing:
                        yield (color, EndType.OUTGOING)

            def is_valid(e):
                return (frozenset(connections(pattern, e.pattern))
                        <= frozenset(connections(target, e.target)))

            for x in self.visited:
                if not is_valid(x):
                    return False
            return True

        while True:
            self.__current_index += 1
            if self.at_end():
                return
            if is_current_unvisited() and is_current_valid():
                self.visited.add(self.current())
                return

    def at_end(self):
        return self.__current_index >= len(self.selected)

    def __str__(self):

        def generate():
            for i, e in enumerate(self.selected):
                if i == self.__current_index:
                    yield '[%s === %s]' % e
                elif e in self.visited:
                    yield '{%s === %s}' % e
                elif i > self.__current_index:
                    yield '%s === %s' % e
                else:
                    yield '(%s === %s)' % e

        return ', '.join(generate())

    def __eq__(self, other):
        return (id(self) == id(other)
                or isinstance(other, Configuration)
                and frozenset(self.selected) == frozenset(other.selected))
