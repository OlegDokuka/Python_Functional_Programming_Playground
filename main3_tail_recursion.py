# refactor to functional
from datetime import datetime

from tail_recursion import tail_call_optimized


def fib_imperative(n: int) -> int:
    if n == 0:
        return 0

    current = 1
    previous = 0

    for i in range(1, n):
        old_current = current
        current += previous
        previous = old_current

    return current


# fixme
# def fib_fn(n: int) -> int:
#     if n == 0:
#         return 0
#     elif n == 1:
#         return 1
#     else:
#         return fib_fn(n - 1) + fib_fn(n - 2)


# solution
@tail_call_optimized
def fib_helper(depth: int, step: int, current: int, previous: int) -> int:
    if depth == step:
        return current
    else:
        return fib_helper(depth, step + 1, current + previous, current)


def fib_fn(n: int) -> int:
    return n if n < 2 else fib_helper(n, 2, 1, 1)


if __name__ == '__main__':
    print(f"[{datetime.now().strftime('%H:%M:%S')}] start")
    res = fib_imperative(5000)
    print(f"[{datetime.now().strftime('%H:%M:%S')}] imperative {res}")

    print(f"[{datetime.now().strftime('%H:%M:%S')}] start")
    res = fib_fn(5000)
    print(f"[{datetime.now().strftime('%H:%M:%S')}] fn {res}")
