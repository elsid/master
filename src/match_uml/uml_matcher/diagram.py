#coding: utf-8

from collections import namedtuple
from graph_matcher import Graph

MatchResult = namedtuple('MatchResult', (
    'generalizations',
    'associations',
    'dependencies',
    'subsitutions',
    'usages',
))

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
        return MatchResult(
            Graph(self.generalizations).match(Graph(pattern.generalizations)),
            Graph(self.associations).match(Graph(pattern.associations)),
            Graph(self.dependencies).match(Graph(pattern.dependencies)),
            Graph(self.subsitutions).match(Graph(pattern.subsitutions)),
            Graph(self.usages).match(Graph(pattern.usages))
        )

    def __repr__(self):
        return ('\n' 'generatlizations' '\n' '%s' % Graph(self.generalizations)
            + '\n' 'associations' '\n' '%s' % Graph(self.associations))
