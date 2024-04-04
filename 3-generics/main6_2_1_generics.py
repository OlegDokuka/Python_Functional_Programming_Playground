from math import sqrt
from numbers import Number
from typing import Callable, TypeVar, Generic

T = TypeVar("T", )
K = TypeVar("K", covariant=True)

class Animal:
    def __init__(self):
        return
class Cat(Animal):
    def __init__(self):
        super().__init__()
        return
class Dog(Animal):
    def __init__(self):
        super().__init__()
        return

class Box(Generic[T]):
    def __init__(self):
        super().__init__()
        return

if __name__ == '__main__':
    # print(sqrt2(3))
    box: Box[str] = Box()
    box = box.put(1)
    print()
