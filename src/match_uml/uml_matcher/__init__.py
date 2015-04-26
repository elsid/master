# coding: utf-8

from uml_matcher.aggregation import Aggregation
from uml_matcher.classifier import Classifier
from uml_matcher.data_type import DataType
from uml_matcher.diagram import (
    Diagram, Generalization, BinaryAssociation, Dependency)
from uml_matcher.direction import Direction
from uml_matcher.enumeration import Enumeration
from uml_matcher.interface import Interface
from uml_matcher.match import MatchResult
from uml_matcher.named_element import NamedElement
from uml_matcher.operation import Operation
from uml_matcher.parameter import Parameter
from uml_matcher.primitive_type import PrimitiveType
from uml_matcher.property import Property
from uml_matcher.type import Type
from uml_matcher.visibility import Visibility
Class = __import__('uml_matcher.class', fromlist=['Class']).Class
