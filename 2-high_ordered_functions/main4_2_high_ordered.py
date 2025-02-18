from functools import partial
from typing import Callable

negate: Callable[[int], int] = lambda value: value if value < 0 else -value
abs: Callable[[int], int] = lambda value: -value if value < 0 else value
increment = lambda value: value + 1
decrement = lambda value: value - 1


pow2 = partial(pow, exp = 2)

print(pow2(8))


# print(pow(2)(8))

# solution 1
# def compose(fn1: Callable[[int], int], fn2: Callable[[int], int]) -> Callable[[int], int]:
#     return lambda value: fn2(fn1(value))
#
#
# def compose(fn1: Callable[[int], int], fn2: Callable[[int], int]) -> Callable[[int], int]:
#     return lambda value: fn2(fn1(value))

# solution 2
def compose(*fns: Callable[[int], int]) -> Callable[[int], int]:
    if len(fns) == 1:
        return fns[0]
    else:
        return lambda value: compose(*fns[1:])(fns[0](value))


if __name__ == '__main__':
    # res = abs(increment(increment(negate(pow2(2)))))
    print("hello world")
    # res_fn = compose(compose(compose(compose(pow2, negate), increment), increment), abs)
    res_fn = compose(pow2,
                     negate,
                     increment,
                     pow2,
                     increment,
                     abs)
    #
    # print(res_fn(1))

    # pow2 = pow_carried(2)
    # pow3 = pow_carried(3)
    #
    # print(pow3(3))
    # print(pow3(4))

    # print(res)
    # print(res_fn(4))
