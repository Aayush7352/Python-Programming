def main():
    # List comprehensions
    print("=== List Comprehensions ===")
    squares = [x ** 2 for x in range(10)]
    print(f"Squares: {squares}")

    evens = [x for x in range(20) if x % 2 == 0]
    print(f"Evens: {evens}")

    # Nested list comprehension
    matrix = [[i * j for j in range(1, 4)] for i in range(1, 4)]
    print(f"Multiplication table: {matrix}")

    # With if-else
    parity = ["even" if x % 2 == 0 else "odd" for x in range(10)]
    print(f"Parity: {parity}")

    # Flattening
    nested = [[1, 2], [3, 4], [5, 6]]
    flat = [item for sublist in nested for item in sublist]
    print(f"Flattened: {flat}")

    # Dictionary comprehensions
    print("\n=== Dictionary Comprehensions ===")
    squares_dict = {x: x ** 2 for x in range(6)}
    print(f"Squares dict: {squares_dict}")

    even_squares = {x: x ** 2 for x in range(10) if x % 2 == 0}
    print(f"Even squares: {even_squares}")

    # Swapping keys and values
    original = {"a": 1, "b": 2, "c": 3}
    swapped = {v: k for k, v in original.items()}
    print(f"Swapped: {swapped}")

    # Set comprehensions
    print("\n=== Set Comprehensions ===")
    unique_lengths = {len(word) for word in ["hello", "world", "python", "code"]}
    print(f"Unique lengths: {unique_lengths}")

    even_set = {x for x in range(20) if x % 2 == 0}
    print(f"Even set: {even_set}")

    # Generator expression (memory efficient)
    print("\n=== Generator Expressions ===")
    gen = (x ** 2 for x in range(10))
    print(f"Generator type: {type(gen)}")
    print(f"Generator as list: {list(gen)}")

    # Performance comparison
    import sys
    list_comp = [x for x in range(10000)]
    gen_expr = (x for x in range(10000))
    print(f"\nList size: {sys.getsizeof(list_comp)} bytes")
    print(f"Generator size: {sys.getsizeof(gen_expr)} bytes")


if __name__ == "__main__":
    main()
