# coding: utf-8

from uml_matcher.classifier import Classifier


class PrimitiveType(Classifier):
    def __eq__(self, other):
        return (id(self) == id(other)
                or super(PrimitiveType, self).__eq__(other)
                and isinstance(other, PrimitiveType))
