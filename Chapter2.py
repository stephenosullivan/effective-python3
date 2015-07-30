from datetime import datetime
import json

__author__ = 'stephenosullivan'


class Item14:
    """
    Prefer exceptions to returning None
    """
    # Easy to confuse None and zero and empty string
    # since they all evaluate to false in conditional expressions

    # Except ignores other errors
    def __init__(self):
        print('Item14')
        print(self.divide(10, 4))
        print(self.divide(10, 0) if self.divide(10, 0) else 'Cannot divide by zero')
        self.divide_better_test(10, 4)
        self.divide_better_test(10, 0)

    def divide(self, a, b):
        try:
            return a / b
        except ZeroDivisionError:
            return None

    def divide_better(self, a, b):
        try:
            return a / b
        except ZeroDivisionError as e:
            raise ValueError('Invalid inputs') from e

    def divide_better_test(self, x, y):
        try:
            result = self.divide_better(x, y)
        except ValueError:
            print('Invalid Inputs')
        else:
            print('Result is %.1f' % result)


class Item15:
    """
    Know how closures interact with variable scope
    """
    # nonlocal -- scope traversal upon assignment
    def __init__(self):
        print('Item 15')
        numbers = [8, 3, 1, 2, 5, 4, 7, 6]
        group = {2, 3, 5, 7}
        self.sort_priority(numbers, group)
        print(numbers)
        print(self.closure_test())
        numbers = [8, 3, 1, 2, 5, 4, 7, 6]
        group = {2, 3, 5, 7}
        print(self.sort_priority3(numbers, group))
        print(numbers)
        numbers = [8, 3, 1, 2, 5, 4, 7, 6]
        group = {2, 3, 5, 7}
        sorter = Item15_Sorter(group)
        numbers.sort(key=sorter)
        assert sorter.found is True

    def sort_priority(self, values, group):
        def helper(x):
            if x in group:
                return 0, x
            return 1, x

        values.sort(key=helper)

    def closure_test(self):
        found = 1

        def test():
            # nonlocal found
            found = 2

        test()
        return found

    def sort_priority3(self, values, group):
        found = False

        def helper(x):
            nonlocal found
            if x in group:
                found = True
                return 0, x
            return 1, x

        values.sort(key=helper)
        return found


class Item15_Sorter(object):  # Not sure what this does
    def __init__(self, group):
        self.group = group
        self.found = False

    def __call__(self, x):
        if x in self.group:
            self.found = True
            return 0, x
        return 1, x


class Item16:
    """
    Consider generators instead of running lists
    """

    def __init__(self):
        from itertools import islice

        with open(__file__, 'r') as f:
            it = self.index_file(f)
            results = islice(it, 0, 16)
            print(list(results))

    def index_file(self, handle):
        offset = 0
        for line in handle:
            if line:
                yield offset
            for letter in line:
                offset += 1
                if letter == ' ':
                    yield offset


class Item17:
    """
    Be defensive when iterating over arguments
    """
    # Explicitly exhaust an input iterator and
    # keep a copy of its entire contents in a list

    # Or accept a function that returns a new iterator
    # each time it is called ???

    # Best way is just to build a class with __iter__
    # then calls can be made to __iter__ to allocate a
    # second iterator object

    def __init__(self):
        print('Item 17')
        # Not sure how this works
        # percentages = self.normalize_func(lambda: self.read_visits(__file__))
        visits = Item17_ReadVisits('./data_file_17.txt')
        percentages = self.normalize_defensive(visits)
        print(percentages)

    def read_visits(self, data_file):
        with open(data_file) as f:
            for line in f:
                yield int(line)

    def normalize(self, numbers):
        total = sum(numbers)
        result = []
        for value in numbers:
            percent = 100 * value / total
            result.append(percent)
        return result

    def normalize_func(self, get_iter):
        total = sum(get_iter())
        result = []
        for value in get_iter():
            percent = 100 * value / total
            result.append(percent)
        return result

    def normalize_defensive(self, numbers):
        if iter(numbers) is iter(numbers):  # returns an error if type iter
            raise TypeError('Must supply a container')
        total = sum(numbers)
        result = []
        for value in numbers:
            percent = 100 * value / total
            result.append(percent)
        return result


