# write fn
from typing import Callable, Any

def sum(val_1: int, val_2: int) -> int:
    return val_1 + val_2


lambda_sum: Callable[[int, int], int] = lambda x, y: x + y

if __name__ == '__main__':
    print(sum(1, 2))
    print(lambda_sum(1, 2))
