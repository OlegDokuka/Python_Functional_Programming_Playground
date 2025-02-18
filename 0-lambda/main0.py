# write fn
from typing import Callable, Any, List

def sum(list : List[int]) -> int:
    res =list[0] + list[1]
    list.insert(0, res)
    return res


lambda_sum: Callable[[int, int], int] = lambda x, y: x + y

if __name__ == '__main__':
    list = [1, 2]
    print(sum(list))
    print(sum(list))
    print(sum(list))
    print(lambda_sum(1, 2))
