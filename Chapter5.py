__author__ = 'stephenosullivan'

import subprocess, time, os
from threading import Thread
from threading import Barrier
from threading import Lock
import select
from time import sleep
from queue import Queue
from collections import namedtuple


class item36:
    def __init__(self):
        print('-----------------\n'
              'Item 36\n'
              '-----------------\n')
        proc = subprocess.Popen(['echo', 'Hello from the child!'], stdout=subprocess.PIPE)
        out, err = proc.communicate()
        print(out.decode('utf-8'))

        proc = subprocess.Popen(['sleep', '0.3'])
        # while proc.poll() is None:
        #     print('Working...')
        print('Exit status', proc.poll())

        start = time.time()
        procs = []
        for i in range(10):
            #proc = self.run_sleep(0.1)
            proc = self.run_print(i)
            procs.append(proc)

        for proc in procs:
            proc.communicate()
        end = time.time()
        print('Finished in %.3f seconds' % (end - start))

        # Encrypt data
        procs = []
        for _ in range(3):
            data = os.urandom(10)
            proc = self.run_openssl(data)
            procs.append(proc)

        for proc in procs:
            out, err = proc.communicate()
            #print(out)
            print(out[-10:])

        # Piping
        input_procs = []
        hash_procs = []
        for _ in range(3):
            data = os.urandom(10)
            proc = self.run_openssl(data)
            input_procs.append(proc)
            hash_proc = self.run_md5(proc.stdout)
            hash_procs.append(hash_proc)

        for proc in input_procs:
            proc.communicate()
        for proc in hash_procs:
            out, err = proc.communicate()
            print(out.strip())

        # place time limit on execution
        proc = self.run_sleep(10)
        try:
            proc.communicate(timeout=0.1)
        except subprocess.TimeoutExpired:
            proc.terminate()
            proc.wait()

        print('Exit Status', proc.poll())

    def run_sleep(self, period):
        proc = subprocess.Popen(['sleep', str(period)])
        return proc

    def run_print(self, iteration):
        proc = subprocess.Popen(['echo', 'Process ' + str(iteration)])
        return proc

    def run_openssl(self, data):
        env = os.environ.copy()
        env['password'] = b'\xe24U\n\xd0Q13S\x11'
        proc = subprocess.Popen(['openssl', 'enc', '-des3', '-pass', 'env:password'],
                                env=env,
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE)
        proc.stdin.write(data)
        proc.stdin.flush()
        return proc

    def run_md5(self, input_stdin):
        proc = subprocess.Popen(
            ['md5'],
            stdin=input_stdin,
            stdout=subprocess.PIPE
        )
        return proc

class item37:
    def __init__(self):
        print('------------------\n'
              'Item 37\n'
              '------------------')
        numbers = [2139079, 1214759, 1516637, 1852285]
        start = time.time()
        for number in numbers:
            list(factorize(number))
        end = time.time()
        print('Took %.3f seconds' % (end - start))

        start = time.time()
        threads = []
        for number in numbers:
            thread = FactorizeThread(number)
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()
        end = time.time()
        print('Took %.3f seconds' % (end - start))

        # Slow system call
        start = time.time()
        for _ in range(5):
            slow_systemcall()
        end = time.time()
        print('Took %.3f seconds' % (end - start))

        # Multiple system call
        start = time.time()
        threads = []
        for _ in range(5):
            thread = Thread(target=slow_systemcall())
            thread.start()
            threads.append(thread)

        for i in range(5):
            compute_helicopter_location(i)

        for thread in threads:
            thread.join()
        end = time.time()
        print('Took %.3f seconds' % (end - start))

def factorize(number):
    for i in range(1, number+1):
        if number % i == 0:
            yield i


class FactorizeThread(Thread):
    def __init__(self, number):
        super().__init__()
        self.number = number

    def run(self):
        self.factors = list(factorize(self.number))

def slow_systemcall():
    select.select([], [], [], 0.1)

