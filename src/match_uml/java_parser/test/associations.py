# coding: utf-8

from unittest import TestCase, main
from hamcrest import assert_that, contains_inanyorder
from uml_matcher import Class, Type, Property, Interface, BinaryAssociation
from java_parser.associations import make_associations


class MakeAssociations(TestCase):
    def test_make_should_succeed(self):
        class_a = Class('A')
        interface_b = Interface('B')
        type_a = Type(class_a)
        type_b = Type(interface_b)
        property_b_of_a = Property(type_b, 'b', owner=class_a)
        property_a_of_b = Property(type_a, 'a', owner=interface_b)
        class_a.properties.append(property_a_of_b)
        interface_b.properties.append(property_b_of_a)
        associations = make_associations({'A': type_a, 'B': type_b})
        assert_that(associations, contains_inanyorder(
            BinaryAssociation({property_b_of_a, Property(type_a, 'A_end')}),
            BinaryAssociation({property_a_of_b, Property(type_b, 'B_end')}),
        ))

if __name__ == '__main__':
    main()
