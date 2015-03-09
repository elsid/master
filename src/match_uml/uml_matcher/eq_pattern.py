# coding: utf-8

from collections import Iterable


def _op_pattern(value, other, mult, single):
    return (other is None
            or value is None and other is None
            or value is not None and (isinstance(other, Iterable) and mult()
                                      or single()))


def eq_pattern(value, other):
    return _op_pattern(value, other, lambda: value in other,
                       lambda: value == other)


def equiv_pattern(value, other):

    def mult():
        for x in other:
            if value.equiv_pattern(x):
                return True

    return _op_pattern(value, other, mult, lambda: value.equiv_pattern(other))


def sub_equiv_pattern(value, other):

    def mult():
        for x in other:
            if value.sub_equiv_pattern(x):
                return True

    return _op_pattern(value, other, mult,
                       lambda: value.sub_equiv_pattern(other))
