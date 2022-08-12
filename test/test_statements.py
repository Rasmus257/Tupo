# Statements
from abc import ABCMeta
from os.path import join as j
from os.path import join
import os.path
import os
args = (1, 2)
kwargs = {'x': 1, 'y': 2}
x = y = 1
x, y = args
x += 2
assert 1 == 1, 'reason'
del kwargs['x']
pass


# Function definitions
lambda x: x + 1


def decorator(f):
    def decorated(*args, **kwargs):
        return f(*args, **kwargs)
    return decorated


@decorator
@decorator
def ite(cond: str, true=True, false=False):
    if cond:
        return true
    return false


def nums():
    x = 0
    while True:
        yield x
        x += 1


def f(x):
    global y
    y = x

    def g(y):
        nonlocal x
        x = y
    return g

# Class statements


class A(object):
    def __init__(self, x):
        self.x = x


@decorator
class B(A, metaclass=ABCMeta):
    pass


class C():
    def __init__(self, x):
        super().__init__(x)
        self.x = x


class D:
    def __str__(self, x):
        return x

    def __repr__(self, x):
        return x

    @staticmethod
    def call(x):
        return x

    @classmethod
    def call(cls, x):
        return x


print(__file__ + ' = ok')
