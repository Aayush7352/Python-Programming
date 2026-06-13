from typing import List, Dict


def basic_lambdas():
    """Basic lambda function usage."""
    print("=== Basic Lambdas ===")
    square = lambda x: x ** 2
    add = lambda a, b: a + b
    is_even = lambda x: x % 2 == 0

    print(f"  square(5) = {square(5)}")
    print(f"  add(10, 20) = {add(10, 20)}")
    print(f"  is_even(7) = {is_even(7)}")
    print(f"  is_even(8) = {is_even(8)}")


def lambdas_with_sorting():
    """Lambdas for custom sorting."""
    print("\n=== Lambdas for Sorting ===")
    students = [
        {"name": "Alice", "grade": 85, "age": 20},
        {"name": "Bob", "grade": 92, "age": 22},
        {"name": "Charlie", "grade": 78, "age": 19},
        {"name": "Diana", "grade": 95, "age": 21},
    ]

    by_grade = sorted(students, key=lambda s: s["grade"], reverse=True)
    print("  Sorted by grade (desc):")
    for s in by_grade:
        print(f"    {s['name']}: {s['grade']}")

    by_age = sorted(students, key=lambda s: s["age"])
    print("  Sorted by age:")
    for s in by_age:
        print(f"    {s['name']}: {s['age']}")


def lambdas_with_map_filter():
    """Lambdas with map and filter."""
    print("\n=== Lambdas with Map/Filter ===")
    numbers = list(range(1, 11))

    squared = list(map(lambda x: x ** 2, numbers))
    print(f"  Squares: {squared}")

    evens = list(filter(lambda x: x % 2 == 0, numbers))
    print(f"  Evens: {evens}")

    # Combining map and filter
    result = list(map(lambda x: x * 10, filter(lambda x: x % 3 == 0, numbers)))
    print(f"  Multiples of 3 * 10: {result}")


def lambdas_with_reduce():
    """Lambdas with reduce."""
    from functools import reduce
    print("\n=== Lambdas with Reduce ===")
    numbers = [1, 2, 3, 4, 5]

    total = reduce(lambda a, b: a + b, numbers)
    print(f"  Sum: {total}")

    product = reduce(lambda a, b: a * b, numbers)
    print(f"  Product: {product}")

    max_val = reduce(lambda a, b: a if a > b else b, numbers)
    print(f"  Max: {max_val}")


def lambdas_with_defaultdict():
    """Lambdas with defaultdict factory."""
    from collections import defaultdict
    print("\n=== Lambdas with defaultdict ===")
    words = ["apple", "banana", "apple", "cherry", "banana", "apple"]

    counter = defaultdict(lambda: 0)
    for word in words:
        counter[word] += 1
    print(f"  Counter: {dict(counter)}")

    grouped = defaultdict(lambda: [])
    for word in words:
        grouped[len(word)].append(word)
    print(f"  Grouped by length: {dict(grouped)}")


def lambdas_in_quick_operations():
    """Common lambda patterns."""
    print("\n=== Common Lambda Patterns ===")
    points = [(1, 2), (3, 1), (5, 4), (2, 3)]

    # Sort by sum of coordinates
    sorted_by_sum = sorted(points, key=lambda p: p[0] + p[1])
    print(f"  Sorted by sum: {sorted_by_sum}")

    # Sort by distance from origin
    sorted_by_dist = sorted(points, key=lambda p: p[0] ** 2 + p[1] ** 2)
    print(f"  Sorted by distance: {sorted_by_dist}")

    # Nested list sorting
    data = [[1, 3, 2], [2, 1, 3], [3, 2, 1]]
    sorted_by_second = sorted(data, key=lambda x: x[1])
    print(f"  Sorted by 2nd element: {sorted_by_second}")


def main():
    basic_lambdas()
    lambdas_with_sorting()
    lambdas_with_map_filter()
    lambdas_with_reduce()
    lambdas_with_defaultdict()
    lambdas_in_quick_operations()

    # Lambdas limitation
    print("\n=== Lambda Limitations ===")
    print("  Lambdas are limited to single expressions:")
    print("    Good: lambda x: x ** 2")
    print("    Bad:  lambda x: if x > 0: return x  # SyntaxError")
    print("  Use regular functions for complex logic")


if __name__ == "__main__":
    main()
