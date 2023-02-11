from typing import Callable

negate: Callable[[int], int] = lambda value: value if value < 0 else -value
abs: Callable[[int], int] = lambda value: -value if value < 0 else value
increment: Callable[[int], int] = lambda value: value + 1
decrement: Callable[[int], int] = lambda value: value - 1
pow2: Callable[[int], int] = lambda value: value ** 2

if __name__ == '__main__':
    res = abs(increment(increment(negate(pow2(4)))))

    print(res)
