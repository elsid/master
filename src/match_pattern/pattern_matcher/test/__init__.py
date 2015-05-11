# coding: utf-8

from pattern_matcher.test.type import ReprMultiplicity, MakeType
from pattern_matcher.test.direction import MakeDirection
from pattern_matcher.test.has_equivalents import HasEquivalents
from pattern_matcher.test.classifier import MakeClassifier
from pattern_matcher.test.operation import MakeOperation
from pattern_matcher.test.model import MatchModel, ReprModel, YamlModel
from pattern_matcher.test.match import (
    EqIgnoreOrder, Check, MakeMatchVariant, MakeMatchResult)
from pattern_matcher.test.property import MakeProperty
from pattern_matcher.test.data_type import MakeDataType
from pattern_matcher.test.interface import MakeInterface
from pattern_matcher.test.parameter import MakeParameter
from pattern_matcher.test.aggregation import MakeAggregation
from pattern_matcher.test.primitive_type import MakePrimitiveType
from pattern_matcher.test.enumeration import MakeEnumeration
from pattern_matcher.test.visibility import MakeVisibility
MakeClass = __import__('pattern_matcher.test.class',
                       fromlist=['MakeClass']).MakeClass
