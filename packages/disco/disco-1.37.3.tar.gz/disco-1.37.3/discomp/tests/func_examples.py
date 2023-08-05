import os
import sys


def mult(x, y=1):
    z = x * y
    print(z)
    return z


def hello():
    print('hello')


def pow3(x):
    z = x ** 3
    print(z)
    return z


def mult_wrapper(x, y=1):
    z = mult(x, y)
    return z
