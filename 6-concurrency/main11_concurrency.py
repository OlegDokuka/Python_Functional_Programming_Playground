import concurrent.futures
import multiprocessing
import math
import time
from typing import Iterable

PRIMES1 = [
    112272535095293,
    112582705942171,
    112272535095293,
    115280095190773,
    115797848077099,
    1099726899285419]


PRIMES2 = [
    1,
    2,
    3,
    4,
    6,
    7]

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


def data_set_prime_checking(values: Iterable[int]) -> Iterable[bool]:
    return [is_prime(value) for value in values]


def main():
    start = time.time_ns()


    with concurrent.futures.ProcessPoolExecutor(2) as executor:

        for numbers, primes in zip([PRIMES2, ], executor.map(data_set_prime_checking, [PRIMES2, ])):
            for number, prime in zip(numbers, primes):
                print('%d is prime: %s' % (number, prime))



    print(f"time taken {(time.time_ns() - start) / 1000000} ms")

if __name__ == '__main__':
    main()