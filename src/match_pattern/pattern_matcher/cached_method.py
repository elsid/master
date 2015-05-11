#!/usr/bin/env python
# coding: utf-8


def cached_method(method):

    def enable(self):
        setattr(self, '__cache_enabled', True)

    def disable(self):
        setattr(self, '__cache_enabled', False)

    def reset(self):
        setattr(self, '__cache', {})

    def wrapper(self, *args, **kwargs):
        if not hasattr(self, '__cache'):
            setattr(self, '__cache', {})
            setattr(self, 'enable_cache', enable)
            setattr(self, 'disable_cache', disable)
            setattr(self, 'reset_cache', reset)
            setattr(self, '__cache_enabled', True)
        elif not getattr(self, '__cache_enabled'):
            return method(self, *args, **kwargs)
        cache = getattr(self, '__cache')
        if method in cache:
            return cache[method]
        result = method(self, *args, **kwargs)
        cache[method] = result
        return result

    return wrapper
