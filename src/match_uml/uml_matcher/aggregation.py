# coding: utf-8

from enum import Enum


class Aggregation(Enum):
    none = 'none'
    shared = 'shared'
    composite = 'composite'

    def __str__(self):
        return self.value
