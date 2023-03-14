from typing import TypeVar, Generic, Callable, Any, Tuple

T = TypeVar("T")
R = TypeVar("R", contravariant=True)


class Optional(Generic[T]):

    @staticmethod
    def of(value: T) -> 'Optional[T]':
        return Something(value) if (value is not None) else Nothing()  # type: ignore

    def is_present(self) -> bool:
        raise Exception("not implemented")

    def value(self) -> T:
        raise Exception("not implemented")

    def __factory__(self, value: R) -> 'Optional[R]':
        raise Exception("N/I")

    def map(self, mapper: Callable[[T], R]) -> 'Optional[R]':
        if self.is_present():
            return self.__factory__(mapper(self.value()))
        else:
            return Nothing()

    def filter(self, filter_fn: Callable[[T], bool]) -> 'Optional[T]':
        if self.is_present() and filter_fn(self.value()):
            return self
        else:
            return Nothing()

    def peek(self, action: Callable[[T], None]) -> 'Optional[T]':
        if self.is_present():
            action(self.value())
            return self
        else:
            return Nothing()

    def transform(self, fn: Callable[['Optional[T]'], 'Optional[R]']) -> 'Optional[R]':
        return fn(self)

    def flat_map(self, fn: Callable[[T], 'Optional[R]']) -> 'Optional[R]':
        if self.is_present():
            return fn(self.value())
        else:
            return Nothing()

    def zip(self, another: 'Optional[R]') -> 'Optional[Tuple[T,R]]':
        if self.is_present() and another.is_present():
            return self.__factory__((self.value(), another.value()))
        else:
            return Nothing()


class Nothing(Optional[T]):
    def is_present(self) -> bool:
        return False


class Something(Optional[T]):
    def __init__(self, value: T):
        super().__init__()
        self._value = value

    def is_present(self) -> bool:
        return True

    def value(self) -> T:
        return self._value

    def __factory__(self, value: R) -> "Something[R]":
        return Something(value)


def do_my_processing_over_optional(o_value: Optional[str]) -> Optional[int]:
    return o_value.map(lambda x: int(x))


def do_my_processing_over_optional_1(o_value: Optional[int]) -> Optional[int]:
    return o_value.flat_map(lambda value: Optional.of(str(value))) \
        .filter(lambda value: len(value) >= 3) \
        .map(lambda value: int(value))


if __name__ == '__main__':
    # value.transform(do_my_processing_over_optional)
    o = Optional.of(123) \
        .map(lambda value: str(value)) \
        .transform(do_my_processing_over_optional) \
        .transform(do_my_processing_over_optional_1) \
        .peek(lambda value: print(f"after all {value}")) \
        .zip(Optional.of("312"))

    if o.is_present(): print(o.value())
