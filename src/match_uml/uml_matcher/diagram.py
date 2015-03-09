# coding: utf-8

from collections import namedtuple
from graph_matcher import Graph


def replace_node_by_obj(variants):
    return ([tuple((p[0].obj, p[1].obj)) for p in v] for v in variants)


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


class MatchResult(object):
    def __init__(self, results=None,
                 generalizations=tuple(),
                 associations=tuple(),
                 dependencies=tuple(),
                 substitutions=tuple(),
                 usages=tuple()):
        results = results or tuple()
        self.generalizations = (generalizations if generalizations
                                or len(results) <= 0 else results[0])
        self.associations = (associations if associations
                             or len(results) <= 1 else results[1])
        self.dependencies = (dependencies if dependencies
                             or len(results) <= 2 else results[2])
        self.substitutions = (substitutions if substitutions
                              or len(results) <= 3 else results[3])
        self.usages = (usages if usages or len(results) <= 4 else results[4])

    def __eq__(self, other):
        return (id(self) == id(other)
                or isinstance(other, type(self))
                and eq_ignore_order(self.generalizations, other.generalizations)
                and eq_ignore_order(self.associations, other.associations)
                and eq_ignore_order(self.dependencies, other.dependencies)
                and eq_ignore_order(self.substitutions, other.substitutions)
                and eq_ignore_order(self.usages, other.usages))

    def __repr__(self):
        connections = (
            ('generalizations', self.generalizations),
            ('associations', self.associations),
            ('dependencies', self.dependencies),
            ('substitutions', self.substitutions),
            ('usages', self.usages),
        )
        return ('\n'.join('%s\n%s' % (n, '\n'.join('%s\n' % '\n'.join(
            '  %s === %s' % tuple(y) for y in x) for x in v))
            for n, v in connections if v))


class Generalization(namedtuple('Generalization', ('derived', 'base'))):
    def __repr__(self):
        return '%s --> %s' % (self.derived, self.base)


class BinaryAssociation(frozenset):
    def __init__(self, ends):
        assert len(ends) == 2
        super(BinaryAssociation, self).__init__(ends)

    def __eq__(self, other):
        return (id(self) == id(other)
                or isinstance(other, type(self))
                and eq_ignore_order(self, other))

    def __repr__(self):
        return '%s --- %s' % tuple(self)


class Diagram(object):
    def __init__(self,
                 generalizations=tuple(),
                 associations=tuple(),
                 dependencies=tuple(),
                 substitutions=tuple(),
                 usages=tuple()):
        self.generalizations = generalizations
        self.associations = associations
        self.dependencies = dependencies
        self.substitutions = substitutions
        self.usages = usages

    def match(self, pattern):
        return MatchResult([list(replace_node_by_obj(r)) for r in (
            Graph(self.generalizations).match(Graph(pattern.generalizations)),
            Graph(self.associations).match(Graph(pattern.associations)),
            Graph(self.dependencies).match(Graph(pattern.dependencies)),
            Graph(self.substitutions).match(Graph(pattern.substitutions)),
            Graph(self.usages).match(Graph(pattern.usages))
        )])

    def __eq__(self, other):
        return (id(self) == id(other)
                or isinstance(other, type(self))
                and eq_ignore_order(self.generalizations, other.generalizations)
                and eq_ignore_order(self.associations, other.associations)
                and eq_ignore_order(self.dependencies, other.dependencies)
                and eq_ignore_order(self.substitutions, other.substitutions)
                and eq_ignore_order(self.usages, other.usages))

    def __repr__(self):
        connections = (
            ('generalizations', self.generalizations),
            ('associations', self.associations),
            ('dependencies', self.dependencies),
            ('substitutions', self.substitutions),
            ('usages', self.usages),
        )
        return ('\n'.join('%s\n%s' % (n, '\n'.join(
            '  %s' % repr(x) for x in v)) for n, v in connections if v))
