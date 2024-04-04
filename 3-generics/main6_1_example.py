from math import sqrt
from numbers import Number
from typing import Callable, TypeVar, Union, Generic

T = TypeVar('T')


def sum(x: T, y: T) -> T:
    if not isinstance(x, type(y)):
        raise TypeError('bla')
    return x + y


TV = TypeVar('TV', bound=Number)


class Vector(Generic[TV]):

    def sum(self) -> TV:
        raise Exception("boom")

    def put(self, value_fn: Callable[[], TV]):
        # self.values.insert(0, value)
        return self


class Vector_Int(Vector[int]):
    def sum(self) -> int:
        return 1


if __name__ == '__main__':
    vec: Vector[Number] = Vector_Int()
    fn_int: Callable[[Number], int] = lambda n: sum(1, 2)
    fn: Callable[[int], Number] = fn_int
    vec.put(fn)
    # print(res)
    sum("", "wdqwe")
    sum(Vector(), Vector())
