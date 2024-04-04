from abc import abstractmethod
from concurrent.futures import Executor, Future, ProcessPoolExecutor
from typing import Callable, Generic, TypeVar

T = TypeVar('T')


class ForkJoinTask(Generic[T]):
    _future: Future[T]

    def __init__(self, executor: Executor):
        self._executor = executor

    @abstractmethod
    def __call__(self, *args, **kwargs):
        pass

    def fork(self) -> None:
        self._future = self._executor.submit(self)

    def join(self) -> T:
        return self._future.result()


class FibTask(ForkJoinTask[int]):
    _n: int
    def __init__(self, executor: Executor, n: int):
        super().__init__(executor)
        self._n = n
    def __call__(self, *args, **kwargs):
        if (self._n == 0) or (self._n == 1):
            return self._n

        task = FibTask(self._executor, self._n - 2)
        task.fork()
        return FibTask(self._executor, self._n - 1)() + task.join()

def do_math(input) -> int:
    return input * input

if __name__ == '__main__':
    executer = ProcessPoolExecutor(max_workers=12)
    # future_result: Future[int] = executer.submit(do_math, 2)


    print(FibTask(executer, 5)())
    # future_result.add_done_callback(lambda f: )
