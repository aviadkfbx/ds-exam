# Low memory problem
#
# Assume a finite sequence of objects with an unknown length. S=a_1, a_2, ...
# There exists 1 object with value ai=a' that appears more than half of the time:
# |{i|a_i=a'}| / N > N / 2
# Our goal is to find the value a' using the following constraints:
#  1. We are allowed 1 pass over the sequence
#  2. We are allowed to store 1 object in an object called MemorySlot.
#  3. We can use 1 instance of a Counter object, this object has a few methods that we cannot extend/change:
#       plus1
#       minus1
#       is_zero
#
# Implement the missing python code to find a'.


class MemorySlot:
    """a single memory slot for objects of any type
    you cannot assign values to any other variables than the memory slot"""

    def __init__(self):
        self._value = None

    def replace(self, value):
        self._value = value

    @property
    def get(self):
        return self._value


class Counter:
    """A really weird counter that doesn't tell what the count is
    It can increment by 1, decrement by 1 and check if the value is 0"""

    def __init__(self):
        self._count = 0

    def plus1(self):
        self._count += 1

    def minus1(self):
        self._count -= 1

    @property
    def is_zero(self) -> bool:
        return self._count == 0


def find_most_frequent(*values):
    counter = Counter()  # use only 1
    slot = MemorySlot()  # use only 1
    # your implementation goes here

    return slot.get
