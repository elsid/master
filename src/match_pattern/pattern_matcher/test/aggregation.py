# coding: utf-8

import yaml
from unittest import TestCase, main
from hamcrest import assert_that, equal_to
from pattern_matcher.aggregation import Aggregation


class MakeAggregation(TestCase):
    def test_make(self):
        assert_that(str(Aggregation.NONE), equal_to('none'))
        assert_that(str(Aggregation.SHARED), equal_to('shared'))
        assert_that(str(Aggregation.COMPOSITE), equal_to('composite'))

    def test_yaml_dump(self):
        assert_that(yaml.dump(Aggregation.NONE),
                    equal_to("!Aggregation 'none'\n"))
        assert_that(yaml.dump(Aggregation.SHARED),
                    equal_to("!Aggregation 'shared'\n"))
        assert_that(yaml.dump(Aggregation.COMPOSITE),
                    equal_to("!Aggregation 'composite'\n"))

    def test_yaml_load(self):
        assert_that(yaml.load("!Aggregation 'none'\n"),
                    equal_to(Aggregation.NONE))
        assert_that(yaml.load("!Aggregation 'shared'\n"),
                    equal_to(Aggregation.SHARED))
        assert_that(yaml.load("!Aggregation 'composite'\n"),
                    equal_to(Aggregation.COMPOSITE))
