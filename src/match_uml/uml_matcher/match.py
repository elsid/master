# coding: utf-8

from collections import namedtuple
from graph_matcher import Graph, replace_node_by_obj


class MatchVariant(object):
    def __init__(self, equivalents=None):
        self.equivalents = (tuple(equivalents) if equivalents else tuple())

    def __eq__(self, other):
        return (id(self) == id(other)
                or isinstance(other, MatchVariant)
                and eq_ignore_order(self.equivalents, other.equivalents))

    def __repr__(self):
        return '\n'.join('%s === %s' % (x.target, x.pattern)
                         for x in self.equivalents)

    def __len__(self):
        return len(self.equivalents)

    def __contains__(self, item):
        return isinstance(item, tuple) and item in self.equivalents


class MatchResult(object):
    def __init__(self, variants=None):
        self.variants = tuple(variants) if variants else tuple()

    def __eq__(self, other):
        return (id(self) == id(other)
                or isinstance(other, MatchResult)
                and eq_ignore_order(self.variants, other.variants))

    def __repr__(self):
        return '\n'.join('%s\n' % repr(x) for x in self.variants)

    def __len__(self):
        return len(self.variants)

    def __contains__(self, item):
        return isinstance(item, MatchVariant) and item in self.variants


def eq_ignore_order(first, second):

    def is_list(value):
        return isinstance(value, list)

    used = set()
    if len(first) != len(second):
        return False
    for x in first:
        found_eq = False

        def can_be_used(i, y):
            return (i not in used and (is_list(y) and eq_ignore_order(x, y) or
                    not is_list(y) and x == y))

        for i, y in enumerate(second):
            if can_be_used(i, y):
                used.add(i)
                found_eq = True
                break
        if not found_eq:
            return False
    return True


Owns = namedtuple('Owns', ('classifier', 'property'))


def make_ownerships(associations):
    for association in associations:
        for end in association:
            if end.owner:
                yield Owns(end.owner, end)


def make_graph(diagram):
    return Graph(list(diagram.generalizations)
                 + list(diagram.dependencies)
                 + list(diagram.associations)
                 + list(make_ownerships(diagram.associations)))


def match(target, pattern):
    result = make_graph(target).match(make_graph(pattern))
    return MatchResult([MatchVariant(x) for x in replace_node_by_obj(result)])
