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
        print(f"[{n}]fib(0)[0]")
        return 0
    elif n == 1:
        print(f"[{n}]fib(1)[1]")
        return 1
    else:
        print (f"[{n}]")
        left = fib_fn(n - 1)
        print(f"[{n}]fib({n}-1)[{left}]")
        right = fib_fn(n - 2)
        print (f"fib({n}-2)[{right}]")

        return  left + right


def fib_true_recursion(n: int, i: int = 0, previous: int = 0, current: int = 1) -> int:
    if n == i + 1 :
        print(f"[n={n}][i={i}][previous={previous}][current={current}]")
        return previous

    print(f"[n={n}][i={i}][previous={previous}][current={current}]")
    return fib_true_recursion(n = n, i = i + 1, previous = current, current = current + previous)



def fib(n: int) -> int:
    return fib_true_recursion(n, 0,0, 1)


if __name__ == '__main__':
    fib_true_recursion(5)
    # print(f"[{datetime.now().strftime('%H:%M:%S')}] start")
    # res = fib_imperative(40)
    # print(f"[{datetime.now().strftime('%H:%M:%S')}] imperative {res}")
    # #
    # # print(f"[{datetime.now().strftime('%H:%M:%S')}] start")
    # # res = fib_fn(40)
    # # print(f"[{datetime.now().strftime('%H:%M:%S')}] fn {res}")
    #
    # print(f"[{datetime.now().strftime('%H:%M:%S')}] start")
    # res = fib(40)
    # print(f"[{datetime.now().strftime('%H:%M:%S')}] fn {res}")
