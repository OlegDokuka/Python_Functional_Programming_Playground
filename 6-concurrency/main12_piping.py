import math
import time
from functools import partial, reduce
from multiprocessing import Process, JoinableQueue, Queue
from queue import Empty
from time import sleep
from typing import Iterable, Callable, Any


def pipe(*fns: Callable[[Iterable], Iterable]) -> Callable[[Iterable], Iterable]:
    # return fns[0] if len(fns) == 1 else lambda i: fns[-1](pipe(*fns[:-1])(i))
    return reduce(lambda state, next_fn: lambda it: next_fn(state(it)), fns)


is_numeric: Callable[[str], bool] = lambda x: x.isnumeric()
gt: Callable[[int], Callable[[int], bool]] = lambda value : lambda item: item > value
# to_int: Callable[[str], int] = lambda x: int(x)


def to_int(val: str) -> int:
    sleep(0.3)
    return int(val)

class TerminateFlag:
    pass

def inner(input_queue: Queue, output_queue: Queue, processing_fn: Callable[[Iterable], Iterable]):
    def queue_reader() -> Iterable:
        try:
            while True:
                message = input_queue.get()
                if isinstance(message, TerminateFlag):
                    return
                yield message
        except ValueError:
            return

    for e in processing_fn(queue_reader()):
        output_queue.put(e)

    output_queue.put(TerminateFlag())

# Process Main ---1-2-3          2-5
#                      \       /
# Process 2             1 | 2-5
def publish_on(fn: Callable[[Iterable], Iterable]) -> Callable[[Iterable], Iterable]:

    def outer(input_it: Iterable) -> Iterable:
        try:
            input_queue: Queue = Queue()
            output_queue: Queue = Queue()
            Process(target=inner, args=(input_queue, output_queue, fn)).start()

            for item in input_it:
                input_queue.put(item)
                try:
                    message = output_queue.get_nowait()
                    if isinstance(message, TerminateFlag):
                        return
                    yield message
                except Empty:
                    continue

            input_queue.put(TerminateFlag())

            while True:
                message = output_queue.get()
                if isinstance(message, TerminateFlag):
                    return
                yield message
        except ValueError:
            return

    return outer



def is_prime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    sqrt_n = int(math.floor(math.sqrt(n)))
    for i in range(3, sqrt_n + 1, 2):
        if n % i == 0:
            return False
    return True

def check_if_prime(it):
    return pipe(
        lambda _it: filter(is_prime, _it),
        partial(map, lambda a: a),
        print_fn("inner")
    )(it)

def print_fn(label: str):
    def inner(it):
        for item in it:
            print(label, item)
            yield item

    return inner

if __name__ == '__main__':
    start = time.time_ns()
    my_processing_pipe = pipe(
        partial(filter, is_numeric),
        partial(map, to_int),
        partial(filter, gt(0)),
        print_fn("before"),
        # check_if_prime,
        publish_on(check_if_prime),
        list
    )


    print(my_processing_pipe(["asb", "0", "1", "2", "3.", "5", "7", "*", "8", "9", "11", "10.", "21", "112272535095263", "112582705942171", "112272535095293", "115280095190773", "1099726899285419", "115797848077099"]))


    print(f"time taken {(time.time_ns() - start) / 1000000} ms")