def compute_helicopter_location(index):
    pass

class item38:
    def __init__(self):
        print('-----------------\n'
              'Item 38\n'
              '-----------------\n')

        how_many = 10**5
        counter = Counter()
        run_threads(worker, how_many, counter)
        print('Counter should be %d, found %d' % (5 * how_many, counter.count))

        counter = LockingCounter()
        run_threads(worker, how_many, counter)
        print('Counter should be %d, found %d' % (5 * how_many, counter.count))



class Counter(object):
    def __init__(self):
        self.count = 0

    def increment(self, offset):
        self.count += offset

def worker(sensor_index, how_many, counter):
    BARRIER.wait()
    for _ in range(how_many):
        counter.increment(1)

BARRIER = Barrier(5)
def run_threads(func, how_many, counter):
    threads = []
    for i in range(5):
        args = (i, how_many, counter)
        thread = Thread(target=func, args=args)
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()

class LockingCounter(object):
    def __init__(self):
        self.lock = Lock()
        self.count = 0

    def increment(self, offset):
        with self.lock:
            self.count += offset

class item39:
    """Items 39: Use Queue to Coordinate work between threads"""
    def __init__(self):
        print('-' * (len(self.__doc__) + 1), '\n',
              self.__doc__, '\n',
              '-'*(len(self.__doc__) + 1), '\n',
              sep='')

        def download(item):
            return item

        def resize(item):
            return item

        def upload(item):
            return item

        download_queue = MyQueue()
        resize_queue = MyQueue()
        upload_queue = MyQueue()
        done_queue = MyQueue()
        threads = [
            Worker(download, download_queue, resize_queue),
            Worker(resize, resize_queue, upload_queue),
            Worker(upload, upload_queue, done_queue),
        ]

        # for thread in threads:
        #     thread.start()
        # for _ in range(1):
        #     download_queue.put(object())
        #
        # while len(done_queue.items) < 1:
        #     sleep(0.1)
        # for thread in threads:
        #     thread.join()
        #
        # processed = len(done_queue.items)
        # polled = sum(t.polled_count for t in threads)
        # print('Processed', processed, 'items after polling',
        #       polled, 'times')

        testBuiltInQueue1()
        testBuiltInQueue2()
        testBuiltInQueue3()

        download_queue = ClosableQueue()
        resize_queue = ClosableQueue()
        upload_queue = ClosableQueue()
        done_queue = ClosableQueue()
        threads = [
            StoppableWorker(download, download_queue, resize_queue),
            StoppableWorker(resize, resize_queue, upload_queue),
            StoppableWorker(upload, upload_queue, done_queue)
        ]

        for thread in threads:
            thread.start()

        for _ in range(1000):
            download_queue.put(object())
        download_queue.close()

        download_queue.join()
        resize_queue.close()
        resize_queue.join()
        upload_queue.close()
        upload_queue.join()
        print(done_queue.qsize(), 'items finished')




from collections import deque

class MyQueue:
    def __init__(self):
        self.items = deque()
        self.lock = Lock()

    def put(self, item):
        with self.lock:
            self.items.append(item)

    def get(self):
        with self.lock:
            return self.items.popleft()

class Worker(Thread):
    def __init__(self, func, in_queue, out_queue):
        super().__init__()
        self.func = func
        self.in_queue = in_queue
        self.out_queue = out_queue
        self.polled_count = 0
        self.work_done = 0

    def run(self):
        while True:
            self.polled_count += 1
            try:
                item = self.in_queue.get()
            except IndexError:
                sleep(0.01)
            else:
                result = self.func(item)
                self.out_queue.put(result)
                self.work_done += 1

class testBuiltInQueue1(Queue):
    def __init__(self):
        super().__init__()
        thread = Thread(target=self.consumer)
        thread.start()

        print('Producer putting')
        self.put(object())
        print('Before join')
        thread.join()
        print('Producer done')

    def consumer(self):
        print('Consumer waiting')
        self.get()
        print('Consumer done')

