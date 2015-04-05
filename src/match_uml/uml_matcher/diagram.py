# coding: utf-8

from collections import namedtuple
from uml_matcher.match import match, eq_ignore_order


class Generalization(namedtuple('Generalization', ('derived', 'base'))):
    def __repr__(self):
        return '%s --> %s' % (self.derived, self.base)


class BinaryAssociation(frozenset):
    def __init__(self, ends):
        assert len(ends) == 2
        super(BinaryAssociation, self).__init__(ends)

    def __eq__(self, other):
        return (id(self) == id(other)
                or isinstance(other, BinaryAssociation)
                and eq_ignore_order(self, other))

    def __repr__(self):
        return '%s --- %s' % tuple(self)


class Diagram(object):
    def __init__(self,
                 generalizations=tuple(),
                 associations=tuple()):
        self.generalizations = generalizations
        self.associations = associations

    def match(self, pattern):
        return match(self, pattern)

    def __eq__(self, other):
        return (id(self) == id(other)
                or isinstance(other, Diagram)
                and eq_ignore_order(self.generalizations, other.generalizations)
                and eq_ignore_order(self.associations, other.associations))

    def __repr__(self):
        connections = (
            ('generalizations', self.generalizations),
            ('associations', self.associations),
        )
        return ('\n'.join('%s\n%s' % (n, '\n'.join(
            '  %s' % repr(x) for x in v)) for n, v in connections if v))
