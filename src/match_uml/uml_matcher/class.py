# coding: utf-8

from uml_matcher.classifier import Classifier
from graph_matcher import cached_eq


class Class(Classifier):
    @cached_eq
    def __eq__(self, other):
        return (id(self) == id(other)
                or super(Class, self).__eq__(other)
                and isinstance(other, Class))
