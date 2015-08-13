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


class Item45:
    """
    Use datetime instead of time for local clocks
    """
    def __init__(self):
        from time import localtime, strftime, mktime, strptime

        now = 1407694710
        local_tuple = localtime(now)
        time_format = '%Y-%m-%d %H:%M:%S'
        time_str = strftime(time_format, local_tuple)
        print(time_str)

        time_tuple = strptime(time_str, time_format)
        utc_now = mktime(time_tuple)
        print(utc_now)

        parse_format = '%Y-%m-%d %H:%M:%S %Z'
        depart_sfo = '2014-05-01 15:45:16 PDT'
        time_tuple = strptime(depart_sfo, parse_format)
        time_str = strftime(time_format, time_tuple)
        print(time_str)

        from datetime import datetime, timezone
        now = datetime(2014, 8, 10, 18, 18, 30)
        now_utc = now.replace(tzinfo=timezone.utc)
        now_local = now_utc.astimezone()
        print(now_local)

        time_str = '2014-08-10 11:18:30'
        now = datetime.strptime(time_str, time_format)
        time_tuple = now.timetuple()
        utc_now = mktime(time_tuple)
        print(utc_now)

        # pytz
        import pytz
        arrival_nyc = '2014-05-01 23:33:24'
        nyc_dt_naive = datetime.strptime(arrival_nyc, time_format)
        eastern = pytz.timezone('US/Eastern')
        nyc_dt = eastern.localize(nyc_dt_naive)
        utc_dt = pytz.utc.normalize(nyc_dt.astimezone(pytz.utc))
        print(utc_dt)

        pacific = pytz.timezone('US/Pacific')
        sf_dt = pacific.normalize(utc_dt.astimezone(pacific))
        print(sf_dt)

        nepal = pytz.timezone('Asia/Katmandu')
        nepal_dt = nepal.normalize(utc_dt.astimezone(nepal))
        print(nepal_dt)

class Item46:
    """
    Use built-in algorithms and data structures
    """
    def __init__(self):
        from collections import deque, OrderedDict, defaultdict
        import random
        fifo = deque()
        fifo.append(1)
        x = fifo.popleft()

        # Dictionary
        a = {}
        a['foo'] = 1
        a['bar'] = 2

        # Randomly populate 'b' to cause hash conflicts
        while True:
            z = random.randint(99, 1013)
            b = {}
            for i in range(z):
                b[i] = i
            b['foo'] = 1
            b['bar'] = 2
            for i in range(z):
                del b[i]
            if str(b) != str(a):
                break

        print(a)
        print(b)
        print('Equal?', a == b)


        # OrderedDict
        a = OrderedDict()
        a['foo'] = 1
        a['bar'] = 2
        b = OrderedDict()
        b['foo'] = 'red'
        b['bar'] = 'blue'

        for value1, value2 in zip(a.values(), b.values()):
            print(value1, value2)

        # DefaultDict
        stats = {}
        key = 'my_counter'
        if key not in stats:
            stats[key] = 0
        stats[key] += 1

        stats = defaultdict(int)
        stats['my_counter'] += 1

        # Heap Queue
        import heapq
        a = []
        heapq.heappush(a, 5)
        heapq.heappush(a, 3)
        heapq.heappush(a, 7)
        heapq.heappush(a, 4)
        print(a)
        print(heapq.heappop(a), heapq.heappop(a), heapq.heappop(a), heapq.heappop(a))


        # Bisection
        import bisect
        x = list(range(10**6))
        i = x.index(991234)
        i = bisect.bisect_left(x, 991234)

        # Itertools -- From PyMOTW
        # Chain
        import itertools
        for i in itertools.chain([1, 2, 3],['a', 'b', 'c']):
            print(i)

        # izip
        for i in zip([1, 2, 3], ['a', 'b', 'c']):
            print(i)

        # count
        for i in zip(itertools.count(), ['a', 'b', 'c']):
            print(i)

        i = 0
        for item in itertools.cycle(['a', 'b', 'c']):
            print(item)
            if i == 10:
                break
            i += 1


        print(list(itertools.islice(range(10), 4, 6)))
        print(list(itertools.takewhile(lambda x: x < 5, [1,4,6,7,3])))
        print(list(itertools.dropwhile(lambda x: x < 5, [1,4,6,7,3])))
        print(list(filter(lambda x: x < 5, [1,4,6,7,3])))
        print(list(itertools.filterfalse(lambda x: x < 5, [1,4,6,7,3])))

        a = range(3)
        b = range(4,7)
        print(list(itertools.product(a,b)))
        print(list(itertools.permutations(b)))
        print(list(itertools.combinations(a, 2)))

if __name__ == '__main__':
    sol = Item42()
    print(fibonacci)
    help(fibonacci)
    sol = Item45()
    sol = Item46()