class testBuiltInQueue2(Queue):
    def __init__(self):
        super().__init__(1)
        thread = Thread(target=self.consumer)
        thread.start()

        self.put(object())
        print('Put 1')
        self.put(object())
        print('Put 2')
        thread.join()
        print('Producer done')

    def consumer(self):
        time.sleep(0.1)
        self.get()
        print('Consumer got 1')
        self.get()
        print('Consumer got 2')

class testBuiltInQueue3(Queue):
    def __init__(self):
        super().__init__()
        thread = Thread(target=self.consumer).start()

        self.put(object())
        print('Producer waiting')
        self.join()
        print('Producer done')


    def consumer(self):
        print('Consumer waiting')
        work = self.get()
        print('Consumer working')
        print('Consumer done')
        self.task_done()


class ClosableQueue(Queue):
    SENTINEL = object()

    def close(self):
        self.put(self.SENTINEL)

    def __iter__(self):
        while True:
            item = self.get()
            try:
                if item is self.SENTINEL:
                    return
                yield item
            finally:
                self.task_done()

class StoppableWorker(Thread):
    def __init__(self, func, in_queue, out_queue):
        super().__init__()
        self.func = func
        self.in_queue = in_queue
        self.out_queue = out_queue
        self.polled_count = 0
        self.work_done = 0

    def run(self):
        for item in self.in_queue:
            result = self.func(item)
            self.out_queue.put(result)

class item40:
    """Items 40: Consider Coroutines to run many functions concurrently"""
    def __init__(self):
        print('-' * (len(self.__doc__) + 1), '\n',
              self.__doc__, '\n',
              '-'*(len(self.__doc__) + 1), '\n',
              sep='')

        CoroutineTest()


class CoroutineTest:
    def __init__(self):
        it = self.mycoroutine()
        next(it)
        it.send('First')
        it.send('Second')

        it = self.minimize()
        next(it)
        print(it.send(10))
        print(it.send(4))
        print(it.send(22))
        print(it.send(-1))

    def mycoroutine(self):
        while True:
            received = yield
            print('Received:', received)

    def minimize(self):
        current = yield
        while True:
            value = yield current
            current = min(value, current)

