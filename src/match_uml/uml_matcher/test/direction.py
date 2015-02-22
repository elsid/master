#coding: utf-8

from unittest import TestCase, main
from hamcrest import assert_that, calling, raises, equal_to
from uml_matcher.direction import Direction

class MakeDirection(TestCase):
    def test_make(self):
        assert_that(str(Direction.in_), equal_to(''))
        assert_that(str(Direction.out), equal_to('out'))
        assert_that(str(Direction.inout), equal_to('inout'))

if __name__ == '__main__':
    main()
