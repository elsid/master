# coding: utf-8

from uml_matcher.named_element import NamedElement
from uml_matcher.direction import Direction


class Parameter(NamedElement):
    def __init__(self, type, name='anonymous', direction=Direction.in_):
        super(Parameter, self).__init__(name)
        self.type = type
        self.direction = direction

    def sub_equiv_pattern(self, pattern):
        return ((self.type is None or pattern.type is not None
                 and self.type.sub_equiv_pattern(pattern.type))
                and self.direction == pattern.direction)

    def __eq__(self, other):
        return (id(self) == id(other)
                or super(Parameter, self).__eq__(other)
                and isinstance(other, Parameter)
                and self.type == other.type
                and self.direction == other.direction)
