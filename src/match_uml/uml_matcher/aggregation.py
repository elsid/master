# coding: utf-8

import yaml
from enum import Enum


class Aggregation(Enum):
    none = 'none'
    shared = 'shared'
    composite = 'composite'

    def __str__(self):
        return self.value

    @staticmethod
    def yaml_representer(dumper, value):
        return dumper.represent_scalar(u'!Aggregation', unicode(value))

    @staticmethod
    def yaml_constructor(loader, node):
        value = loader.construct_scalar(node)
        return Aggregation(value)


yaml.add_representer(Aggregation, Aggregation.yaml_representer)
yaml.add_constructor('!Aggregation', Aggregation.yaml_constructor)
