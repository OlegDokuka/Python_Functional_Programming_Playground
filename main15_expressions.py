import asyncio
from typing import Callable

import expression
from expression import Option

negate: Callable[[int], int] = lambda value: value if value < 0 else -value
abs: Callable[[int], int] = lambda value: -value if value < 0 else value
increment = lambda value: value + 1
decrement = lambda value: value - 1


@expression.curry(1)
def pow(degree, value):
    return value ** degree


pow2 = pow(2)
pow3 = pow(3)

if __name__ == '__main__':
    # res_fn = compose(pow_carried(3),
    #                  negate,
    #                  increment,
    #                  pow_carried(2),
    #                  increment,
    #                  abs)
    print(expression.compose(pow(3),
                             negate,
                             increment,
                             pow(2),
                             increment,
                             abs)(4))


    # def exists(x: Option[int]) -> bool:
    #     match x:
    #         case Some(value):
    #             return value.
    #     return False

    print(expression.collections.seq.of_iterable([1, 2, 3])
          .map(lambda i: i + 1)
          .filter(lambda i: i > 2))

    # mylist([1, 2, 3])
    # .pipe(partial(map, lambda i: i + 1),
    #       partial(zip, [3, 2, 1]),
    #       partial(map, lambda t: t[0] + t[1]),
    #       partial(filter, lambda i: i > 2))
