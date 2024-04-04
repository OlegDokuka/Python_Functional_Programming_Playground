from multiprocessing import Process, Queue
import math

PRIMES = [
    112272535095293,
    112582705942171,
    112272535095293,
    115280095190773,
    115797848077099,
    1099726899285419]


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


def worker(input_queue: Queue, output_queue: Queue):
    while True:
        val = input_queue.get()
        output_queue.put((val, is_prime(val)))


def main():
    results = Queue()
    workers = [(Process(target=worker, args=(q, results,)), q) for q in [Queue() for _ in range(4)]]

    for (w, _) in workers:
        w.start()

    for i in range(len(PRIMES)):
        (_, q) = workers[i % len(workers)]
        q.put(PRIMES[i])

    while True:
        print(results.get())


if __name__ == '__main__':
    main()
