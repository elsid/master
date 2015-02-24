# coding: utf-8

from uml_matcher.named_element import NamedElement
from uml_matcher.direction import Direction


class Parameter(NamedElement):
    def __init__(self, type, name='anonymous', direction=Direction.in_):
        self.type = type
        self.name = name
        self.direction = direction

    def sub_equivalent_pattern(self, pattern):
        return ((self.type is None or pattern.type is not None
                 and self.type.sub_equivalent_pattern(pattern.type))
                and self.direction == pattern.direction)

    def __eq__(self, other):
        return (isinstance(other, type(self))
                and self.name == self.name
                and self.type == other.type
                and self.direction == other.direction)
