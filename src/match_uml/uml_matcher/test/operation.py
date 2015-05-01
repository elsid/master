# coding: utf-8

from unittest import TestCase, main
from hamcrest import assert_that, equal_to
from uml_matcher.operation import Operation


class MakeOperation(TestCase):
    def test_equivalent_pattern_should_succeed(self):
        assert_that(Operation(None).sub_equiv_pattern(Operation(None)),
                    equal_to(True))

if __name__ == '__main__':
    main()
