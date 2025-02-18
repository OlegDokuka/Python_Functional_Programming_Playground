import time
from abc import abstractmethod
from concurrent.futures import Executor, Future
from multiprocessing import Process
from threading import Thread
from typing import Callable, Generic, TypeVar

counter: int = 0

def worker(id):
    global counter
    start = time.time_ns()
    print(f"[{id}] starting")
    counter += 1
    print(f"[{id}] done  calc {counter} time taken {(time.time_ns() - start) / 1000000} ms")


def worker2(id):
    start = time.time_ns()
    print(f"[{id}] starting")
    res = 0
    for i in range(1000000):
        res += i
        print(f"[{id}] {res}")
    print(f"[{id}] done calc {res} time taken {(time.time_ns() - start) / 1000000} ms")


if __name__ == '__main__':
    counter+=1
    start = time.time_ns()
    t1 = Process(target=worker2, args=(1,))
    t2 = Process(target=worker2, args=(2,))
    t1.start()
    t2.start()
    print(f"processes allocated it took {(time.time_ns() - start) / 1000000} ms")
    t1.join()
    t2.join()
