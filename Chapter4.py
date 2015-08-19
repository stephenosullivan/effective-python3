__author__ = 'stephenosullivan'


from datetime import *
import weakref

class Item29:
    """
    Use plain attributes instead of get and set methods
    """
    def __init__(self):
        r2 = VoltageResistance(1e3)
        print('Before: %5r amps' % r2.current)
        r2.voltage = 10
        print('After: %5r amps' % r2.current)

        r3 = BoundedResistance(1e3)
        #r3.ohms = 0        Error!!
        #BoundedResistance(-5)

        r4 = FixedResistance(1e3)
        #r4.ohms = 2e3       # Attribute Error


class Resistor(object):
    def __init__(self, ohms):
        self.ohms = ohms
        self.voltage = 0
        self.current = 0


class VoltageResistance(Resistor):
    def __init__(self, ohms):
        super().__init__(ohms)
        self._voltage = 0

    @property
    def voltage(self):
        return self._voltage

    @voltage.setter
    def voltage(self, voltage):
        self._voltage = voltage
        self.current = self._voltage / self.ohms

# Class to check that all resistance values are above zero
class BoundedResistance(Resistor):
    def __init__(self, ohms):
        super().__init__(ohms)

    @property
    def ohms(self):
        return self._ohms

    @ohms.setter
    def ohms(self, ohms):
        if ohms <= 0:
            raise ValueError('%f ohms must be > 0' % ohms)
        self._ohms = ohms


# Make attributes from parent class immutable
class FixedResistance(Resistor):
    def __init__(self, ohms):
        super().__init__(ohms)

    @property
    def ohms(self):
        return self._ohms

    @ohms.setter
    def ohms(self, ohms):
        if hasattr(self, '_ohms'):
            raise AttributeError("Can't set attribute")
        self._ohms = ohms

class Item30:
    """
    Consider @property instead of refactoring attributes
    """
    def __init__(self):
        bucket = Bucket(60)
        fill(bucket, 100)
        print(bucket)

        if deduct(bucket, 99):
            print('Had 99 quota')
        else:
            print('Not enough for 99 quota')
        print(bucket)

        if deduct(bucket, 3):
            print('Had 3 quota')
        else:
            print('Not enough for 3 quota')
        print(bucket)

        bucketv2 = BucketV2(60)
        fill(bucketv2, 100)
        print(bucketv2)

        if deduct(bucketv2, 99):
            print('Had 99 quota')
        else:
            print('Not enough for 99 quota')
        print(bucketv2)

        if deduct(bucketv2, 3):
            print('Had 3 quota')
        else:
            print('Not enough for 3 quota')
        print(bucketv2)

class Bucket(object):
    def __init__(self, period):
        self.period_delta = timedelta(seconds=period)
        self.reset_time = datetime.now()
        self.quota = 0

    def __repr__(self):
        return 'Bucket(quota=%d)' % self.quota

def fill(bucket, amount):
    now = datetime.now()
    if now - bucket.reset_time > bucket.period_delta:
        bucket.quota = 0
        bucket.reset_time = now
    bucket.quota += amount

def deduct(bucket, amount):
    now = datetime.now()
    if now - bucket.reset_time > bucket.period_delta:
        return False
    if bucket.quota - amount < 0:
        return False
    bucket.quota -= amount
    return True

class BucketV2:
    def __init__(self, period):
        self.period_delta = timedelta(seconds=period)
        self.reset_time = datetime.now()
        self.max_quota = 0
        self.quota_consumed = 0

    def __repr__(self):
        return 'Bucket(max_quota=%d, quota_consumed=%d)' % (self.max_quota, self.quota_consumed)

    @property
    def quota(self):
        return self.max_quota - self.quota_consumed

    @quota.setter
    def quota(self, amount):
        delta = self.max_quota - amount
        if amount == 0:
            self.quota_consumed = 0
            self.max_quota = 0
        elif delta < 0:
            assert self.quota_consumed == 0
            self.max_quota = amount
        else:
            assert self.max_quota >= self.quota_consumed
            self.quota_consumed += delta


class Item31:
    """
    Use descriptors for reusable @property methods
    """
    def __init__(self):
        galileo = Homework()
        galileo.grade = 95

        exam = Exam()
        exam.writing_grade = 40

        first_exam = Examv2()
        first_exam.writing_grade = 82
        second_exam = Examv2()
        second_exam.writing_grade = 75
        print('First ', first_exam.writing_grade, 'is right')
        print('First ', second_exam.writing_grade, 'is right')




# Validate that the grade received is a percentage
class Homework(object):
    def __init__(self):
        self._grade = 0

    @property
    def grade(self):
        return self._grade

    @grade.setter
    def grade(self, value):
        if not (0 <= value <= 100):
            raise ValueError('Grade must be between zero and 100')
        self._grade = value

