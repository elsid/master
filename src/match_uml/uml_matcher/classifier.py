# coding: utf-8

from graph_matcher import cached_eq
from uml_matcher.named_element import NamedElement
from uml_matcher.has_equivalents import has_equivalents
from uml_matcher.match import eq_ignore_order


class Classifier(NamedElement):
    def __init__(self, name='anonymous', properties=None,
                 operations=None, generals=None, suppliers=None):
        super(Classifier, self).__init__(name)
        self.properties = list(properties) if properties else []
        self.operations = list(operations) if operations else []
        self.generals = list(generals) if generals else []
        self.suppliers = list(suppliers) if suppliers else []
        for property_ in self.properties:
            property_.owner = self
        for operation in self.operations:
            operation.owner = self

    def has_property(self, name):
        return name in set(property_.name for property_ in self.properties)

    def has_operation(self, name):
        return name in set(operation.name for operation in self.operations)

    @cached_eq
    def equiv_pattern(self, pattern):
        return (isinstance(pattern, Classifier)
                and has_equivalents(self.properties, pattern.properties)
                and has_equivalents(self.operations, pattern.operations))

    def __eq__(self, other):
        return (id(self) == id(other)
                or super(Classifier, self).__eq__(other)
                and isinstance(other, Classifier)
                and eq_ignore_order(self.properties, other.properties)
                and eq_ignore_order(self.operations, other.operations))

    def __hash__(self):
        return id(self)
