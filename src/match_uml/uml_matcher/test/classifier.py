# coding: utf-8

from unittest import TestCase, main
from hamcrest import assert_that, equal_to
from uml_matcher.classifier import Classifier
from uml_matcher.property import Property
from uml_matcher.type import Type


class MakeClassifier(TestCase):
    def test_equivalent_pattern_should_succeed(self):
        assert_that(Classifier().equiv_pattern(Classifier()),
                    equal_to(True))

    def test_eq_empty_should_succeed(self):
        assert_that(Classifier(), equal_to(Classifier()))

    def test_eq_with_property_should_succeed(self):
        assert_that(
            Classifier('A', [Property(Type(Classifier('B')), 'b')]),
            equal_to(Classifier('A', [Property(Type(Classifier('B')), 'b')])))

    def test_eq_two_recursive_should_succeed(self):
        a1 = Classifier('A')
        a1.properties = [Property(Type(a1), 'a')]
        a2 = Classifier('A')
        a2.properties = [Property(Type(a2), 'a')]
        assert_that(a1, equal_to(a2))
        assert_that(a1.equiv_pattern(a2), equal_to(True))

if __name__ == '__main__':
    main()
