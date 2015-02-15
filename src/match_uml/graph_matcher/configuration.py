#coding: utf-8

from copy import copy

class Configuration(object):
    def __init__(self, target_node, pattern_node):
        self.selected = [(target_node, pattern_node)]
        self.current = 0
        self.visited = set(self.selected)

    def target(self):
        return self.selected[self.current][0]

    def pattern(self):
        return self.selected[self.current][1]

    def visited_targets(self):
        return set([target for target, _ in self.visited])

    def visited_patterns(self):
        return set([pattern for _, pattern in self.visited])

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
                self.visited.add((self.target(), self.pattern()))
                return

    def at_end(self):
        return self.current == len(self.selected)

    def priority(self):
        result = len(self.selected) - self.current
        if not self.at_end():
            result += len(self.target().neighbors())
        return result

    def __repr__(self):
        return ', '.join(('%s' if i != self.current else '[%s]') %
            str((str(p[0]), str(p[1]))) for (i, p) in enumerate(self.selected))

    def __eq__(self, other):
        return set(self.selected) == set(other.selected)
