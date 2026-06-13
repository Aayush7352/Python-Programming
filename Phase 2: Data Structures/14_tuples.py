def main():
    # Creating tuples
    empty = ()
    single = (5,)  # trailing comma is required
    numbers = (1, 2, 3, 4, 5)
    mixed = (1, "hello", 3.14)
    nested = ((1, 2), (3, 4))
    constructed = tuple("python")
    without_parens = 1, 2, 3  # tuple packing

    print("=== Creating Tuples ===")
    print(f"Empty: {empty}")
    print(f"Single element: {single}")
    print(f"Numbers: {numbers}")
    print(f"Mixed: {mixed}")
    print(f"Nested: {nested}")
    print(f"From string: {constructed}")
    print(f"Tuple packing: {without_parens}")

    # Tuple indexing and slicing
    print("\n=== Indexing and Slicing ===")
    print(f"First: {numbers[0]}, Last: {numbers[-1]}")
    print(f"Slice [1:3]: {numbers[1:3]}")
    print(f"Reverse: {numbers[::-1]}")

    # Tuple unpacking
    print("\n=== Tuple Unpacking ===")
    a, b, c = (10, 20, 30)
    print(f"a={a}, b={b}, c={c}")
    head, *tail = [1, 2, 3, 4, 5]
    print(f"head={head}, tail={tail}")
    *first, last = (1, 2, 3, 4, 5)
    print(f"first={first}, last={last}")

    # Named tuples
    print("\n=== Named Tuples ===")
    from collections import namedtuple
    Point = namedtuple("Point", ["x", "y"])
    p = Point(10, 20)
    print(f"Point: {p}")
    print(f"p.x = {p.x}, p[0] = {p[0]}")
    print(f"p.y = {p.y}, p[1] = {p[1]}")
    x, y = p
    print(f"Unpacked: x={x}, y={y}")

    # Tuple immutability
    print("\n=== Tuple Immutability ===")
    t = (1, 2, 3)
    print(f"Tuple: {t}")
    print("Tuples are immutable - cannot change elements")
    print("But if tuple contains mutable objects, those can change:")
    t2 = ([1, 2], [3, 4])
    t2[0].append(99)
    print(f"After modifying inner list: {t2}")

    # Tuple methods
    print(f"\n=== Tuple Methods ===")
    print(f"Count of 2: {(1, 2, 2, 3, 2).count(2)}")
    print(f"Index of 3: {(1, 2, 3, 4).index(3)}")
    print(f"Length: {len((1, 2, 3))}")


if __name__ == "__main__":
    main()
