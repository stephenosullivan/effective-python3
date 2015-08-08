__author__ = 'stephenosullivan'


from datetime import *

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
        return ('Bucket(max_quota=%d, quota_consumed=%d)' % (self.max_quota, self.quota_consumed))

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

if __name__ == '__main__':
    sol = Item29()
    sol = Item30()
