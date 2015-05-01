# coding: utf-8

from graph_matcher import cached_eq
from uml_matcher.classifier import Classifier


class PrimitiveType(Classifier):
    @cached_eq
    def __eq__(self, other):
        return (id(self) == id(other)
                or super(PrimitiveType, self).__eq__(other)
                and isinstance(other, PrimitiveType))
