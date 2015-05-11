# coding: utf-8

import yaml
from unittest import TestCase, main
from hamcrest import assert_that, equal_to
from pattern_matcher.classifier import Classifier
from pattern_matcher.property import Property
from pattern_matcher.type import Type


class MakeClassifier(TestCase):
    def test_equivalent_pattern_should_succeed(self):
        assert_that(Classifier().equiv_pattern(Classifier()),
                    equal_to(True))

    def test_eq_empty_should_succeed(self):
        assert_that(Classifier(), not equal_to(Classifier()))
        assert_that(Classifier('A'), equal_to(Classifier('A')))

    def test_eq_with_property_should_succeed(self):
        assert_that(
            Classifier('A', properties=[Property(Type(Classifier('B')), 'b')]),
            equal_to(Classifier('A', properties=[
                Property(Type(Classifier('B')), 'b')])))

    def test_eq_two_recursive_should_succeed(self):
        a1 = Classifier('A')
        a1.properties = [Property(Type(a1), 'a')]
        a2 = Classifier('A')
        a2.properties = [Property(Type(a2), 'a')]
        assert_that(a1, equal_to(a2))
        assert_that(a1.equiv_pattern(a2), equal_to(True))

    def test_dump_and_load_yaml_classifier_with_name_should_succeed(self):
        data = "!Classifier {name: a}\n"
        classifier = Classifier('a')
        assert_that(yaml.dump(classifier), equal_to(data))
        assert_that(yaml.load(data), equal_to(classifier))

    def test_dump_and_load_yaml_classifier_with_property_should_succeed(self):
        classifier = Classifier('a', properties=[Property(name='a')])
        data = (
            "!Classifier\n"
            "name: a\n"
            "properties:\n"
            "- !Property {name: a}\n"
        )
        assert_that(yaml.dump(classifier), equal_to(data))
        assert_that(yaml.load(data), equal_to(classifier))

    def test_dump_and_load_yaml_recursive_classifier_should_succeed(self):
        classifier = Classifier('a')
        classifier.suppliers = [classifier]
        data = "&id001 !Classifier\nname: a\nsuppliers:\n- *id001\n"
        assert_that(yaml.dump(classifier), equal_to(data))
        assert_that(yaml.load(data), equal_to(classifier))


if __name__ == '__main__':
    main()
