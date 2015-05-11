# coding: utf-8

import yaml
from graph_matcher import cached_eq
from pattern_matcher.classifier import Classifier


class Interface(Classifier):
    @cached_eq
    def __eq__(self, other):
        return (id(self) == id(other)
                or super(Interface, self).__eq__(other)
                and isinstance(other, Interface))

    def __str__(self):
        return 'interface %s' % self.name

    @staticmethod
    def yaml_constructor(loader, node):
        result = Interface()
        yield result
        result.update(**loader.construct_mapping(node, True))


yaml.add_representer(Interface, Interface.yaml_representer)
yaml.add_constructor('!Interface', Interface.yaml_constructor)
