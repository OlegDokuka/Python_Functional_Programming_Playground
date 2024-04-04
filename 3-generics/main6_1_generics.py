from math import sqrt
from numbers import Number
from typing import Callable, TypeVar

negate: Callable[[int], int] = lambda value: value if value < 0 else -value
abs: Callable[[int], int] = lambda value: -value if value < 0 else value
increment: Callable[[int], int] = lambda value: value + 1
decrement: Callable[[int], int] = lambda value: value - 1
pow: Callable[[int, int], int] = lambda degree, value: value ** degree
sqrt2: Callable[[float], float] = lambda value: sqrt(value)

pow_carried = lambda degree: lambda value: pow(degree, value)
pow2 = pow_carried(2)
pow3 = pow_carried(3)

# def map(value: int, *operations: Callable[[int], int]) -> int:
#     if (len(operations) == 0):
#         return value
#     else:
#         return map(operations[0](value), *operations[1:])


# Solution
T = TypeVar("T")


def map(value: T, *operations: Callable[[T], T]) -> T:
    if (len(operations) == 0):
        return value
    else:
        return map(operations[0](value), *operations[1:])


if __name__ == '__main__':
    # print(sqrt2(3))
    print(map(1.1, sqrt2))
