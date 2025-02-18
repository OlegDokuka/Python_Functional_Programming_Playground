from functools import reduce
from typing import TypeVar, Generic, Callable, Any, overload



class Optional[T]:
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

    @overload
    def pipe(self, fn: Callable[["Optional[T]"], "Optional[R]"]) -> "Optional[R]": ...

    @overload
    def pipe(self, fn0: Callable[["Optional[T]"], "Optional[R]"],
             fn1: Callable[["Optional[R]"], "Optional[R1]"]) -> "Optional[R1]": ...

    @overload
    def pipe(self, fn0: Callable[["Optional[T]"], "Optional[R]"], fn1: Callable[["Optional[R]"], "Optional[R1]"],
             fn2: Callable[["Optional[R1]"], "Optional[R2]"]) -> "Optional[R2]": ...

    @overload
    def pipe(self, fn0: Callable[["Optional[T]"], "Optional[R]"], fn1: Callable[["Optional[R]"], "Optional[R1]"],
             fn2: Callable[["Optional[R1]"], "Optional[R2]"],
             fn3: Callable[["Optional[R2]"], "Optional[R3]"]) -> "Optional[R3]": ...

    @overload
    def pipe(self, fn0: Callable[["Optional[T]"], "Optional[R]"], fn1: Callable[["Optional[R]"], "Optional[R1]"],
             fn2: Callable[["Optional[R1]"], "Optional[R2]"],
             fn3: Callable[["Optional[R2]"], "Optional[R3]"],
             fn4: Callable[["Optional[R3]"], "Optional[R4]"]) -> "Optional[R4]": ...

    @overload
    def pipe(self, fn0: Callable[["Optional[T]"], "Optional[R]"], fn1: Callable[["Optional[R]"], "Optional[R1]"],
             fn2: Callable[["Optional[R1]"], "Optional[R2]"],
             fn3: Callable[["Optional[R2]"], "Optional[R3]"],
             fn4: Callable[["Optional[R3]"], "Optional[R4]"],
             fn5: Callable[["Optional[R4]"], "Optional[R5]"]) -> "Optional[R5]": ...

    @overload
    def pipe(self, fn0: Callable[["Optional[T]"], "Optional[R]"], fn1: Callable[["Optional[R]"], "Optional[R1]"],
             fn2: Callable[["Optional[R1]"], "Optional[R2]"],
             fn3: Callable[["Optional[R2]"], "Optional[R3]"],
             fn4: Callable[["Optional[R3]"], "Optional[R4]"],
             fn5: Callable[["Optional[R4]"], "Optional[R5]"],
             fn6: Callable[["Optional[R5]"], "Optional[R6]"]) -> "Optional[R6]": ...

    @overload
    def pipe(self, fn0: Callable[["Optional[T]"], "Optional[R]"], fn1: Callable[["Optional[R]"], "Optional[R1]"],
             fn2: Callable[["Optional[R1]"], "Optional[R2]"],
             fn3: Callable[["Optional[R2]"], "Optional[R3]"],
             fn4: Callable[["Optional[R3]"], "Optional[R4]"],
             fn5: Callable[["Optional[R4]"], "Optional[R5]"],
             fn6: Callable[["Optional[R5]"], "Optional[R6]"],
             fn7: Callable[["Optional[R6]"], "Optional[R7]"]) -> "Optional[R7]": ...

    @overload
    def pipe(self, fn0: Callable[["Optional[T]"], "Optional[R]"], fn1: Callable[["Optional[R]"], "Optional[R1]"],
             fn2: Callable[["Optional[R1]"], "Optional[R2]"],
             fn3: Callable[["Optional[R2]"], "Optional[R3]"],
             fn4: Callable[["Optional[R3]"], "Optional[R4]"],
             fn5: Callable[["Optional[R4]"], "Optional[R5]"],
             fn6: Callable[["Optional[R5]"], "Optional[R6]"],
             fn7: Callable[["Optional[R6]"], "Optional[R7]"],
             fn8: Callable[["Optional[R7]"], "Optional[R8]"]) -> "Optional[R8]": ...

    def pipe(self, *fns: Callable[["Optional[Any]"], "Optional[Any]"]) -> "Optional[Any]":
        return reduce(lambda opt, fn: fn(opt), fns, self)


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


def map(fn: Callable[[T], R]) -> Callable[[Optional[T]], "Optional[R]"]:
    return lambda cur_opt: Something(fn(cur_opt.get())) if cur_opt.is_present() else Nothing()


def filter(fn: Callable[[T], bool]) -> Callable[[Optional[T]], "Optional[T]"]:
    return lambda cur_opt: cur_opt if cur_opt.is_present() and fn(cur_opt.get()) else Nothing()


def flat_map(fn: Callable[[T], "Optional[R]"]) -> Callable[[Optional[T]], "Optional[R]"]:
    return lambda cur_opt: fn(cur_opt.get()) if cur_opt.is_present() else Nothing()


def zip_with(other: "Optional[R]") -> Callable[[Optional[T]], "Optional[(T, R)]"]:
    return lambda cur_opt: Something(
        (cur_opt.get(), other.get())) if cur_opt.is_present() and other.is_present() else Nothing


if __name__ == '__main__':
    o: Optional[(str, str)] = Optional.of(123) \
        .pipe(
            map(str),
            map(lambda input: isinstance(input, str)),
            zip_with(Optional.of("312"))
        )

    if o.is_present(): print(o.get())
