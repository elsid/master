# coding: utf-8

import yaml
from graph_matcher import cached_eq
from pattern_matcher.named_element import NamedElement
from pattern_matcher.has_equivalents import has_equivalents
from pattern_matcher.match import eq_ignore_order


class Classifier(NamedElement):
    def __init__(self, name=None, properties=None,
                 operations=None, generals=None, suppliers=None):
        super(Classifier, self).__init__(name)
        self.__properties = list(properties) if properties else []
        self.__operations = list(operations) if operations else []
        self.generals = list(generals) if generals else []
        self.suppliers = list(suppliers) if suppliers else []
        for property_ in self.__properties:
            property_.owner = self
        for operation in self.__operations:
            operation.owner = self

    @property
    def properties(self):
        return self.__properties

    @properties.setter
    def properties(self, value):
        self.__properties = value
        for property_ in self.__properties:
            property_.owner = self

    @property
    def operations(self):
        return self.__operations

    @operations.setter
    def operations(self, value):
        self.__operations = value
        for operation in self.__operations:
            operation.owner = self

    def has_property(self, name):
        return name in set(property_.name for property_ in self.__properties)

    def has_operation(self, name):
        return name in set(operation.name for operation in self.__operations)

    @cached_eq
    def equiv_pattern(self, pattern):
        return (isinstance(pattern, Classifier)
                and has_equivalents(self.__properties, pattern.__properties)
                and has_equivalents(self.__operations, pattern.__operations))

    def __eq__(self, other):
        return (id(self) == id(other)
                or super(Classifier, self).__eq__(other)
                and isinstance(other, Classifier)
                and eq_ignore_order(self.__properties, other.__properties)
                and eq_ignore_order(self.__operations, other.__operations))

    def __str__(self):
        return 'classifier %s' % self.name

    def update(self, **kwargs):
        if 'name' in kwargs:
            self.name = kwargs['name']
        if 'properties' in kwargs:
            self.properties = kwargs['properties']
        if 'operations' in kwargs:
            self.operations = kwargs['operations']
        if 'generals' in kwargs:
            self.generals = kwargs['generals']
        if 'suppliers' in kwargs:
            self.suppliers = kwargs['suppliers']

    @staticmethod
    def yaml_representer(dumper, value):
        return Classifier._yaml_representer(
            dumper, value,
            properties=value.properties or None,
            operations=value.operations or None,
            generals=value.generals or None,
            suppliers=value.suppliers or None,
        )

    @staticmethod
    def yaml_constructor(loader, node):
        result = Classifier()
        yield result
        result.update(**loader.construct_mapping(node, True))


yaml.add_representer(Classifier, Classifier.yaml_representer)
yaml.add_constructor('!Classifier', Classifier.yaml_constructor)
