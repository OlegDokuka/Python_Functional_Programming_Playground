import concurrent
import time
from abc import abstractmethod
from concurrent.futures import Executor, Future
from multiprocessing import Process
from threading import Thread
from typing import Callable, Generic, TypeVar

counter: int = 0

def worker(id):
    global counter
    time.sleep(1)
    start = time.time_ns()
    print(f"[{id}] starting")
    counter += 1
    print(f"[{id}] done  calc {counter} time taken {(time.time_ns() - start) / 1000000} ms")
    return counter + id


def worker2(id):
    start = time.time_ns()
    print(f"[{id}] starting")
    res = 0
    for i in range(1000000):
        res += i
        print(f"[{id}] {res}")
    print(f"[{id}] done calc {res} time taken {(time.time_ns() - start) / 1000000} ms")




if __name__ == '__main__':
    with concurrent.futures.ProcessPoolExecutor(2) as executor:
        future1: Future[int] = executor.submit(worker, 1)
        future2: Future[int] = executor.submit(worker, 2)

        def when_work_is_done1(result: Future[int]):
            def when_work_is_done2(result: Future[int]):
                print("result", result.result())

                def when_work_is_done2(result: Future[int]):
                    print("result", result.result())
                    when_work_is_done()
                when_work_is_done()
            print("result", result.result())
            when_work_is_done



        future1.add_done_callback(when_work_is_done)
        future2.add_done_callback(when_work_is_done)
        print("1")
        print("2")
        print("3")
        # print("future1", future1.result())
        # print("future2", future2.result())
