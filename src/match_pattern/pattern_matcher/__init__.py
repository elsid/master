# coding: utf-8

from pattern_matcher.aggregation import Aggregation
from pattern_matcher.classifier import Classifier
from pattern_matcher.data_type import DataType
from pattern_matcher.model import Model
from pattern_matcher.direction import Direction
from pattern_matcher.enumeration import Enumeration
from pattern_matcher.interface import Interface
from pattern_matcher.match import MatchResult
from pattern_matcher.named_element import NamedElement
from pattern_matcher.operation import Operation
from pattern_matcher.parameter import Parameter
from pattern_matcher.primitive_type import PrimitiveType
from pattern_matcher.property import Property
from pattern_matcher.type import Type
from pattern_matcher.visibility import Visibility
from pattern_matcher.cached_method import cached_method
Class = __import__('pattern_matcher.class', fromlist=['Class']).Class
