# coding: utf-8

import yaml
from enum import Enum


class Visibility(Enum):
    public = 'public'
    protected = 'protected'
    private = 'private'

    def __str__(self):
        if self == Visibility.public:
            return '+'
        elif self == Visibility.protected:
            return '#'
        elif self == Visibility.private:
            return '-'

    @staticmethod
    def yaml_representer(dumper, value):
        return dumper.represent_scalar(u'!Visibility', unicode(value.value))

    @staticmethod
    def yaml_constructor(loader, node):
        value = loader.construct_scalar(node)
        return Visibility(value)


yaml.add_representer(Visibility, Visibility.yaml_representer)
yaml.add_constructor('!Visibility', Visibility.yaml_constructor)
