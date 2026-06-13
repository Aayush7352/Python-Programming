class Vector:
    """A 2D vector demonstrating magic methods."""

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    # String representations
    def __str__(self) -> str:
        return f"Vector({self.x}, {self.y})"

    def __repr__(self) -> str:
        return f"Vector({self.x!r}, {self.y!r})"

    # Arithmetic
    def __add__(self, other: "Vector") -> "Vector":
        if not isinstance(other, Vector):
            return NotImplemented
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Vector") -> "Vector":
        if not isinstance(other, Vector):
            return NotImplemented
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float) -> "Vector":
        return Vector(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar: float) -> "Vector":
        return self.__mul__(scalar)

    def __neg__(self) -> "Vector":
        return Vector(-self.x, -self.y)

    def __abs__(self) -> float:
        return (self.x ** 2 + self.y ** 2) ** 0.5

    # Comparison
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vector):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __lt__(self, other: "Vector") -> bool:
        if not isinstance(other, Vector):
            return NotImplemented
        return abs(self) < abs(other)

    # Container
    def __len__(self) -> int:
        return 2  # 2D vector

    def __getitem__(self, index: int) -> float:
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        raise IndexError(f"Vector index {index} out of range")

    def __iter__(self):
        return iter((self.x, self.y))

    # Callable
    def __call__(self, scale: float = 1.0) -> "Vector":
        return Vector(self.x * scale, self.y * scale)

    # Context manager
    def __enter__(self):
        print(f"Entering context with {self}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"Exiting context with {self}")
        return False


def main():
    print("=== Magic Methods ===")
    v1 = Vector(3, 4)
    v2 = Vector(1, 2)

    print(f"str: {str(v1)}")
    print(f"repr: {repr(v1)}")
    print(f"abs: {abs(v1):.2f}")
    print(f"v1 + v2 = {v1 + v2}")
    print(f"v1 - v2 = {v1 - v2}")
    print(f"v1 * 3 = {v1 * 3}")
    print(f"3 * v1 = {3 * v1}")
    print(f"-v1 = {-v1}")
    print(f"v1 == Vector(3,4): {v1 == Vector(3, 4)}")
    print(f"v1 < v2: {v1 < v2}")
    print(f"len(v1): {len(v1)}")
    print(f"v1[0]: {v1[0]}, v1[1]: {v1[1]}")
    print(f"list(v1): {list(v1)}")
    print(f"v1(2) (calling): {v1(2)}")

    print("\n=== Context Manager ===")
    with Vector(10, 20) as v:
        print(f"  Inside context: {v}")

    print("\n=== Hash and Membership ===")
    v = Vector(3, 4)
    print(f"hash: {hash(v)}")
    s = {v, Vector(1, 2), Vector(3, 4)}
    print(f"Set with vectors: {s}")
    print(f"Vector(3,4) in set? {Vector(3, 4) in s}")


if __name__ == "__main__":
    main()
