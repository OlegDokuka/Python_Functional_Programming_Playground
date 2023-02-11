# refactor me to functional

# def square(x: list[int]) -> list[int]:
#     res = []
#     for index in range(len(x)):
#         res.append(x[index] ** 2)
#
#     return res


# solution


# def square(data_source: list[int]) -> list[int]:
#     return [i ** 2 for i in data_source]


def square(x: list[int]) -> list[int]:
    return list(map(lambda i: i ** 2, x))


if __name__ == '__main__':
    arr = [1, 2, 3]
    print(square(arr))
    print(square(arr))