#Grade for exam
class Exam(object):
    def __init__(self):
        # multiple parts of grade
        self._writing_grade = 0
        self._math_grade = 0

    @staticmethod
    def _check_grade(value):
        if not (0 <= value <= 100):
            raise ValueError('Grade must be between 0 and 100')

    @property
    def writing_grade(self):
        return self._writing_grade

    @writing_grade.setter
    def writing_grade(self, value):
        self._check_grade(value)
        self._writing_grade = value

    @property
    def math_grade(self):
        return self._math_grade

    @math_grade.setter
    def math_grade(self, value):
        self._check_grade(value)
        self._math_grade = value


# Use descriptors instead
# Save each instance in a dict
class Grade:
    def __init__(self):
        #self._values = {}
        self._values = weakref.WeakKeyDictionary()

    def __get__(self, instance, instance_type):
        if instance is None:
            return self
        return self._values.get(instance, 0)

    def __set__(self, instance, value):
        if not (0 <= value <= 100):
            raise ValueError('Grade must be between 0 and 100')
        self._values[instance] = value



class Examv2:
    math_grade = Grade()
    writing_grade = Grade()
    science_grade = Grade()

class Item32:
    """
    Use __getattr__, __getattribute__, and __setattr__ for Lazy Attributes
    """
    def __init__(self):
        data = LazyDB()
        print('Before:', data.__dict__)
        print('foo:', data.foo)
        print('After', data.__dict__)

        data = LoggingLazyDB()
        print('exists:', data.exists)
        print('foo:   ', data.foo)
        print('foo:   ', data.foo)

        data = ValidatingDB()
        print('exists:', data.exists)
        print('foo:   ', data.foo)
        print('foo,   ', data.foo)

        data = MissingPropertyDB()
        #data.bad_name

        data = LoggingLazyDB()
        print('Before:       ', data.__dict__)
        print('foo exists:   ', hasattr(data, 'foo'))
        print('After:        ', data.__dict__)
        print('foo exists:   ', hasattr(data, 'foo'))

        data = ValidatingDB()
        print('foo exists: ', hasattr(data, 'foo'))
        print('foo exists: ', hasattr(data, 'foo'))

        data = LoggingSavingDB()
        print('Before:    ', data.__dict__)
        data.foo = 5
        print('After:     ', data.__dict__)
        data.foo = 7
        print('Finally:   ', data.__dict__)

        data = DictionaryDB({'foo': 3})
        print(data.foo)

class LazyDB:
    def __init__(self):
        self.exists = 5

    def __getattr__(self, name):
        value = 'Value for %s' % name
        setattr(self, name, value)
        return value

class LoggingLazyDB(LazyDB):
    def __getattr__(self, name):
        print('Called __getattr__(%s)' % name)
        return super().__getattr__(name)

class ValidatingDB:
    def __init__(self):
        self.exists = 5

    def __getattribute__(self, name):
        print('Called __getAttribute__(%s)' % name)
        try:
            return super().__getattribute__(name)
        except AttributeError:
            value = 'Value for %s' % name
            setattr(self, name, value)
            return value


class MissingPropertyDB:
    def __getattr__(self, name):
        if name == 'bad_name':
            raise AttributeError('%s is missing' % name)

class SavingDB:
    def __setattr__(self, name, value):
        pass
        super().__setattr__(name, value)

class LoggingSavingDB(SavingDB):
    def __setattr__(self, name, value):
        print('Called __setattr__(%s, %r)' % (name, value))
        super().__setattr__(name, value)

class BrokenDict:
    def __init__(self, data):
        self._data = {}

    def __getattribute__(self, name):
        print('Called __getattribute__(%s)' % name)
        return self._data[name]

class DictionaryDB:
    def __init__(self, data):
        self._data = data

    def __getattribute__(self, item):
        data_dict = super().__getattribute__('_data')
        return data_dict[item]


class Item33:
    """
    Validate subclasses with Metaclasses
    """
    def __init__(self):
        print("Item 23 \n"
              "-------")
        a = MyClass()
        b = a
        print(a.stuff)
        print(MyClass)

        print('Before class')
        #print(Line.interior_angles())





class Meta(type):
    def __new__(meta, name, bases, class_dict):
        orig_print = __builtins__.print
        print((meta, name, bases, class_dict))
        print(orig_print)
        return type.__new__(meta, name, bases, class_dict)

class MyClass(object, metaclass=Meta):
    def __init__(self):
        print('init')

    stuff = 123

    def foo(self):
        pass

class ValidatePolygon(type):
    def __new__(meta, name, bases, class_dict):
        print(bases, 'bases')
        if bases != (object, ):
            if class_dict['sides'] < 3:
                raise ValueError('Polygons need 3+ sides')
        return type.__new__(meta, name, bases, class_dict)

class Polygon(object, metaclass=ValidatePolygon):
    sides = None

    @classmethod
    def interior_angles(cls):
        return (cls.sides - 2) * 180

class Triangle(Polygon):
    sides = 3

class Line(Polygon):
     print('Before sides')
     sides = 4
#     print('After sides')
#     print('After class')


if __name__ == '__main__':
    sol = Item29()
    sol = Item30()
    sol = Item31()
    sol = Item32()
    sol = Item33()