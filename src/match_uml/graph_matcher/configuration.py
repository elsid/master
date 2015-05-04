# coding: utf-8

from copy import copy
from collections import namedtuple


Equivalent = namedtuple('Equivalent', ('target', 'pattern'))


class Configuration(object):
    def __init__(self, target_node, pattern_node):
        e = Equivalent(target_node, pattern_node)
        self.selected = [e]
        self.current = 0
        self.visited = {e}

    def target(self):
        return self.selected[self.current].target

    def pattern(self):
        return self.selected[self.current].pattern

    def visited_targets(self):
        return frozenset(target for target, _ in self.visited)

    def visited_patterns(self):
        return frozenset(pattern for _, pattern in self.visited)

    def copy(self):
        other = copy(self)
        other.selected = copy(self.selected)
        other.current = self.current
        other.visited = copy(self.visited)
        return other

    def extend(self, pairs):
        self.selected.extend(pairs)

    def filter(self, pairs):
        return list(set(pairs).difference(set(self.selected)))

    def step(self):
        visited_targets = self.visited_targets()
        visited_patterns = self.visited_patterns()
        while True:
            self.current += 1
            if self.current >= len(self.selected):
                return
            if (self.target() not in visited_targets
                    and self.pattern() not in visited_patterns):
                self.visited.add(Equivalent(self.target(), self.pattern()))
                return

    def at_end(self):
        return self.current == len(self.selected)

    def priority(self):
        result = len(self.selected) - self.current
        if not self.at_end():
            result += len(self.target().neighbors())
        return result

    def __str__(self):

        def generate():
            for i, e in enumerate(self.selected):
                if i == self.current:
                    yield '[%s === %s]' % e
                elif e in self.visited:
                    yield '{%s === %s}' % e
                elif i > self.current:
                    yield '%s === %s' % e
                else:
                    yield '(%s === %s)' % e

        return ', '.join(generate())

    def __eq__(self, other):
        return (id(self) == id(other)
                or isinstance(other, Configuration)
                and set(self.selected) == set(other.selected))
