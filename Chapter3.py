__author__ = 'stephenosullivan'

import os
import threading
from collections import defaultdict


class Item22_SimpleGradebook(object):
    """
    Prefer classes over bookkeeping with dictionaries and tuples
    """
    def __init__(self):
        self._grades = {}

    def add_student(self, name):
        self._grades[name] = []

    def report_grade(self, name, score):
        self._grades[name].append(score)

    def average_grad(self, name):
        grades = self._grades[name]
        return sum(grades) /len(grades)

# Extend functionality to store grades by subject
# Create dict of dicts
class Item22_BySubjectGradebook(object):
    def __init__(self):
        self._grades = {}

    def add_student(self, name):
        self._grades[name] = {}

    def report_grade(self, name, subject, grade):
        by_subject = self._grades[name]
        grade_list = by_subject.setdefault(subject, [])
        grade_list.append(grade)

    def average_grade(self, name):
        by_subject = self._grades[name]
        total, count = 0, 0
        for grades in by_subject.values():
            total += sum(grades)
            count += len(grades)
        return total /count

class Item22_WeightedGradebook(object):
    def __init__(self):
        self._grades = {}

    def add_student(self, name):
        self._grades[name] = {}

    def report_grade(self, name, subject, grade, weight):
        by_subject = self._grades[name]
        grade_list = by_subject.setdefault(subject, [])
        grade_list.append(grade)

    def average_grade(self, name):
        by_subject = self._grades[name]
        total, count = 0, 0
        for grades in by_subject.values():
            total += sum(grades)
            count += len(grades)
        return total /count

class Item22_Subject(object):
    def __init__(self):
        from collections import namedtuple
        self._grades = []
        self.Grade = namedtuple('Grade', ('score', 'weight'))

    def report_grade(self, score, weight):
        self._grades.append(self.Grade(score, weight))

    def average_grade(self):
        total, total_weight = 0, 0
        for grade in self._grades:
            total += grade.score * grade.weight
            total_weight += grade.weight
        return total / total_weight

class Item22_Student(object):
    def __init__(self):
        self._subjects = {}

    def subject(self, name):
        return self._subjects.setdefault(name, Item22_Subject())

    def average_grade(self):
        total, count = 0, 0
        for subject in self._subjects.values():
            total += subject.average_grade()
            count += 1
        return total / count


class Item22_GradeBook(object):
    def __init__(self):
        self._students = {}

    def student(self, name):
        return self._students.setdefault(name, Item22_Student())

class Item22:
    def __init__(self):
        book = Item22_GradeBook()
        albert = book.student('Albert Einstein')
        math = albert.subject('Math')
        math.report_grade(80, 0.10)
        math.report_grade(75, 0.15)
        print(albert.average_grade())

class Item23:
    """
    Accept functions for simple interfaces instead of classes
    """
    def __init__(self):

        names = ['Socrates', 'Archimedes', 'Plato', 'Aristotle']
        names.sort(key=lambda x: len(x))
        print(names)

        current = {'green': 12, 'blue': 3}

        increments = [('red', 5), ('blue', 17), ('orange', 9)]
        result = defaultdict(self.log_missing, current)
        print('Before:', dict(result))
        for key, amount in increments:
            result[key] += amount
        print('After: ', dict(result))

        counter = CountMissing()
        result = defaultdict(counter.missing, current)

        for key, amount in increments:
            result[key] += amount
        assert counter.added == 2

        counter = BetterCountMissing()
        counter()
        assert callable(counter)

        counter = BetterCountMissing()
        result = defaultdict(counter, current)
        for key, amount in increments:
            result[key] += amount
        assert counter.added == 2
        print(result)

    def log_missing(self):
        """
        log each time the key is missing
        :return:
        """
        print('Key added')
        return 0

    def increment_with_report(self, current, increments):
        added_count = 0

        def missing():
            nonlocal added_count
            added_count += 1
            return 0

        result = defaultdict(missing(), current)
        for key, amount in increments:
            result[key] += amount

        return result, added_count

class CountMissing(object):
    def __init__(self):
        self.added = 0

    def missing(self):
        self.added += 1
        return 0

class BetterCountMissing(object):
    def __init__(self):
        self.added = 0

    def __call__(self):
        self.added += 1
        return 0

class Item24:
    """
    Use @classmethod Polymorphism to construct objects generically
    """
    def __init__(self):
        from tempfile import TemporaryDirectory

        def write_test_files(tmpdir):
            # Write files in tmpdir
            filenames = [os.path.join(tmpdir, 'step%d.txt' % i) for i in range(10)]
            for file in filenames:
                f = open(file, 'w')
                f.write('This is a sentence\n')
                #f = open(file)
                #print(f.readline())

        with TemporaryDirectory() as tmpdir:
            write_test_files(tmpdir)
            result = self.mapreduce(tmpdir)

        print('There are', result, 'lines')



    # List the contents of a directory and construct a PathInputData
    # instance for each file it contains
    def generate_inputs(self, data_dir):
        for name in os.listdir(data_dir):
            yield PathInputData(os.path.join(data_dir, name))

    def create_workers(self, input_list):
        workers = []
        for input_data in input_list:
            workers.append(LineCountWorker(input_data))
        return workers

    def execute(self, workers):
        threads = [threading.Thread(target=w.map) for w in workers]
        for thread in threads: thread.start()
        for thread in threads: thread.join()

        first, rest = workers[0], workers[1:]

        for worker in rest:
            first.reduce(worker)
        return first.result

    def mapreduce(self, data_dir):
        inputs = self.generate_inputs(data_dir)
        workers = self.create_workers(inputs)
        return self.execute(workers)




class InputData(object):
    def read(self):
        raise NotImplementedError

class PathInputData(InputData):
    def __init__(self, path):
        super().__init__()
        self.path = path

    def read(self):
        return open(self.path).read()

class Worker(object):
    def __init__(self, input_data):
        self.input_data = input_data
        self.result = None

    def map(self):
        raise NotImplementedError

    def reduce(self, other):
        raise NotImplementedError

class LineCountWorker(Worker):
    def map(self):
        data = self.input_data.read()
        self.result = data.count('\n')

    def reduce(self, other):
        self.result += other.result


class GenericInputData(object):
    def read(self):
        raise NotImplementedError

    @classmethod
    def generate_inputs(cls, config):
        raise NotImplementedError

class PathInputDataGeneric(GenericInputData):
    def __init__(self, path):
        super().__init__()
        self.path = path

    def read(self):
        return open(self.path).read()

    @classmethod
    def generate_inputs(cls, config):
        data_dir = config['data_dir']
        for name in os.listdir(data_dir):
            yield cls(os.path.join(data_dir, name))

class GenericWorker(object):
    def __init__(self, input_data):
    self.input_data = input_data
    self.result = None

    def map(self):
        raise NotImplementedError

    def reduce(self, other):
        raise NotImplementedError

    @classmethod
    def create_workers(cls, input_class, config):
        workers = []
        for input_data in input_class.generate_inputs(config):
            workers.append(cls(input_data))
        return workers

class LineCountWorker(Worker):
    def map(self):
        data = self.input_data.read()
        self.result = data.count('\n')

    def reduce(self, other):
        self.result += other.result

if __name__ == '__main__':
    sol = Item22()
    sol = Item23()
    sol = Item24()