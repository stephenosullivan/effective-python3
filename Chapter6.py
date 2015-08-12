__author__ = 'stephenosullivan'

import functools

class Item42:
    """
    Define function decorators with functools.wraps
    """
    def __init__(self):
        fibonacci(3)

def trace(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print('%s(%r, %r) -> %r' % (func.__name__, args, kwargs, result))
        return result
    return wrapper

@trace
def fibonacci(n):
    """
    Return the nth Fibonacci number
    :param n:
    :return:
    """
    if n in (0, 1):
        return n
    return fibonacci(n - 2) + fibonacci(n - 1)

if __name__ == '__main__':
    sol = Item42()
    print(fibonacci)
    help(fibonacci)
