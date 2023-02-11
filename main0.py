# write fn

def sum(val_1: int, val_2: int) -> int:
    return val_1 + val_2


lamda_sum = lambda x, y: x + y

if __name__ == '__main__':
    print(sum(1, 2))
    print(lamda_sum(1, 2))
