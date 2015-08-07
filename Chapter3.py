__author__ = 'stephenosullivan'

import os
import threading
from collections import defaultdict
import json


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
        return sum(grades) / len(grades)


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
        return total / count


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
        return total / count


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
                # f = open(file)
                # print(f.readline())

        with TemporaryDirectory() as tmpdir:
            write_test_files(tmpdir)
            result = self.mapreduce(tmpdir)

        print('There are', result, 'lines')

        with TemporaryDirectory() as tmpdir:
            write_test_files(tmpdir)
            config = {'data_dir': tmpdir}
            result = self.mapreduce2(LineCountWorker2, PathInputDataGeneric, config)

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

    def mapreduce2(self, worker_class, input_class, config):
        workers = worker_class.create_workers(input_class, config)
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


class LineCountWorker2(GenericWorker):
    def map(self):
        data = self.input_data.read()
        self.result = data.count('\n')

    def reduce(self, other):
        self.result += other.result


class Item25:
    """
    Initialize parent classes with super
    """

    def __init__(self):
        a = MyChildClass()
        print(MyChildClass().value)

        assert Explicit(10).value == Implicit(10).value


class MyBaseClass(object):
    def __init__(self, value):
        self.value = value


class MyChildClass(MyBaseClass):
    def __init__(self):
        MyBaseClass.__init__(self, 5)


class Explicit(MyBaseClass):
    def __init__(self, value):
        super(__class__, self).__init__(value * 2)


class Implicit(MyBaseClass):
    def __init__(self, value):
        super().__init__(value * 2)


class Item26:
    """
    Use Multiple Inheritance Only for Mix-in Utility Classes

    Mix-in classes don't define their own instance attributes nor require their
    __init__ constructor to be called
    """

    def __init__(self):
        tree = BinaryTree(10, left=BinaryTree(7, right=BinaryTree(9)), right=BinaryTree(13, left=BinaryTree(11)))
        print('Tree to dict', tree.to_dict())

        root = BinaryTreeWithParent(10)
        root.left = BinaryTreeWithParent(7, parent=root)
        root.left.right = BinaryTreeWithParent(9, parent=root.left)

        print('With parent', root.to_dict())

        my_tree = NamedSubTree('foobar', root.left.right)
        print(my_tree.to_dict())

        serialized = """{ "switch": {"ports": 5, "speed": 1e9}, "machines": [{"cores": 8, "ram": 32e9, "disk": 5e12}, {"cores": 4, "ram": 16e9, "disk": 1e12}, {"cores": 2, "ram": 4e9, "disk": 500e9}]}"""

        deserialized = DatacenterRack.from_json(serialized)
        roundtrip = deserialized.to_json()
        assert json.loads(serialized) == json.loads(roundtrip)

        print(json.loads(serialized))


# Convert an object from its in-memory representation to a dictionary that's
# ready for serialization
class ToDictMixin(object):
    def to_dict(self):
        return self._traverse_dict(self.__dict__)

    def _traverse_dict(self, instance_dict):
        output = {}
        for key, value in instance_dict.items():
            output[key] = self._traverse(key, value)
        return output

    def _traverse(self, key, value):
        if isinstance(value, ToDictMixin):
            return value.to_dict()
        elif isinstance(value, dict):
            return self._traverse_dict(value)
        elif isinstance(value, list):
            return [self._traverse(key, i) for i in value]
        elif hasattr(value, '__dict__'):
            return self._traverse_dict(value.__dict__)
        else:
            return value


class BinaryTree(ToDictMixin):
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


class BinaryTreeWithParent(BinaryTree):
    def __init__(self, value, left=None, right=None, parent=None):
        super().__init__(value, left=left, right=right)
        self.parent = parent

    def _traverse(self, key, value):
        if isinstance(value, BinaryTreeWithParent) and key == 'parent':
            return value.value
        else:
            return super()._traverse(key, value)


class NamedSubTree(ToDictMixin):
    def __init__(self, name, tree_with_parent):
        self.name = name
        self.tree_with_parent = tree_with_parent


class JsonMixin(object):
    @classmethod
    def from_json(cls, data):
        kwargs = json.loads(data)
        return cls(**kwargs)

    def to_json(self):
        return json.dumps(self.to_dict())


class DatacenterRack(ToDictMixin, JsonMixin):
    def __init__(self, switch=None, machines=None):
        self.switch = Switch(**switch)
        self.machines = [Machine(**kwargs) for kwargs in machines]

class Switch(ToDictMixin, JsonMixin):
    def __init__(self, ports=None, speed=None):
        self.ports = ports
        self.speed = speed

class Machine(ToDictMixin, JsonMixin):
    def __init__(self, cores=None, ram=None, disk=None):
        self.cores = cores
        self.ram = ram
        self.disk = disk


