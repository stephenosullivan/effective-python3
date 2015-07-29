__author__ = 'stephenosullivan'

class Item1:
    import sys
    print(sys.version_info)
    print(sys.version)

class Item3:
    """Know the differences between bytes, str, and unicode"""
    def __init__(self, a):
        _a = a
        #print(self.to_str(a))
        #print(self.to_byte(a))

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

    def get_first_int(self, values, key, default = 0):
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
        chile_ranks = {'ghost':1, 'habanero':2, 'cayenne':3}
        rank_dict = {rank: name for name, rank in chile_ranks.items()}
        chile_len_set = {len(name) for name in rank_dict.values()}
        print(rank_dict, chile_len_set)


if __name__ == "__main__":
    sol1 = Item1()
    sol3 = Item3("This is a string")
    sol4 = Item4()
    sol6 = Item6()
    sol7 = Item7([1,2,3])