class Item17_ReadVisits:
    def __init__(self, data_path):
        self.data_path = data_path

    def __iter__(self):
        with open(self.data_path) as f:
            for line in f:
                yield int(line)


class Item18:
    """
    Reduce visual noise with variable positional arguments
    """

    def __init__(self):
        self.log('My numbers are', 1, 2)
        self.log('Hello there')
        it = self.my_generator()
        self.my_func(*it)
        it = self.my_generator()
        self.my_func(it)

    def log(self, message, *values):
        if not values:
            print(message)
        else:
            values_str = ', '.join(str(x) for x in values)
            print('%s: %s' % (message, values_str))

    def my_generator(self):
        for i in range(10):
            yield i

    def my_func(self, *args):
        print(args)

class Item20:
    """
    Use None and docstrings to specify dynamic default arguments
    """
    def __init__(self):
        self.log_bad('Hello there')
        self.log_bad('Hello there')     # Same time
        self.log('Hello there')
        self.log('Hello there')
        data = str(567)
        print(self.decode_bad(data))
        foo = self.decode_bad('bad data')
        foo['stuff'] = 5
        bar = self.decode_bad('also bad')
        bar['meep'] = 1
        print('Foo', foo)
        print('Bar', bar)

        # Test the good version
        foo = self.decode('data')
        foo['stuff'] = 5
        bar = self.decode('not bad')
        bar['meep'] = 1
        print('Foo', foo)
        print('Bar', bar)


    def log_bad(self, message, when=datetime.now()):
        print('%s: %s' % (message, when))

    def log(self, message, when=None):
        """
        Log a message with a timestamp
        :param message: Message to print
        :param when: datetime of when message occurred
                    Defaults to the present time
        :return: void
        """
        when = datetime.now() if when is None else when
        print('%s: %s' % (message, when))

    def decode_bad(self,data, default={}):
        try:
            return json.loads(data)
        except ValueError:
            return default

    def decode(self,data,default=None):
        """
        Load JSON data from a string

        :param data: JSON data to decode
        :param default:Value to return if decoding fails.
                Defaults to an empty dictionary
        :return: dict()
        """
        default = {} if default is None else default

        try:
            return json.loads(data)
        except ValueError:
            return default

class Item21:
    """
    Enforce clarity with keyword only arguments
    """
    def __init__(self):
        print(self.safe_division(1, 10**500, True, False))
        print(self.safe_division(10**500, 1, True, False))
        print(self.safe_division(1, 0, True, True))
        print(self.safe_division_c(1, 0, ignore_zero_division=True))

    def safe_division(self, number, divisor, ignore_overflow, ignore_zero_division):
        try:
            return number / divisor
        except OverflowError:
            if ignore_overflow:
                return 0
            else:
                raise
        except ZeroDivisionError:
            if ignore_zero_division:
                return float('inf')
            else:
                raise

    # Keyword-only safe division
    # '*' symbol indicates the end of positional arguments and the beginning
    # of keyword-only arguments

    def safe_division_c(self, number, divisor, *, ignore_overflow=False, ignore_zero_division=False):
        try:
            return number / divisor
        except OverflowError:
            if ignore_overflow:
                return 0
            else:
                raise
        except ZeroDivisionError:
            if ignore_zero_division:
                return float('inf')
            else:
                raise

if __name__ == "__main__":
    sol14 = Item14()
    sol15 = Item15()
    sol16 = Item16()
    sol17 = Item17()
    sol18 = Item18()
    sol20 = Item20()
    sol21 = Item21()
