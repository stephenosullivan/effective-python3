__author__ = 'stephenosullivan'

class Item29:
    """
    Use plain attributes instead of get and set methods
    """
    def __init__(self):
        r2 = VoltageResistance(1e3)
        print('Before: %5r amps' % r2.current)
        r2.voltage = 10
        print('After: %5r amps' % r2.current)


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


if __name__ == '__main__':
    sol = Item29()
