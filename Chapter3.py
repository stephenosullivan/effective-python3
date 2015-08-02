__author__ = 'stephenosullivan'


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


if __name__ == '__main__':
    sol = Item22()
