__author__ = 'stephenosullivan'

import subprocess, time, os
from threading import Thread
from threading import Barrier
from threading import Lock
import select
from time import sleep
from queue import Queue


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

        for thread in threads:
            thread.start()
        for _ in range(1000):
            download_queue.put(object())

        while len(done_queue.items) < 1000:
            sleep(0.1)

        processed = len(done_queue.items)
        polled = sum(t.polled_count for t in threads)
        print('Processed', processed, 'items after polling',
              polled, 'times')

        testBuiltInQueue1()
        testBuiltInQueue2()


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




if __name__ == '__main__':
    sol = item36()
    sol = item37()
    sol = item38()
    sol = item39()