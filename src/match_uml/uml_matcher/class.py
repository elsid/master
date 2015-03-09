# coding: utf-8

from uml_matcher.classifier import Classifier


class Class(Classifier):
    def __eq__(self, other):
        return (id(self) == id(other)
                or super(Class, self).__eq__(other)
                and isinstance(other, Class))
