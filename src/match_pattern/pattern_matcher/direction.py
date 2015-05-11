# coding: utf-8

import yaml
from enum import Enum


class Direction(Enum):
    IN = 'in'
    OUT = 'out'
    INOUT = 'inout'

    def __str__(self):
        return self.value

    @staticmethod
    def yaml_representer(dumper, value):
        return dumper.represent_scalar(u'!Direction', unicode(value))

    @staticmethod
    def yaml_constructor(loader, node):
        return Direction(loader.construct_scalar(node).lower())


yaml.add_representer(Direction, Direction.yaml_representer)
yaml.add_constructor('!Direction', Direction.yaml_constructor)
