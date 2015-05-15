# coding: utf-8

from pattern_matcher import Class, Model, cached_method


class BaseDerived(object):
    @cached_method
    def base(self):
        return Class('Base')

    @cached_method
    def derived(self):
        return Class('Derived', generals=[self.base()])

    @cached_method
    def create(self):
        return Model([self.base(), self.derived()])


if __name__ == '__main__':
    print BaseDerived().create()