# coding: utf-8

from uml_matcher.test.type import ReprMultiplicity, MakeType
from uml_matcher.test.direction import MakeDirection
from uml_matcher.test.has_equivalents import HasEquivalents
from uml_matcher.test.classifier import MakeClassifier
from uml_matcher.test.operation import MakeOperation
from uml_matcher.test.diagram import MatchDiagram, ReprDiagram
from uml_matcher.test.match import (
    EqIgnoreOrder, Check, MakeMatchVariant, MakeMatchResult)
from uml_matcher.test.property import MakeProperty
from uml_matcher.test.data_type import MakeDataType
from uml_matcher.test.interface import MakeInterface
from uml_matcher.test.parameter import MakeParameter
from uml_matcher.test.aggregation import MakeAggregation
from uml_matcher.test.primitive_type import MakePrimitiveType
from uml_matcher.test.enumeration import MakeEnumeration
from uml_matcher.test.visibility import MakeVisibility
MakeClass = __import__('uml_matcher.test.class',
                       fromlist=['MakeClass']).MakeClass
