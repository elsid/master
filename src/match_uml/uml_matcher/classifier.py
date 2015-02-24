# coding: utf-8

from uml_matcher.named_element import NamedElement
from uml_matcher.has_equivalents import has_equivalents


class Classifier(NamedElement):
    def __init__(self, name='anonymous', properties=None, operations=None):
        self.name = name
        self.properties = properties or []
        self.operations = operations or []
        for property_ in self.properties:
            property_.owner = self

    def has_property(self, name):
        return name in set(property_.name for property_ in self.properties)

    def has_operation(self, name):
        return name in set(operation.name for operation in self.operations)

    def equivalent_pattern(self, pattern):
        return (has_equivalents(self.properties, pattern.properties)
                and has_equivalents(self.operations, pattern.operations))

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        if other is None or not isinstance(other, type(self)):
            return False
        return (self.name == self.name
                and self.properties == other.properties
                and self.operations == other.operations)

    def __hash__(self):
        return id(self)
