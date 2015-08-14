__author__ = 'stephenosullivan'

class Item55:
    """
    Use repr Strings for debugging output
    """
    def __init__(self):
        a = "string"
        print(a)
        print(repr(a))
        print(eval(repr(a)))

        print('%r' % a)

        a = Opaque(5,4)
        print(a)
        b = BetterClass(6,7)
        print(b)
        print(a.__dict__)

class Opaque:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class BetterClass:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "BetterClass(%s, %s)" % (self.x, self.y)


class Item56:
    """
    Test everything with unittest
    """
    def __init__(self):
        return

def to_str(data):
    if isinstance(data, str):
        return data
    elif isinstance(data, bytes):
        return data.decode('utf-8')
    else:
        raise TypeError('Must supply string or bytes, ' 'found: %r' % data)

from unittest import TestCase, main
class UtilsTestCase(TestCase):
    def test_to_str_bytes(self):
        self.assertEqual('hello', to_str(b'hello'))

    def test_to_str_str(self):
        self.assertEqual('hello', to_str('hello'))

    def test_to_str_bad(self):
        self.assertRaises(TypeError, to_str, object())



if __name__ == "__main__":
    sol = Item55()
    main()
