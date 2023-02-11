from functools import cache
from typing import Callable


def memoize(pure_fn: Callable[[int], int]) -> Callable[[int], int]:
    memory = {}  # type: ignore

    def decorator(key_value: int) -> int:
        if key_value in memory:
            return memory[key_value]
        else:
            result = pure_fn(key_value)
            memory[key_value] = result
            return result

    return decorator


# @memoize
def fib(n: int) -> int:
    return n if n < 2 else (fib(n - 1) + fib(n - 2))


# solution
# def memoiz(fn: Callable[[int], int]) -> Callable[[int], int]:
#     memory = {}
#
#     def wrapper(depth: int) -> int:
#         if depth in memory:
#             return memory[depth]
#         else:
#             result = fn(depth)
#             memory[depth] = result
#             return result
#
#     return wrapper
#
#
# @memoiz
# def fib(n: int) -> int:
#     return n if n < 2 else (fib(n - 1) + fib(n - 2))



if __name__ == '__main__':
    fib = cache(fib)
    print(fib(100))
