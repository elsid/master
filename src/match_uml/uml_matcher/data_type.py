# coding: utf-8

import yaml
from graph_matcher import cached_eq
from uml_matcher.classifier import Classifier


class DataType(Classifier):
    @cached_eq
    def __eq__(self, other):
        return (id(self) == id(other)
                or super(DataType, self).__eq__(other)
                and isinstance(other, DataType))

    def __str__(self):
        return 'data type %s' % self.name

    @staticmethod
    def yaml_constructor(loader, node):
        result = DataType()
        yield result
        result.update(**loader.construct_mapping(node, True))


yaml.add_representer(DataType, DataType.yaml_representer)
yaml.add_constructor('!DataType', DataType.yaml_constructor)
