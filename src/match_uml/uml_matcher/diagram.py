# coding: utf-8

import yaml
from uml_matcher.match import match, eq_ignore_order, make_graph
from uml_matcher.classifier import Classifier


class Diagram(object):
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
                or isinstance(other, Diagram)
                and eq_ignore_order(self.classifiers, other.classifiers))

    def __str__(self):

        def generate():
            for classifier in self.classifiers:
                yield str(classifier)

        return '\n'.join(generate())

    def __repr__(self):
        return 'Diagram(%s)' % (repr(self.classifiers)
                                if self.classifiers else '')

    @staticmethod
    def yaml_representer(dumper, value):
        return dumper.represent_sequence('!Diagram', value.classifiers)

    @staticmethod
    def yaml_constructor(loader, node):
        return Diagram(loader.construct_sequence(node))


yaml.add_representer(Diagram, Diagram.yaml_representer)
yaml.add_constructor('!Diagram', Diagram.yaml_constructor)
