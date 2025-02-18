from functools import cache
from typing import Callable, Dict, Any



# @memoiz
def fib(n: int) -> int:
    return n if n < 2 else (fib(n - 1) + fib(n - 2))

if __name__ == '__main__':
    print(fib(100))
