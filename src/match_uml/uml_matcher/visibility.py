# coding: utf-8

from enum import Enum


class Visibility(Enum):
    public = 'public'
    protected = 'protected'
    private = 'private'

    def __str__(self):
        if self == Visibility.public:
            return '+'
        elif self == Visibility.protected:
            return '#'
        elif self == Visibility.private:
            return '-'
