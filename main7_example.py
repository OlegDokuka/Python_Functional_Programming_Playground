class Vector:
    def __init__(self, *parts: int):
        self.parts = list[int](parts)

    def __add__(self, other: "Vector") -> "Vector":
        length = len(self.parts)
        if length == len(other.parts):
            self.parts = [self.parts[i] + other.parts[i] for i in range(0, length)]
            return self

        raise Exception(f"Incompatible length of vectors {self} and {other}")

    def __str__(self):
        return f"Vector([{', '.join([str(part) for part in self.parts])}])"


if __name__ == '__main__':
    vector1 = Vector(1, 2)
    vector2 = Vector(2, 3)
    vector3 = Vector(3, 5)
    print(f"before v1{vector1} v2{vector2} v3{vector3}")
    print(vector1 + vector2 + vector3)
    print(f"after v1{vector1} v2{vector2} v3{vector3}")
    print(vector1 + vector2 + vector3)
    print(f"after v1{vector1} v2{vector2} v3{vector3}")

