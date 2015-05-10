# coding: utf-8

import yaml
from unittest import TestCase, main
from hamcrest import assert_that, equal_to
from uml_matcher.aggregation import Aggregation


class MakeAggregation(TestCase):
    def test_make(self):
        assert_that(str(Aggregation.none), equal_to('none'))
        assert_that(str(Aggregation.shared), equal_to('shared'))
        assert_that(str(Aggregation.composite), equal_to('composite'))

    def test_yaml_dump(self):
        assert_that(yaml.dump(Aggregation.none),
                    equal_to("!Aggregation 'none'\n"))
        assert_that(yaml.dump(Aggregation.shared),
                    equal_to("!Aggregation 'shared'\n"))
        assert_that(yaml.dump(Aggregation.composite),
                    equal_to("!Aggregation 'composite'\n"))

    def test_yaml_load(self):
        assert_that(yaml.load("!Aggregation 'none'\n"),
                    equal_to(Aggregation.none))
        assert_that(yaml.load("!Aggregation 'shared'\n"),
                    equal_to(Aggregation.shared))
        assert_that(yaml.load("!Aggregation 'composite'\n"),
                    equal_to(Aggregation.composite))


if __name__ == '__main__':
    main()
