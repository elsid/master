# coding: utf-8

from collections import namedtuple
from uml_matcher.match import match, eq_ignore_order, make_graph


class Generalization(namedtuple('Generalization', ('derived', 'general'))):
    def __repr__(self):
        return '%s ----> %s' % (self.derived, self.general)


class BinaryAssociation(frozenset):
    def __init__(self, ends):
        assert len(ends) == 2
        super(BinaryAssociation, self).__init__(ends)

    def __eq__(self, other):
        return (id(self) == id(other)
                or isinstance(other, BinaryAssociation)
                and eq_ignore_order(self, other))

    def __repr__(self):
        return '%s ----- %s' % tuple(self)


class Dependency(namedtuple('Dependency', ('client', 'supplier'))):
    def __repr__(self):
        return '%s - - > %s' % (self.client, self.supplier)


class Diagram(object):
    def __init__(self,
                 generalizations=tuple(),
                 associations=tuple(),
                 dependencies=tuple()):
        self.generalizations = generalizations
        self.associations = associations
        self.dependencies = dependencies

    def match(self, pattern, limit=None):
        return match(self, pattern, limit)

    def graph(self):
        return make_graph(self)

    def __eq__(self, other):
        return (id(self) == id(other)
                or isinstance(other, Diagram)
                and eq_ignore_order(self.generalizations, other.generalizations)
                and eq_ignore_order(self.associations, other.associations)
                and eq_ignore_order(self.dependencies, other.dependencies))

    def __repr__(self):
        connections = (
            ('generalizations', self.generalizations),
            ('associations', self.associations),
            ('dependencies', self.dependencies),
        )
        return ('\n'.join('%s\n%s' % (n, '\n'.join(
            '  %s' % repr(x) for x in v)) for n, v in connections if v))
