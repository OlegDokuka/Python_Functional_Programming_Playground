# refactor to functional
from datetime import datetime


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


def fib_fn(n: int) -> int:
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib_fn(n - 1) + fib_fn(n - 2)


if __name__ == '__main__':
    print(f"[{datetime.now().strftime('%H:%M:%S')}] start")
    res = fib_imperative(60)
    print(f"[{datetime.now().strftime('%H:%M:%S')}] imperative {res}")

    print(f"[{datetime.now().strftime('%H:%M:%S')}] start")
    res = fib_fn(60)
    print(f"[{datetime.now().strftime('%H:%M:%S')}] fn {res}")
