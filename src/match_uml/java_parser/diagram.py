# coding: utf-8

from uml_matcher import Diagram
from java_parser import (
    make_classifiers, make_generalizations, fill_classifiers, make_associations)


def make_diagram(tree):
    classifiers, errors = make_classifiers(tree)
    if errors:
        return Diagram(), errors
    generalizations = make_generalizations(tree, classifiers)
    types, errors = fill_classifiers(tree, classifiers)
    if errors:
        return Diagram(generalizations), errors
    associations = make_associations(types)
    return Diagram(generalizations, associations), tuple()
