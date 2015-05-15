# coding: utf-8

from patterns.abstract_factory import AbstractFactory
from patterns.base_derived import BaseDerived
from patterns.bridge import Bridge
from patterns.chain_of_responsibility import ChainOfResponsibility
from patterns.decorator import Decorator
from patterns.empty import Empty
from patterns.memento import Memento
from patterns.method_overriding import MethodOverriding


PATTERNS = (
    AbstractFactory,
    BaseDerived,
    Bridge,
    ChainOfResponsibility,
    Decorator,
    Empty,
    Memento,
    MethodOverriding,
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
    return patterns[name]().create()


def names():
    return (pattern.__name__ for pattern in PATTERNS)
