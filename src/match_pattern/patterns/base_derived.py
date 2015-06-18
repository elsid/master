# coding: utf-8

from utils import cached_method
from pattern_matcher import Classifier, Model


class BaseDerived(object):
    @cached_method
    def base(self):
        return Classifier('Base')

    @cached_method
    def derived(self):
        return Classifier('Derived', generals=[self.base()])

    @cached_method
    def create(self):
        return Model([self.base(), self.derived()])


if __name__ == '__main__':
    print BaseDerived().create()