class Item27:
    """
    Prefer Public Attributes over Private Ones
    """

    def __init__(self):
        foo = MyObject()
        assert foo.public_field == 5
        assert foo.get_private_field() == 10
        # print(foo.__private_field)
        bar = MyOtherObject()
        print(bar.get_private_field_of_instance(bar))
        print(MyOtherObject.get_private_field_of_instance(bar))

        baz = MyChildObject()
        # baz.get_private_field()   # Can't access

        # Try to cheat!
        assert baz._MyParentObject__private_field == 71

        print(baz.__dict__)

        a = Child()
        print(a.get(), 'and', a._value, 'are different')


class MyObject(object):
    def __init__(self):
        self.public_field = 5
        self.__private_field = 10

    def get_private_field(self):
        return self.__private_field


# Class methods have access to private attributes
class MyOtherObject():
    def __init__(self):
        self.__private_field = 71

    @classmethod
    def get_private_field_of_instance(cls, instance):
        return instance.__private_field


# A subclass cannot access it's parents private methods
class MyParentObject():
    def __init__(self):
        self.__private_field = 71


class MyChildObject(MyParentObject):
    def get_private_field(self):
        return self.__private_field


# Use private members to avoid naming conflicts

class ApiClass():
    def __init__(self):
        self.__value = 7

    def get(self):
        return self.__value


class Child(ApiClass):
    def __init__(self):
        super().__init__()
        self._value = 'hello'


class Item28:
    """
    Inherit from collections.abc for Custom Container Types
    """

    def __init__(self):
        foo = FrequencyList(['a', 'b', 'a', 'c', 'b', 'a', 'd'])
        print('Length is', len(foo))
        foo.pop()
        print('After pop:', repr(foo))
        print('Frequency', foo.frequency())

        tree = IndexableNode(10, left=IndexableNode(5, left=IndexableNode(2),
                                                    right=IndexableNode(6, right=IndexableNode(7))),
                             right=IndexableNode(15, left=IndexableNode(11)))

        print('LRR =', tree.left.right.right.value)
        print('Index 0 =', tree[0])
        print('Index 1 =', tree[1])
        print('Index 6 =', tree[6])
        print(tree._search(0, None))
        print('11 in tree', 11 in tree)
        print('17 in tree', 17 in tree)
        print('Tree is', list(tree))

        print(tree[6])
        # len(tree)

        tree = SequenceNode(10, left=SequenceNode(5, left=SequenceNode(2),
                                                  right=SequenceNode(6, right=SequenceNode(7))),
                            right=SequenceNode(15, left=SequenceNode(11)))

        print('Sequence Tree is ', list(tree))
        print('Tree has %d nodes' % len(tree))
        # print('Index 0', tree[0])


        tree = BetterNode(10, left=BetterNode(5, left=BetterNode(2),
                                              right=BetterNode(6, right=BetterNode(7))),
                          right=BetterNode(15, left=BetterNode(11)))

        print('index 7:', tree.index(7))
        print('count of 10', tree.count(10))


# Attempt custom list which can count the freq of its members
class FrequencyList(list):
    def __init__(self, members):
        super().__init__(members)

    def frequency(self):
        counts = {}
        for item in self:
            counts.setdefault(item, 0)
            counts[item] += 1
        return counts


class BinaryNode:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


class IndexableNode(BinaryNode):
    def _search(self, count, index):
        found = None
        if self.left:
            found, count = self.left._search(count, index)
        if not found and count == index:
            found = self
        else:
            count += 1
        if not found and self.right:
            found, count = self.right._search(count, index)
        # print( count, index)
        return found, count

        # Iterative solution
        # node = self
        # nodes_to_traverse = []
        # print('b', index)
        # if index is None:
        #     print('None')
        #     ind = -1
        # else:
        #     ind = index
        # while nodes_to_traverse or node.right or node.left:
        #     while node.left:
        #         nodes_to_traverse.append(node)
        #         node = node.left
        #
        #     if ind == 0:
        #         return node, count
        #     else:
        #         ind -= 1
        #         count += 1
        #
        #     while node.right is None:
        #         node = nodes_to_traverse.pop()
        #         if ind == 0:
        #             return node, count
        #         else:
        #             ind -= 1
        #             count += 1
        #
        #     if node.right:
        #         node = node.right
        #
        # return None, count

    def __getitem__(self, index):
        found, _ = self._search(0, index)
        if not found:
            raise IndexError('Index out of range')
        return found.value


class SequenceNode(IndexableNode):
    def __len__(self):
        _, count = self._search(0, None)
        return count


from collections.abc import Sequence


class BetterNode(SequenceNode, Sequence):
    pass


if __name__ == '__main__':
    sol = Item22()
    sol = Item23()
    sol = Item24()
    sol = Item25()
    sol = Item26()
    sol = Item27()
    sol = Item28()
