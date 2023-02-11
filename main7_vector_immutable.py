# class Vector:
#     def __init__(self, *parts: int):
#         self.parts = list[int](parts)
#
#     def __add__(self, other: "Vector") -> "Vector":
#         length = len(self.parts)
#         if length == len(other.parts):
#             self.parts = [self.parts[i] + other.parts[i] for i in range(0, length)]
#             return self
#
#         raise Exception(f"Incompatible length of vectors {self} and {other}")
#
#     def __str__(self):
#         return f"Vector([{', '.join([str(part) for part in self.parts])}])"
from typing import Generic, TypeVar


# solution 2
T = TypeVar('T', bound='Vector')


class Vector(Generic[T]):
    def __init__(self, *parts: int):
        self.parts = parts

    def __add__(self, other: T) -> T:
        length = len(self.parts)
        if length == len(other.parts):
            return self.__factory__(*(self.parts[i] + other.parts[i] for i in range(0, length)))

        raise Exception(f"Incompatible length of vectors {self} and {other}")

    def __factory__(self, *parts: int) -> T:
        raise Exception("N/I")

    def __str__(self):
        return f"Vector([{', '.join([str(part) for part in self.parts])}])"


class Vector2(Vector["Vector2"]):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)

    def __factory__(self, *parts: int) -> "Vector2":
        return Vector2(parts[0], parts[1])


class Vector3(Vector["Vector3"]):
    def __init__(self, x: int, y: int, z: int):
        super().__init__(x, y, z)

    def __factory__(self, *parts: int) -> "Vector3":
        return Vector3(parts[0], parts[1], parts[2])


if __name__ == '__main__':
    vector1 = Vector2(1, 2)
    vector2 = Vector2(2, 3)
    vector3 = Vector2(3, 5)
    print(f"before v1{vector1} v2{vector2} v3{vector3}")
    print(vector1 + vector2 + vector3)
    print(f"after v1{vector1} v2{vector2} v3{vector3}")
    print(vector1 + vector2 + vector3)
    print(f"after v1{vector1} v2{vector2} v3{vector3}")
