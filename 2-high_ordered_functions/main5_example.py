from functools import cache
from typing import Callable, Dict, Any


def memoiz(func: Callable[[int], int]) -> Callable[[int], int]:
    cache = {}

    def wrapper(input: int) -> int:
        if input not in cache:
            cache[input] = func(input)

        return cache[input]

    return wrapper


# @memoiz
def fib(n: int) -> int:
    return n if n < 2 else (fib(n - 1) + fib(n - 2))
#
# fib: Callable[[int], int] = memoiz(lambda n: n if n < 2 else fib(n - 1) + fib(n - 2))
#
#
# def y_combinator(fn_fn: Callable[[Callable[[int], int], int], Callable[[int], int]]) -> Callable[[int], int]:
#     return lambda n: fn_fn(y_combinator())
#
#
# fib:Callable[[int], int] =

if __name__ == '__main__':
   sum( y_combinator(lambda anon_fib: \
                     memoiz(lambda n: n if n < 2 else (anon_fib(n - 1) + anon_fib(n - 2)))))
    print(fib(100))
    # print(fib(100))
