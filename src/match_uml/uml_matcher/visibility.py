# coding: utf-8

from enum import Enum


class Visibility(Enum):
    public = 1
    protected = 2
    private = 3

    def __str__(self):
        if self == Visibility.public:
            return ''
        elif self == Visibility.protected:
            return '#'
        elif self == Visibility.private:
            return '-'
