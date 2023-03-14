from abc import abstractmethod
from concurrent.futures import ProcessPoolExecutor, Executor
from threading import Thread, Lock
from typing import Any, Callable, Sized


class Task:
    _lock: Lock = Lock()
    _done = False
    _future = None
    _executor = None
    result = None

    def __init__(self, exec: Executor):
        self._executor = exec

    @abstractmethod
    def __call__(self, *args, **kwargs):
        pass

    def __done__(self, res):
        self._lock.acquire()
        self._done = True
        self.result = res
        callback = self._callback
        self._lock.release()

        if callback is not None:
            callback(res)

    def fork(self):
        self._future = self._executor.submit(self)
        return self

    def join(self, callback: Callable[[Any], None]):
        if self._future is None:
            raise Exception("Already joined once")

        self._lock.acquire()
        done = self._done
        res = self.result
        self._future.add_done_callback(callback)
        self._lock.release()

        if done:
            callback(res)


class MyTask(Task):
    def __init__(self, dataset: Sized, start=0, end=-1):
        self._dataset = dataset
        self._start = start
        self._end = len(dataset) if end == -1 else end

    def __call__(self, *args, **kwargs):
        dataset_len = self._end - self._start
        if dataset_len <= 2:
            self.__done__(list(map(lambda x: x * 2, self._dataset[self._start:self._end])))
        else:
            p1 = MyTask(self._dataset, self._start, round(self._start + dataset_len / 2))
            p2 = MyTask(self._dataset, round(self._start + dataset_len / 2), self._end).fork()

            p1.join(lambda p1_result: p2.join(lambda p2_result: self.__done__(p1_result + p2_result)))



if __name__ == '__main__':
    MyTask([1, 2, 3, 4]).fork().join(print)
