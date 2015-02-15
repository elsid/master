#coding: utf-8

from unittest import TestCase, main
from hamcrest import assert_that, equal_to
from uml_matcher.classifier import Classifier

class MakeClassifierTest(TestCase):
    def test_equivalent_pattern_should_succeed(self):
        assert_that(Classifier().equivalent_pattern(Classifier()),
            equal_to(True))
