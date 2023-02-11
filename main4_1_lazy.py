from typing import Callable

log_level = "debug"


# def log_info(line: str):
#     if log_level == "info":
#         print(line)


# solution
def log_info(fn_line: Callable[[], str]):
    if log_level == "info":
        print(fn_line())


if __name__ == '__main__':
    a = 1
    b = 2

    log_info(lambda: f"my evaluated string {print('calc') or b} + {a}")
    # log_info(lambda: f"my evaluated string {print('calc') or b} + {a}")
