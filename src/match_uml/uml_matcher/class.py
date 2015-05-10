# coding: utf-8

import yaml
from uml_matcher.classifier import Classifier
from graph_matcher import cached_eq


class Class(Classifier):
    @cached_eq
    def __eq__(self, other):
        return (id(self) == id(other)
                or super(Class, self).__eq__(other)
                and isinstance(other, Class))

    def __str__(self):
        return 'class %s' % self.name

    @staticmethod
    def yaml_constructor(loader, node):
        result = Class()
        yield result
        result.update(**loader.construct_mapping(node, True))


yaml.add_representer(Class, Class.yaml_representer)
yaml.add_constructor('!Class', Class.yaml_constructor)