class GameOfLife:
    def __init__(self):
        self.ALIVE = '*'
        self.EMPTY = '-'
        self.TICK = object()

        # Retrieve status of neighbors
        self.Query = namedtuple('Query', ('y', 'x'))
        self.Transition = namedtuple('Transition', ('y', 'x', 'state'))
        self.count_neighbor_test()

        # Test Game
        it = self.step_cell(10, 5)
        q0 = next(it)
        print('Me:        ', q0)
        q1 = it.send(self.ALIVE)
        print('Q1:        ', q1)
        print('...')
        q2 = it.send(self.ALIVE)
        q3 = it.send(self.ALIVE)
        q4 = it.send(self.ALIVE)
        q5 = it.send(self.ALIVE)
        q6 = it.send(self.EMPTY)
        q7 = it.send(self.EMPTY)
        q8 = it.send(self.EMPTY)

        t1 = it.send(self.EMPTY)
        print('Outcome: ', t1)

        grid = self.Grid(5, 9)
        grid.assign(0, 3, self.ALIVE)
        grid.assign(1, 4, self.ALIVE)
        grid.assign(2, 2, self.ALIVE)
        grid.assign(2, 3, self.ALIVE)
        grid.assign(2, 4, self.ALIVE)
        print(grid)

        columns = self.ColumnPrinter()
        sim = self.simulate(grid.height, grid.width)
        for i in range(5):
            columns.append(str(grid))
            grid = self.live_a_generation(grid, sim)

        print(columns)

    def count_neighbor_test(self):
        it = self.count_neighbors(10, 5)
        q1 = next(it)
        print('First yield: ', q1)
        q2 = it.send(self.ALIVE)
        print('Second yield:', q2)
        q3 = it.send(self.ALIVE)

        print('...')
        q4 = it.send(self.EMPTY)
        q5 = it.send(self.EMPTY)
        q6 = it.send(self.EMPTY)
        q7 = it.send(self.EMPTY)
        q8 = it.send(self.EMPTY)

        # print('Third yield:', q3)
        # q4 = it.send(self.ALIVE)
        # print('Fourth yield:', q4)
        # q5 = it.send(self.ALIVE)
        # print('Fifth yield:', q5)
        # q6 = it.send(self.ALIVE)
        # print('Sixth yield:', q6)
        # q7 = it.send(self.ALIVE)
        # print('Seventh yield:', q7)
        # q8 = it.send(self.ALIVE)
        #print('Eighth yield:', q8)
        # q9 = it.send(self.ALIVE)
        # print('Third yield:', q9)
        try:
            count = it.send(self.EMPTY)
        except StopIteration as e:
            print('Count: ', e.value)

    def count_neighbors(self, y, x):
        n_ = yield self.Query(y + 1, x + 0)
        ne = yield self.Query(y + 1, x + 1)
        e_ = yield self.Query(y, x + 1)
        se = yield self.Query(y - 1, x + 1)
        s_ = yield self.Query(y - 1, x)
        sw = yield self.Query(y - 1, x - 1)
        w_ = yield self.Query(y, x - 1)
        nw = yield self.Query(y + 1, x - 1)

        neighbor_states = [n_, ne, e_, se, s_, sw, w_, nw]
        count = 0
        for state in neighbor_states:
            if state == self.ALIVE:
                count += 1
        return count

    def game_logic(self, state, neighbors):
        if state == self.ALIVE:
            if neighbors < 2:
                return self.EMPTY
            elif neighbors > 3:
                return self.EMPTY

        else:
            if neighbors == 3:
                return self.ALIVE
        return state

    def step_cell(self, y, x):
        state = yield self.Query(y, x)
        neighbors = yield from self.count_neighbors(y, x)
        next_state = self.game_logic(state, neighbors)
        yield self.Transition(y, x, next_state)

    def simulate(self, height, width):
        while True:
            for y in range(height):
                for x in range(width):
                    yield from self.step_cell(y, x)
            yield self.TICK

    class Grid(object):
        def __init__(self, height, width):
            EMPTY = '-'
            self.height = height
            self.width = width
            self.rows = []
            for _ in range(self.height):
                self.rows.append([EMPTY]*self.width)

        def __str__(self):
            output = ''
            for row in self.rows:
                for cell in row:
                    output += cell
                output += '\n'
            return output

        def query(self, y, x):
            return self.rows[y % self.height][x % self.width]

        def assign(self, y, x, state):
            self.rows[y % self.height][x % self.width] = state

    def live_a_generation(self, grid, sim):
        progeny = self.Grid(grid.height, grid.width)
        item = next(sim)
        while item is not self.TICK:
            if isinstance(item, self.Query):
                state = grid.query(item.y, item.x)
                item = sim.send(state)
            else:  # Must be a Transition
                progeny.assign(item.y, item.x, item.state)
                item = next(sim)
        return progeny


    class ColumnPrinter(object):
        def __init__(self):
            self.columns = []

        def append(self, data):
            self.columns.append(data)

        def __str__(self):
            row_count = 1
            for data in self.columns:
                row_count = max(row_count, len(data.splitlines()) + 1)
            rows = [''] * row_count
            for j in range(row_count):
                for i, data in enumerate(self.columns):
                    line = data.splitlines()[max(0, j - 1)]
                    if j == 0:
                        padding = ' ' * (len(line) // 2)
                        rows[j] += padding + str(i) + padding
                    else:
                        rows[j] += line
                    if (i + 1) < len(self.columns):
                        rows[j] += ' | '
            return '\n'.join(rows)


if __name__ == '__main__':
    sol = item36()
    sol = item37()
    sol = item38()
    sol = item39()
    sol = item40()
    sol = GameOfLife()