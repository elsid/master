# coding: utf-8

from enum import Enum


class Direction(Enum):
    in_ = 'in'
    out = 'out'
    inout = 'inout'

    def __str__(self):
        return self.value
