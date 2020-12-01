from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Union


class Vector(ABC):
    """abstract vector class"""

    _float_size = 4
    _int_size = 8

    @staticmethod
    def one(size: int) -> Vector:
        """return a vector of ones"""
        raise NotImplementedError

    @staticmethod
    def zero(size: int) -> Vector:
        """returns a vector of zeros"""
        raise NotImplementedError

    def __init__(self):
        super().__init__()

    @property
    def size(self) -> int:
        """returns the size of the vector"""
        raise NotImplementedError

    @property
    def values(self) -> List[float]:
        """returns all values of the vector as a list"""
        raise NotImplementedError

    @property
    def compress(self) -> Vector:
        """checks which implementation of Vector will hold less memory
        and creates a copy of the vector with the same values but the optimal type
        assume that every int is 8 and every float is 4
        """
        raise NotImplementedError

    def __getitem__(self, item) -> Union[float, Vector]:
        """indexing method"""
        raise NotImplementedError

    def __neg__(self) -> Vector:
        """return the negative of self"""
        raise NotImplementedError

    def __add__(self, other) -> Vector:
        """add a scalar or a compatible vector"""
        raise NotImplementedError

    def __sub__(self, other) -> Vector:
        """subtract a scalar or a compatible vector"""
        raise NotImplementedError

    def __mul__(self, other) -> Vector:
        """multiply by scalar or compatible vector"""
        raise NotImplementedError

    def __invert__(self):
        """invert the values of the vector"""
        raise NotImplementedError

    def __truediv__(self, other) -> Vector:
        """divide by a vector or a scalar"""
        raise NotImplementedError

    def __eq__(self, other) -> bool:
        """checks that all values are the same"""
        raise NotImplementedError

    def __ne__(self, other) -> bool:
        """not equal"""
        raise NotImplementedError

    def dot(self, other: Vector) -> float:
        """return the dot product of the 2 vectors, if compatible"""
        raise NotImplementedError

    def __str__(self):
        raise NotImplementedError

    def almost_equal(self, other: Vector, eps: float = 1e-10) -> bool:
        v1 = self.values
        v2 = other.values
        out = True
        for t in zip(v1, v2):
            out &= (abs(t[0] - t[1]) < eps)
        return out


# noinspection PyCompatibility
class DenseVector(Vector, ABC):
    """A column vector with values implemented as a list of floats"""

    def __init__(self, *values):
        super().__init__()
        assert len(values) > 0, """vectors must have at least 1 value"""
        self._values = [*values]

    @property
    def size(self) -> int:
        return len(self.values)

    @property
    def values(self) -> List[float]:
        return self._values

    def __getitem__(self, item) -> Union[float, Vector]:
        raise NotImplementedError()

    @property
    def compress(self) -> Vector:
        raise NotImplementedError()

    def __neg__(self):
        raise NotImplementedError()

    def __invert__(self):
        raise NotImplementedError()

    def __add__(self, other) -> Vector:
        raise NotImplementedError()

    def __mul__(self, other) -> Vector:
        raise NotImplementedError()

    def __str__(self):
        return str(self.values)


class SparseVector(Vector, ABC):
    """A column vector that is optimized to have many 0s"""

    def __init__(self, size: int, indices: List[int], non_zero_values: List[float]):
        """
        :param size: the size of the vector
        :param indices: all non 0 indices
        :param non_zero_values: all non 0 values
        """
        super().__init__()
        assert size > 0, """size must be greater than 0, got {}""".format(size)
        if len(indices) > 0:
            assert max(indices) <= size-1, \
                """found an index ({}) that is greater than size ({})""".format(max(indices), size)
        assert len(indices) == len(non_zero_values), """length of indices is not equal to length of values"""
        _negs = list(filter(lambda idx: idx < 0, indices))
        assert len(_negs) == 0, \
            """can't instantiate SparseVector with negative indices, got {}""".format(_negs)
        _cnts = set()
        for i in indices:
            if i in _cnts:
                raise AssertionError("""index {} is duplicate in the indices={}""".format(i, indices))
            else:
                _cnts.add(i)
        non_zero_values = [_ for _ in non_zero_values]
        indices = [_ for _ in indices]
        while 0 in non_zero_values:
            i = non_zero_values.index(0)
            non_zero_values.pop(i)
            indices.pop(i)

        self._size = size
        self._indices = indices
        self._non_zero_values = non_zero_values

    @property
    def indices(self):
        return self._indices

    @property
    def non_zero_values(self):
        return self._non_zero_values

    @property
    def size(self) -> int:
        return self._size

    @property
    def values(self) -> List[float]:
        raise NotImplementedError()

    @property
    def compress(self) -> Vector:
        raise NotImplementedError()

    def __getitem__(self, item) -> Union[float, Vector]:
        raise NotImplementedError()

    def __neg__(self):
        raise NotImplementedError()

    def __invert__(self):
        raise NotImplementedError()

    def __add__(self, other) -> Vector:
        raise NotImplementedError()

    def __mul__(self, other) -> Vector:
        raise NotImplementedError()

    def __str__(self):
        return """[[{size}, {ind}, {val}]]""".format(
            size=self.size,
            ind=str(self.indices),
            val=str(self.non_zero_values)
        )


class BinaryVector(Vector, ABC):
    """Optional: if you want to implement a vector that has only 1s or 0s as values
    write tests to see if it works
    """
    pass
