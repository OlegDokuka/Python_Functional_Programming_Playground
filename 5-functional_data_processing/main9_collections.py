import itertools
from functools import partial, reduce
from typing import Callable, Iterable




def pipe(*fns: Callable[[Iterable], Iterable]) -> Callable[[Iterable], Iterable]:
    # return fns[0] if len(fns) == 1 else lambda i: fns[-1](pipe(*fns[:-1])(i))
    return reduce(lambda state, next_fn: lambda it: next_fn(state(it)), fns)


# def reduce(seed: int, fn: Callable[[int, int], int], it: Iterable[int]) -> int:
#     result = seed
#     for i in it:
#         result = fn(result, i)
#     result = 0
# for i in it:
#     result = result + i
#
# return result




if __name__ == '__main__':
    mylist: list[int]= list([1, 2, 3, 4, 5])
    print(mylist)
    mylist.append("6")
    print(mylist)
    myset = {1, 1, 2, 3, 4}
    print(myset)
    myset.add(1)
    print(myset)

    mytuple: tuple[Callable[[int], int], str, list[int]] = (lambda x: x ** 2, "2", mylist)
    print(mytuple)
    mylist.append("7")
    print(mytuple)

    mydictionary = dict(a=1, b=2, c=3)
    mydictionary1 = {"a":1, "b":2, "c":3}
    print(mydictionary)
    print(mydictionary1)

    my_complext_list = [[1], [2], [3], [4]]
    print(my_complext_list)
    print(list(reduce(itertools.chain, my_complext_list)))

    #
    # zip(io_request() \
    #     .pipe(
    #     filter(),
    #     map,
    #
    # ), io_request, io_request)

    print(list(zip([1, 2, 3], ["a", "b", "c"], [1, 2, 3])))

    # pipe(our_map(lambda i: i + 1),
    #      partial(zip, [3, 2, 1]),
    #      partial(map, lambda t: t[0] + t[1]),
    #      partial(filter, lambda i: i > 2))([1, 2, 3])
    #
    # print(reduce(lambda s, n: s + n, list([1, 2, 3])))
    #
    # print(mylist([1, 2, 3])
    #       .pipe(partial(map, lambda i: i + 1),
    #             partial(zip, [3, 2, 1]),
    #             partial(map, lambda t: t[0] + t[1]),
    #             partial(filter, lambda i: i > 2)))
