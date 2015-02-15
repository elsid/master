#coding: utf-8

from uml_matcher.named_element import NamedElement
from uml_matcher.has_equivalents import has_equivalents

class Classifier(NamedElement):
    def __init__(self, name='anonymous', properties=tuple(),
            operations=tuple()):
        self.name = name
        self.properties = properties
        self.operations = operations
        for property in self.properties:
            property.owner = self

    def equivalent_pattern(self, pattern):
        return (has_equivalents(self.properties, pattern.properties)
            and has_equivalents(self.operations, pattern.operations))

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        if other is None or not isinstance(other, type(self)):
            return False
        return (self.properties == other.properties
            and self.operations == other.operations)

    def __hash__(self):
        return id(self)
