from functools import partial, reduce
from typing import Callable, Iterable


class mylist(list):
    def pipe(self, *fns: Callable[[Iterable], Iterable]) -> 'mylist':
        return mylist(pipe(*fns)(self))


def transform(fn: Callable[[Iterable], Iterable], source: Iterable) -> Iterable:
    return fn(source)


def pipe(*fns: Callable[[Iterable], Iterable]) -> Callable[[Iterable], Iterable]:
    # return fns[0] if len(fns) == 1 else lambda i: fns[-1](pipe(*fns[:-1])(i))
    return reduce(lambda state, next_fn: lambda it: next_fn(state(it)), fns)


# def reduce(seed: int, fn: Callable[[int, int], int], it: Iterable[int]) -> int:
#     result = seed
#     for i in it:
#         result = fn(result, i)
#     result = 0
# for i in it:
#     result = result + i
#
# return result


def our_map(mapper: Callable[[int], str]) -> Callable[[Iterable[int]], Iterable[str]]:
    return lambda ite: map(mapper, ite)

if __name__ == '__main__':
    pipe(our_map(lambda i: i + 1),
         partial(zip, [3, 2, 1]),
         partial(map, lambda t: t[0] + t[1]),
         partial(filter, lambda i: i > 2))([1, 2, 3])

    print(reduce(lambda s, n: s + n, list([1, 2, 3])))

    print(mylist([1, 2, 3])
          .pipe(partial(map, lambda i: i + 1),
                partial(zip, [3, 2, 1]),
                partial(map, lambda t: t[0] + t[1]),
                partial(filter, lambda i: i > 2)))
