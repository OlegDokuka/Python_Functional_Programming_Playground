from typing import Callable


log_level = "debug"


def log_info(line: str):
    if log_level == "info":
        print(line)


if __name__ == '__main__':
    a = 1
    b = 2

    # add print('calc') or
    if log_level == "info":
        log_line = f"my evaluated string {print('calc') or b} + {a}"
        log_info(log_line)
