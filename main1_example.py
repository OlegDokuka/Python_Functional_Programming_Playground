# bad examples

factor = 2


def square_impure_1(x: list[int]) -> list[int]:
    res = []
    for index in range(len(x)):
        res.append(x[index] ** factor)

    return res


def square_impure_2(x: list[int]) -> list[int]:
    for index in range(len(x)):
        x[index] = x[index] ** 2

    return x

# refactor me to functional

def square(x: list[int]) -> list[int]:
    res = [] #assignment
    for index in range(len(x)):
        res.append(x[index] ** 2)

    return res


if __name__ == '__main__':
    # print(square_impure_1([1, 2, 3]))
    # factor = 3
    # print(square_impure_1([1, 2, 3]))

    arr = [1, 2, 3]
    print(square_impure_2(arr))
    print(square_impure_2(arr))
