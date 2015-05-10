# coding: utf-8

import yaml
from enum import Enum


class Direction(Enum):
    in_ = 'in'
    out = 'out'
    inout = 'inout'

    def __str__(self):
        return self.value

    @staticmethod
    def yaml_representer(dumper, value):
        return dumper.represent_scalar(u'!Direction', unicode(value))

    @staticmethod
    def yaml_constructor(loader, node):
        value = loader.construct_scalar(node)
        return Direction(value)


yaml.add_representer(Direction, Direction.yaml_representer)
yaml.add_constructor('!Direction', Direction.yaml_constructor)
