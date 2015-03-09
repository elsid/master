# coding: utf-8

from uml_matcher.classifier import Classifier


class DataType(Classifier):
    def __eq__(self, other):
        return (id(self) == id(other)
                or super(DataType, self).__eq__(other)
                and isinstance(other, DataType))
