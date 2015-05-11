# coding: utf-8

import yaml
from graph_matcher import cached_eq
from pattern_matcher.classifier import Classifier


class Enumeration(Classifier):
    @cached_eq
    def __eq__(self, other):
        return (id(self) == id(other)
                or super(Enumeration, self).__eq__(other)
                and isinstance(other, Enumeration))

    def __str__(self):
        return 'enumeration %s' % self.name

    @staticmethod
    def yaml_constructor(loader, node):
        result = Enumeration()
        yield result
        result.update(**loader.construct_mapping(node, True))


yaml.add_representer(Enumeration, Enumeration.yaml_representer)
yaml.add_constructor('!Enumeration', Enumeration.yaml_constructor)
