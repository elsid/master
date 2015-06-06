# coding: utf-8

import yaml
from pattern_matcher.match import match, eq_ignore_order, make_graph
from pattern_matcher.classifier import Classifier


class Model(object):
    def __init__(self, classifiers=None):
        classifiers = tuple(classifiers) if classifiers else tuple()
        for classifier in classifiers:
            assert isinstance(classifier, Classifier)
        self.classifiers = classifiers

    def match(self, pattern, limit=None):
        return match(self, pattern, limit)

    def graph(self):
        return make_graph(self)

    def __eq__(self, other):
        return (id(self) == id(other)
                or isinstance(other, Model)
                and eq_ignore_order(self.classifiers, other.classifiers))

    def __str__(self):

        def generate():
            for classifier in self.classifiers:
                yield str(classifier)

        return '\n'.join(generate())

    def __repr__(self):
        return 'Model(%s)' % (repr(self.classifiers)
                              if self.classifiers else '')

    @staticmethod
    def yaml_representer(dumper, value):
        return dumper.represent_sequence('!Model', value.classifiers)

    @staticmethod
    def yaml_constructor(loader, node):
        return Model(loader.construct_sequence(node))


yaml.add_representer(Model, Model.yaml_representer)
yaml.add_constructor('!Model', Model.yaml_constructor)
