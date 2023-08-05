# Copyright © 2020 Noel Kaczmarek
from functools import wraps

import time


def timestamp():
    return int(round(time.time() * 1000))


def all_methods(decorator):
    def decorate(cls):
        for attr in cls.__dict__:
            if callable(getattr(cls, attr)):
                setattr(cls, attr, decorator(getattr(cls, attr)))
        return cls
    return decorate