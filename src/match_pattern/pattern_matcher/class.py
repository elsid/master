# coding: utf-8

import yaml
from pattern_matcher.classifier import Classifier
from utils import cached_eq


class Class(Classifier):
    @cached_eq
    def __eq__(self, other):
        return (id(self) == id(other)
                or super(Class, self).__eq__(other)
                and isinstance(other, Class))

    def __str__(self):
        return 'class %s' % self.name


yaml.add_representer(Class, Class.yaml_representer)
yaml.add_constructor('!Class', Class.yaml_constructor)
