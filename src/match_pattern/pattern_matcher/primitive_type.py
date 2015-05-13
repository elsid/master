# coding: utf-8

import yaml
from graph_matcher import cached_eq
from pattern_matcher.classifier import Classifier


class PrimitiveType(Classifier):
    @cached_eq
    def __eq__(self, other):
        return (id(self) == id(other)
                or super(PrimitiveType, self).__eq__(other)
                and isinstance(other, PrimitiveType))

    def __str__(self):
        return 'primitive type %s' % self.name


yaml.add_representer(PrimitiveType, PrimitiveType.yaml_representer)
yaml.add_constructor('!PrimitiveType', PrimitiveType.yaml_constructor)
