# coding: utf-8

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
                 subsetted_properties=tuple(),
                 owner=None):
        super(Property, self).__init__(name)
        self.type = type
        self.visibility = visibility
        self.aggregation = aggregation
        self.is_derived = is_derived
        self.is_derived_union = is_derived_union
        self.is_id = is_id
        self.is_leaf = is_leaf
        self.is_read_only = is_read_only
        self.is_static = is_static
        self.subsetted_properties = subsetted_properties
        self.owner = owner

    def sub_equiv_pattern(self, pattern):
        return (self.sub_eq(pattern)
                and (self.type is None or pattern.type is not None
                     and self.type.sub_equiv_pattern(pattern.type)))

    def equivalent_pattern(self, pattern):
        return (self.sub_equiv_pattern(pattern) and self.owner is None
                or self.owner is not None and pattern.owner is not None
                and self.owner.equivalent_pattern(pattern.owner))

    def sub_eq(self, other):
        return (id(self) == id(other)
                or isinstance(other, Property)
                and self.visibility == other.visibility
                and self.aggregation == other.aggregation
                and self.is_derived == other.is_derived
                and self.is_derived_union == other.is_derived_union
                and self.is_id == other.is_id
                and self.is_leaf == other.is_leaf
                and self.is_read_only == other.is_read_only
                and self.is_static == other.is_static
                and self.subsetted_properties == other.subsetted_properties)

    def __eq__(self, other):
        return (id(self) == id(other)
                or super(Property, self).__eq__(other)
                and isinstance(other, Property)
                and self.sub_eq(other)
                and self.type == other.type)

    def __repr__(self):
        return ('{visibility}{owner}{name}'.format(
            visibility=self.visibility,
            name=self.name,
            owner='' if self.owner is None else '%s::' % self.owner,
        ))

    def __hash__(self):
        return id(self)
