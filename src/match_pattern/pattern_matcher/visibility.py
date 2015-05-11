# coding: utf-8

import yaml
from enum import Enum


class Visibility(Enum):
    PUBLIC = 'public'
    PROTECTED = 'protected'
    PRIVATE = 'private'

    def __str__(self):
        if self == Visibility.PUBLIC:
            return '+'
        elif self == Visibility.PROTECTED:
            return '#'
        elif self == Visibility.PRIVATE:
            return '-'

    @staticmethod
    def yaml_representer(dumper, value):
        return dumper.represent_scalar(u'!Visibility', unicode(value.value))

    @staticmethod
    def yaml_constructor(loader, node):
        return Visibility(loader.construct_scalar(node).lower())


yaml.add_representer(Visibility, Visibility.yaml_representer)
yaml.add_constructor('!Visibility', Visibility.yaml_constructor)
