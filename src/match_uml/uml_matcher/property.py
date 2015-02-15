#coding: utf-8

from uml_matcher.named_element import NamedElement
from uml_matcher.visibility import Visibility
from uml_matcher.aggregation import Aggregation

class Property(NamedElement):
    def __init__(self, type,
            name='anonymous',
            visibility=Visibility.public,
            aggregation=Aggregation.none,
            is_derived=False,
            is_derived_union=False,
            is_id=False,
            is_leaf=False,
            is_read_only=False,
            is_static=False,
            subsetted_properties=tuple()):
        self.name = name
        self.visibility = visibility
        self.aggregation = aggregation
        self.is_derived = is_derived
        self.is_derived_union = is_derived_union
        self.is_id = is_id
        self.is_leaf = is_leaf
        self.is_read_only = is_read_only
        self.is_static = is_static
        self.subsetted_properties = subsetted_properties
        self.owner = None

    def sub_equivalent_pattern(self, pattern):
        return self == pattern

    def equivalent_pattern(self, pattern):
        return (self == pattern and self.owner is None
            or self.owner is not None and pattern.owner is not None
            and self.owner.equivalent_pattern(pattern.owner))

    def __eq__(self, other):
        if other is None  or not isinstance(other, type(self)):
            return False
        return (self.visibility == other.visibility
            and self.aggregation == other.aggregation
            and self.is_derived == other.is_derived
            and self.is_derived_union == other.is_derived_union
            and self.is_id == other.is_id
            and self.is_leaf == other.is_leaf
            and self.is_read_only == other.is_read_only
            and self.is_static == other.is_static
            and self.subsetted_properties == other.subsetted_properties)

    def __repr__(self):
        return ('{visibility}{name}'.format(
            visibility=self.visibility,
            name=self.name))

    def __hash__(self):
        return id(self)
