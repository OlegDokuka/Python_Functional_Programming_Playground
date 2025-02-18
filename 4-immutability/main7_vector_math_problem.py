class Vector[TVector : "Vector"]:
    def __init__(self, *parts: int):
        self.parts = list[int](parts)

    def __add__(self, other: TVector) -> TVector:
        length = len(self.parts)
        if length == len(other.parts):
            return Vector(*[self.parts[i] + other.parts[i] for i in range(0, length)])

        raise Exception(f"Incompatible length of vectors {self} and {other}")

    def __str__(self):
        return f"Vector([{', '.join([str(part) for part in self.parts])}])"

class Vector1(Vector["Vector1"]):
    def __init__(self, v1: int):
        super().__init__(v1)

class Vector2(Vector["Vector2"]):
    def __init__(self, v1: int, v2: int):
        super().__init__(v1, v2)
class Vector3(Vector["Vector3"]):
    def __init__(self, v1: int, v2: int, v3: int):
        super().__init__(v1, v2, v3)

if __name__ == '__main__':
    vector1 = Vector2(1, 2)
    vector2 = Vector2(2, 3)
    vector3 = Vector2(3, 5)
    print(f"before v1{vector1} v2{vector2} v3{vector3}")
    print(vector1 + vector2 + vector3)
    print(f"after v1{vector1} v2{vector2} v3{vector3}")
    print(vector1 + vector2 + vector3)
    print(f"after v1{vector1} v2{vector2} v3{vector3}")

