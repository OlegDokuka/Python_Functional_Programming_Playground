from abc import abstractmethod
from functools import partial
from typing import TypeVar, Generic, Callable, Any, Tuple, Iterable, Self, AnyStr

zip

T = TypeVar("T")
R = TypeVar("R", covariant=True)
GC = TypeVar("GC", covariant=True, bound="PipebaleIterable")


class Optional(Generic[T]):
    def __init__(self) -> None:
        return

    def is_present(self) -> bool:
        raise Exception("Not implemented")

    def get(self):
        raise Exception("Not implemented")

    @staticmethod
    def of(value: T) -> "Optional[T]":
        return Something(value)

    @staticmethod
    def empty() -> "Optional[T]":
        return Nothing()

    def map(self, fn: Callable[[T], R]) -> "Optional[R]":
        return Something(fn(self.get())) if self.is_present() else Nothing()

    def filter(self, fn: Callable[[T], bool]) -> "Optional[T]":
        return self if self.is_present() and fn(self.get()) else Nothing()

    def flat_map(self, fn: Callable[[T], "Optional[R]"]) -> "Optional[R]":
        return fn(self.get()) if self.is_present() else Nothing()

    def zip_with(self, other: "Optional[R]") -> "Optional[(T, R)]":
        return Something((self.get(), other.get())) if self.is_present() and other.is_present() else Nothing


class Something(Optional[T]):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def is_present(self) -> bool:
        return True

    def get(self):
        return self.value


class Nothing(Optional[T]):
    def __init__(self):
        super().__init__()

    def is_present(self) -> bool:
        return False

    def get(self):
        raise Exception("Nothing")


if __name__ == '__main__':
    o = Optional.of(123) \
        .map(str) \
        .map(lambda input: isinstance(input, str)) \
        .zip_with(Optional.of("312"))

    if o.is_present(): print(o.get())
