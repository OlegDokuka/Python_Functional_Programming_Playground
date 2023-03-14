import time
from threading import current_thread, Lock

import reactivex
from reactivex import operators as ops, Observable


def main():
    source: Observable[int] = reactivex.interval(1)  # type: ignore
    (source.pipe(ops.map(lambda x: str(x * 100)),
                 ops.take(10),
                 ops.do_action(on_next=print),
                 ops.flat_map(lambda i: reactivex.of(i).pipe(ops.delay(2))),
                 ops.do_action(on_next=print),
                 ops.filter(lambda x: len(x) > 2),
                 ).subscribe(on_next=print))

    time.sleep(50)  # sleep for 5 seconds


if __name__ == '__main__':
    main()
