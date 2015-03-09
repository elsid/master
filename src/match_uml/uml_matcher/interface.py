# coding: utf-8

from uml_matcher.classifier import Classifier


class Interface(Classifier):
    def __eq__(self, other):
        return (id(self) == id(other)
                or super(Interface, self).__eq__(other)
                and isinstance(other, Interface))
