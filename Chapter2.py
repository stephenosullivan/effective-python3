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
    # each time it is called
    def __init__(self):
        print('Item 17')
        #Not sure how this works
        #percentages = self.normalize_func(lambda: self.read_visits(__file__))
        visits = Item17_ReadVisits(path)
        percentages = self.normalize(visits)
        print(percentages)

    def read_visits(self, data_file):
        with open(data_file) as f:
            for line in f:
                yield int(line)

    def normalize_func(self, get_iter):
        total = sum(get_iter())
        result = []
        for value in get_iter():
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

if __name__ == "__main__":
    sol14 = Item14()
    sol15 = Item15()
    sol16 = Item16()
    sol17 = Item17()
