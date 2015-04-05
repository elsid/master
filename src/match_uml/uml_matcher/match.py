# coding: utf-8

from graph_matcher import Graph


class MatchResult(object):
    def __init__(self, results=None,
                 generalizations=tuple(),
                 associations=tuple()):
        results = results or tuple()
        self.generalizations = (generalizations if generalizations
                                or len(results) <= 0 else results[0])
        self.associations = (associations if associations
                             or len(results) <= 1 else results[1])

    def __eq__(self, other):
        return (id(self) == id(other)
                or isinstance(other, MatchResult)
                and eq_ignore_order(self.generalizations, other.generalizations)
                and eq_ignore_order(self.associations, other.associations))

    def __repr__(self):
        connections = (
            ('generalizations', self.generalizations),
            ('associations', self.associations),
        )
        return ('\n'.join('%s\n%s' % (n, '\n'.join('%s\n' % '\n'.join(
            '  %s === %s' % tuple(y) for y in x) for x in v))
            for n, v in connections if v))


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


def match(target, pattern):
    return MatchResult([list(replace_node_by_obj(r)) for r in (
        Graph(target.generalizations).match(Graph(pattern.generalizations)),
        Graph(target.associations).match(Graph(pattern.associations)),
    )])


def replace_node_by_obj(variants):
    return ([tuple((p[0].obj, p[1].obj)) for p in v] for v in variants)
