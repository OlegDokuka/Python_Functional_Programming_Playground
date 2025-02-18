from functools import partial
from typing import Callable

negate: Callable[[int], int] = lambda value: value if value < 0 else -value
abs: Callable[[int], int] = lambda value: -value if value < 0 else value
increment: Callable[[int], int] = lambda value: value + 1
decrement: Callable[[int], int] = lambda value: value - 1
pow2: Callable[[int], int] = lambda value: value ** 2


print(partial(pow, exp = 2)(8))

def convert_to_int(raw_int: str) -> int:
    return int(raw_int)

def compose[IN, OUT, OUT2](fn1: Callable[[IN], OUT], fn2: Callable[[OUT], OUT2]) -> Callable[[IN], OUT2]:
    return lambda arg: fn2(fn1(arg))

if __name__ == '__main__':
    res1 = pow2(4)
    res2 = negate(res1)
    res3 = increment(res2)
    res4 = increment(res3)
    res_final = abs(res4)

    compose(compose(compose(convert_to_int, increment), increment), abs)

    print(res_final)

    print(
        abs(
            increment(
                increment(
                    negate(
                        pow2(4)
                    )
                )
            )
        )
    )

    my_fn = compose(compose(compose(compose(pow2, negate), increment) ,increment), abs)

    print(
        my_fn(6)
    )
