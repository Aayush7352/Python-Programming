def main():
    # Creating sets
    empty = set()
    numbers = {1, 2, 3, 4, 5}
    mixed = {1, "hello", 3.14}
    constructed = set("mississippi")
    comprehension = {x ** 2 for x in range(10)}

    print("=== Creating Sets ===")
    print(f"Empty set: {empty}")
    print(f"Numbers: {numbers}")
    print(f"From string (unique chars): {constructed}")
    print(f"Comprehension: {comprehension}")

    # Set operations
    print("\n=== Set Operations ===")
    a = {1, 2, 3, 4, 5}
    b = {4, 5, 6, 7, 8}

    print(f"A: {a}")
    print(f"B: {b}")
    print(f"Union (A | B): {a | b}")
    print(f"Union (A.union(B)): {a.union(b)}")
    print(f"Intersection (A & B): {a & b}")
    print(f"Intersection (A.intersection(B)): {a.intersection(b)}")
    print(f"Difference (A - B): {a - b}")
    print(f"Difference (A.difference(B)): {a.difference(b)}")
    print(f"Symmetric diff (A ^ B): {a ^ b}")
    print(f"Symmetric diff (A.symmetric_difference(B)): {a.symmetric_difference(b)}")

    # Set modification
    print("\n=== Set Modification ===")
    s = {1, 2, 3}
    s.add(4); print(f"After add(4): {s}")
    s.update([5, 6]); print(f"After update([5,6]): {s}")
    s.remove(3); print(f"After remove(3): {s}")
    s.discard(10); print(f"After discard(10) (no error): {s}")
    popped = s.pop(); print(f"After pop(): {s}, popped: {popped}")
    s.clear(); print(f"After clear(): {s}")

    # Set comparisons
    print("\n=== Set Comparisons ===")
    a = {1, 2, 3, 4}
    b = {1, 2}
    print(f"A: {a}, B: {b}")
    print(f"B is subset of A: {b.issubset(a)}")
    print(f"A is superset of B: {a.issuperset(b)}")
    print(f"Are A and B disjoint? {a.isdisjoint({5, 6})}")

    # Frozenset
    print("\n=== Frozenset ===")
    fs = frozenset([1, 2, 3, 4, 5])
    print(f"Frozenset: {fs}")
    print("Frozenset is immutable - cannot add/remove elements")
    print(f"Can still do set operations: fs | {6, 7} = {fs | {6, 7}}")


if __name__ == "__main__":
    main()
