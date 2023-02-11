# refactor to functional

# def fib(n: int) -> int:
#     if n == 0:
#         return 0
#
#     current = 1
#     previous = 0
#
#     for i in range(1, n):
#         old_current = current
#         current += previous
#         previous = old_current
#
#     return current


# solution
def fib(n: int) -> int:
    return n if n < 2 else (fib(n - 1) + fib(n - 2))


if __name__ == '__main__':
    print(fib(10))
