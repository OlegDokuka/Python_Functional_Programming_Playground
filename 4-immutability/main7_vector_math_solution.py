# class Vector:
#     def __init__(self, *parts: int):
#         self.parts = list[int](parts)
#
#     def __add__(self, other: "Vector") -> "Vector":
#         length = len(self.parts)
#         if length == len(other.parts):
#             return Vector(*[self.parts[i] + other.parts[i] for i in range(0, length)])
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
            inst = object.__new__(self.__class__)
            inst.__init__(*(self.parts[i] + other.parts[i] for i in range(0, length)))
            return inst

        raise Exception(f"Incompatible length of vectors {self} and {other}")

    def __str__(self):
        return f"{self.__class__.__name__}([{', '.join([str(part) for part in self.parts])}])"


class Vector2(Vector["Vector2"]):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)


class Vector3(Vector["Vector3"]):
    def __init__(self, x: int, y: int, z: int):
        super().__init__(x, y, z)


if __name__ == '__main__':
    vector1 = Vector2(1, 2)
    vector2 = Vector2(2, 3)
    vector3 = Vector2(3, 5)
    vector4_3 = Vector3(3, 5, 6)
    print(f"before v1{vector1} v2{vector2} v3{vector3}")
    print(vector1 + vector2 + vector3)
    print(f"after v1{vector1} v2{vector2} v3{vector3}")
    print(vector1 + vector2 + vector3)
    print(f"after v1{vector1} v2{vector2} v3{vector3}")
    try:
        print(vector1 + vector2 + vector4_3)
    except Exception as e:
        print("expectedly failed")
