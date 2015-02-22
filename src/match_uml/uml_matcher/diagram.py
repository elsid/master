#coding: utf-8

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
        for i, y in enumerate(second):
            if (i not in used and (is_list(y) and eq_ignore_order(x, y)
                    or not is_list(y) and x == y)):
                used.add(i)
                found_eq = True
                break
        if not found_eq:
            return False
    return True

class MatchResult(object):
    def __init__(self, results=tuple(),
            generalizations=tuple(),
            associations=tuple(),
            dependencies=tuple(),
            subsitutions=tuple(),
            usages=tuple()):
        self.generalizations = (generalizations
            if generalizations or len(results) <= 0 else results[0])
        self.associations = (associations
            if associations or len(results) <= 1 else results[1])
        self.dependencies = (dependencies
            if dependencies or len(results) <= 2 else results[2])
        self.subsitutions = (subsitutions
            if subsitutions or len(results) <= 3 else results[3])
        self.usages = (usages if usages or len(results) <= 4 else results[4])

    def __eq__(self, other):
        return (eq_ignore_order(self.generalizations, other.generalizations)
            and eq_ignore_order(self.associations, other.associations)
            and eq_ignore_order(self.dependencies, other.dependencies)
            and eq_ignore_order(self.subsitutions, other.subsitutions)
            and eq_ignore_order(self.usages, other.usages))

    def __repr__(self):
        return '\n'.join(repr(r) for r in (
            self.generalizations,
            self.associations,
            self.dependencies,
            self.subsitutions,
            self.usages
        ))

Generalization = namedtuple('Generalization', ('derived', 'base'))

class Diagram(object):
    def __init__(self,
            generalizations=tuple(),
            associations=tuple(),
            dependencies=tuple(),
            subsitutions=tuple(),
            usages=tuple()):
        self.generalizations = generalizations
        self.associations = associations
        self.dependencies = dependencies
        self.subsitutions = subsitutions
        self.usages = usages

    def match(self, pattern):
        return MatchResult([list(replace_node_by_obj(r)) for r in (
            Graph(self.generalizations).match(Graph(pattern.generalizations)),
            Graph(self.associations).match(Graph(pattern.associations)),
            Graph(self.dependencies).match(Graph(pattern.dependencies)),
            Graph(self.subsitutions).match(Graph(pattern.subsitutions)),
            Graph(self.usages).match(Graph(pattern.usages))
        )])

    def __repr__(self):
        return ('\n' 'generatlizations' '\n' '%s' % Graph(self.generalizations)
            + '\n' 'associations' '\n' '%s' % Graph(self.associations))
