# coding: utf-8

import yaml
from utils import cached_eq
from pattern_matcher.classifier import Classifier


class Interface(Classifier):
    @cached_eq
    def __eq__(self, other):
        return (id(self) == id(other)
                or super(Interface, self).__eq__(other)
                and isinstance(other, Interface))

    def __str__(self):
        return 'interface %s' % self.name


yaml.add_representer(Interface, Interface.yaml_representer)
yaml.add_constructor('!Interface', Interface.yaml_constructor)
