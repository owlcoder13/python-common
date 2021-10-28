"""
Helpers for lazy loading in python
"""


class Lazy(object):
    def __init__(self, func):
        self.func = func
        self.value = None

    def __call__(self):
        if self.value is None:
            self.value = self.func()
        return self.value

    def __str__(self):
        if self.value is None:
            self.value = self.func()
        return self.value
