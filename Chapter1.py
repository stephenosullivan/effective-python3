__author__ = 'stephenosullivan'


class Item1:
    import sys

    print(sys.version_info)
    print(sys.version)


class Item3:
    """Know the differences between bytes, str, and unicode"""

    def __init__(self, a):
        _a = a
        # print(self.to_str(a))
        # print(self.to_byte(a))

    def to_str(self, bytes_or_str):
        if isinstance(bytes_or_str, bytes):
            value = bytes_or_str.decode('utf-8')
        else:
            value = bytes_or_str
        return value

    def to_byte(self, bytes_or_str):
        if isinstance(bytes_or_str, str):
            value = bytes_or_str.encode('utf-8')
        else:
            value = bytes_or_str
        return value


class Item4:
    """Write helper functions instead of complex expressions"""

    def __init__(self):
        from urllib.parse import parse_qs

        my_values = parse_qs('red=5&blue=0&green=', keep_blank_values=True)
        print(repr(my_values))

        print('Red:     ', my_values.get('red'))
        print('Green:   ', my_values.get('green'))
        print('Opacity: ', my_values.get('opacity'))

        print('Red:     ', my_values.get('red', [''])[0] or 0)
        print('Green:   ', my_values.get('green', [''])[0] or 0)
        print('Opacity: ', my_values.get('opacity', [''])[0] or 0)
        """my_values.get(a,b) -- Try to get a; if None: get b"""

        green = self.get_first_int(my_values, 'green')
        print('Green is ', green)

    def get_first_int(self, values, key, default=0):
        found = values.get(key, [''])
        if found[0]:
            found = int(found[0])
        else:
            found = default
        return found


class Item6:
    """
    Item 5: Know how to slice sequences

    Avoid using start, end, and stride in a single slice
    some_list[start:end:stride]
    """

    def __init__(self):
        x = b'mongoose'
        y = x[::-1]
        print(y)
        sol = Item3(0)
        z = sol.to_str('到三藩啦')
        print(z)
        print(sol.to_byte(z))
        try:
            print(sol.to_byte(z)[::-1].decode())
        except UnicodeDecodeError:
            print('Cannot decode to_byte(z)[::-1]')


class Item7:
    """
    Use list comprehensions instead of map and filter
    """

    def __init__(self, input_list):
        print('Item 7\n')
        print('List comprehension: ', self.sum_of_squares(input_list))
        print('Map: ', self.sum_of_squares_map(input_list))
        self.dictionary_comprehension()

    def sum_of_squares(self, input_list):
        return sum([x * x for x in input_list])

    def sum_of_squares_map(self, input_list):
        return sum(map(lambda x: x * x, input_list))

    def dictionary_comprehension(self):
        chile_ranks = {'ghost': 1, 'habanero': 2, 'cayenne': 3}
        rank_dict = {rank: name for name, rank in chile_ranks.items()}
        chile_len_set = {len(name) for name in rank_dict.values()}
        print(rank_dict, chile_len_set)


class Item8:
    """
    Avoid more than two expressions in list comprehensions
    """

    def __init__(self):
        matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        flat = [x for row in matrix for x in row]
        squared = [[x * x for x in row] for row in matrix]

    def flat_clean(self, in_list):
        flat = []
        for sublist1 in in_list:
            for sublist2 in sublist1:
                flat.extend(sublist2)


class Item9:
    """
    Consider Generator Expressions for Large Comprehensions
    """

    def __init__(self):
        """
        Use () instead of [] to make a generator expression
        """
        import inspect

        print(inspect.getfile(inspect.currentframe()))  # script filename (usually with path)
        print(__file__)
        self.it = (len(x) for x in open(__file__))
        print(next(self.it))
        self.loop_over_it(10)

    def loop_over_it(self, count):
        roots = ((x, x ** 0.5) for x in self.it)
        while count:
            print(next(roots))
            count -= 1


class Item10:
    """
    Prefer Enumerate over range
    """
    def __init__(self):
        print(self.rand_int_generator())
        flavor_list = ['vanilla', 'chocolate', 'pecan', 'strawberry']
        self.enum_test(flavor_list)


    # range() example
    def rand_int_generator(self, default=0):
        from random import randint
        random_bits = default
        for i in range(64):
            if randint(0, 1):
                random_bits |= 1 << i  # | bitwise or
        return random_bits

    def enum_test(self, in_list):
        for index, elem in enumerate(in_list, 1):
            print(index, ':', elem)
            # print('%d: %s' %(index, elem))


class Item11:
    """
    Use zip to process iterators in parallel
    """
    # Use zip_longest from itertools if input iterators are different lengths
    def __init__(self):
        names = ['Michael', 'George', 'Sean', 'Lisa']
        letters = [len(x) for x in names]
        print(self.longest_name(names, letters))

    def longest_name(self, names, letters):
        max_letters = 0
        longname = None
        for name, count in zip(names, letters):
            if count > max_letters:
                longname = name
                max_letters = count
        return longname, max_letters

class Item12:
    """
    Avoid else blocks after for while loops
    """
    # Else block runs if the for loops complete
    def __init__(self):
        self.for_else_test()
        print(self.coprime(11, 22))
        print(self.coprime(11, 25))

    def for_else_test(self):
        for i in range(3):
            print('loop %d' % i)
        else:
            print('Else block!')

    def coprime(self, n1, n2):
        for i in range(2,min(n1, n2)+1):
            if n1%i == 0 and n2%i == 0:
                return False
        else:
            return True


class Item13:
    """
    Take advantage of each block in try/except/else/finally
    """


if __name__ == "__main__":
    sol1 = Item1()
    sol3 = Item3("This is a string")
    sol4 = Item4()
    sol6 = Item6()
    sol7 = Item7([1, 2, 3])
    sol8 = Item8()
    sol9 = Item9()
    sol10 = Item10()
    sol11 = Item11()
    sol12 = Item12()
    sol13 = Item13()