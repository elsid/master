# coding: utf-8

from patterns.cached_method import cached_method
from patterns.abstract_factory import AbstractFactory
from patterns.decorator import Decorator

PATTERNS = (
    AbstractFactory,
    Decorator,
)


class InvalidPatternName(Exception):
    def __init__(self, name):
        super(InvalidPatternName, self).__init__(
            'invalid pattern name: %s' % name)
        self.name = name


def make_pattern(name):
    patterns = {pattern.__name__: pattern for pattern in PATTERNS}
    if name not in patterns:
        raise InvalidPatternName(name)
    return patterns[name]().diagram()
