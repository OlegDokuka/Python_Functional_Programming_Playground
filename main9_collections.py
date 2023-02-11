from functools import partial
from typing import Callable, Iterable


class mylist(list):
    def pipe(self, *fns: Callable[[Iterable], Iterable]) -> 'mylist':
        return mylist(pipe(*fns)(self))


def transform(fn: Callable[[Iterable], Iterable], source: Iterable) -> Iterable:
    return fn(source)


def pipe(*fns: Callable[[Iterable], Iterable]) -> Callable[[Iterable], Iterable]:
    return fns[0] if len(fns) == 1 else lambda i: fns[-1](pipe(*fns[:-1])(i))


if __name__ == '__main__':
    print(mylist([1, 2, 3])
          .pipe(partial(map, lambda i: i + 1),
                partial(zip, [3, 2, 1]),
                partial(map, lambda t: t[0] + t[1]),
                partial(filter, lambda i: i > 2)))
