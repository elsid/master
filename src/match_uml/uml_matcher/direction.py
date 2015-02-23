# coding: utf-8

from enum import Enum


class Direction(Enum):
    in_ = 1
    out = 2
    inout = 3

    def __str__(self):
        if self == Direction.in_:
            return ''
        elif self == Direction.out:
            return 'out'
        elif self == Direction.inout:
            return 'inout'
