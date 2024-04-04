from typing import Callable

negate: Callable[[int], int] = lambda value: value if value < 0 else -value
abs: Callable[[int], int] = lambda value: -value if value < 0 else value
increment: Callable[[int], int] = lambda value: value + 1
decrement: Callable[[int], int] = lambda value: value - 1
pow2: Callable[[int], int] = lambda value: value ** 2

if __name__ == '__main__':
    res1 = pow2(4)
    res2 = negate(res1)
    res3 = increment(res2)
    res4 = increment(res3)
    res_final = abs(res4)

    print(res_final)
    print(abs(increment(increment(negate(pow2(4))))))
