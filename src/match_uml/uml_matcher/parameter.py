# coding: utf-8

from uml_matcher.named_element import NamedElement
from uml_matcher.direction import Direction
from uml_matcher.eq_pattern import eq_pattern, sub_equiv_pattern


class Parameter(NamedElement):
    def __init__(self, type, name='anonymous', direction=Direction.in_):
        super(Parameter, self).__init__(name)
        self.type = type
        self.direction = direction

    def sub_equiv_pattern(self, pattern):
        return (isinstance(pattern, Parameter)
                and (sub_equiv_pattern(self.type, pattern.type))
                and eq_pattern(self.direction, pattern.direction))

    def __eq__(self, other):
        return (id(self) == id(other)
                or super(Parameter, self).__eq__(other)
                and isinstance(other, Parameter)
                and self.type == other.type
                and self.direction == other.direction)

    def __repr__(self):
        return '{direction}{name}: {type}'.format(
            name=self.name,
            type=self.type,
            direction=self.direction)
