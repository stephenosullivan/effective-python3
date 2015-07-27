__author__ = 'stephenosullivan'

class item14:
    def divide(self, a, b):
        try:
            return a/b
        except ZeroDivisionError:
            return None

if __name__ == "__main__":
    sol14 = item14()
    result1 = sol14.divide(10,3)
    result2 = sol14.divide(10,0)
    if not result1 or not result2:
        print("Cannot divide by zero")
