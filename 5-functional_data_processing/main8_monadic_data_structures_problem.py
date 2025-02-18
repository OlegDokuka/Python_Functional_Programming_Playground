from abc import abstractmethod
from functools import partial, reduce
from itertools import chain, filterfalse, accumulate, starmap, groupby
from typing import TypeVar, Generic, Callable, Any, Tuple, Iterable, Self, AnyStr



def compose(*fns: Callable) -> Callable:
    return reduce(lambda state, next_fn: lambda it: next_fn(state(it)), fns)

def pipe(*fns: Callable[[Iterable], Iterable]) -> Callable[[Iterable], Iterable]:
    # return fns[0] if len(fns) == 1 else lambda i: fns[-1](pipe(*fns[:-1])(i))
    return reduce(lambda state, next_fn: lambda it: next_fn(state(it)), fns)


is_numeric: Callable[[str], bool] = lambda x: x.isnumeric()
gt: Callable[[int], Callable[[int], bool]] = lambda value : lambda item: item > value
to_int: Callable[[str], int] = lambda x: int(x)
#
# def comonent_A(dataset: SmartDataSet[T]) -> SmartDataSet[B]:
#     dataset.pipe(
#         filter,
#         map,
#         groupby,
#         flatten
#     )
#
# def comonent_B(dataset: SmartDataSet[T]) -> SmartDataSet[B]:
#     dataset.pipe(
#         filter,
#         map,
#         groupby,
#         flatten
#     )
#
#
#
# IO.readDataSet()\ # SmartDataSet(...)
#   .transform(
#     component_A,
#     componentB
# ).exec(Io.store)

if __name__ == '__main__':
    print([i for i in [to_int(raw_i) for raw_i in ["asb", "0", "1", "2", "3.", "5"] if is_numeric(raw_i)] if gt(0)(i)])
    # my_processing_pipe = compose(is_numeric, to_int, gt(0))
    # print([my_processing_pipe(i) for i in ["asb", "1", "2", "3.", "5"]])



    my_processing_pipe = pipe(
        partial(filter, is_numeric),
        partial(map, to_int),
        partial(filter, gt(0)),
        list
    )
    print(my_processing_pipe(["asb", "0", "1", "2", "3.", "5"]))