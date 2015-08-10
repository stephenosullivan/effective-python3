__author__ = 'stephenosullivan'

class Item42:
    """
    Define function decorators with functools.wraps
    """
    def __init__(self):
        self.fibonacci(3)

    def trace(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            print('%s(%r, %r) -> %r' % (func.__name__, args, kwargs, result))
            return result
        return wrapper

    @trace
    def fibonacci(self, n):
        """
        Return the nth Fibonacci number
        :param n:
        :return:
        """
        if n in (0, 1):
            return n
        return self.fibonacci(n - 2) + self.fibonacci(n - 1)

if __name__ == '__main__':
    sol = Item42()