def main():
    # Creating dictionaries
    empty = {}
    person = {"name": "Alice", "age": 30, "city": "New York"}
    constructed = dict(name="Bob", age=25, city="London")
    pairs = dict([("a", 1), ("b", 2), ("c", 3)])
    comprehension = {x: x ** 2 for x in range(6)}
    from_keys = dict.fromkeys(["a", "b", "c"], 0)

    print("=== Creating Dictionaries ===")
    print(f"Empty: {empty}")
    print(f"Person: {person}")
    print(f"Constructed: {constructed}")
    print(f"From pairs: {pairs}")
    print(f"Comprehension: {comprehension}")
    print(f"From keys: {from_keys}")

    # Accessing values
    print("\n=== Accessing Values ===")
    print(f"person['name']: {person['name']}")
    print(f"person.get('age'): {person.get('age')}")
    print(f"person.get('salary', 'Not found'): {person.get('salary', 'Not found')}")

    # Modifying dictionaries
    print("\n=== Modifying Dictionaries ===")
    d = {"a": 1, "b": 2}
    d["c"] = 3; print(f"After d['c'] = 3: {d}")
    d.update({"d": 4, "e": 5}); print(f"After update: {d}")
    d.setdefault("f", 6); print(f"After setdefault('f', 6): {d}")
    d.setdefault("a", 99); print(f"setdefault existing key: {d}")
    val = d.pop("a"); print(f"After pop('a'): {d}, popped: {val}")
    last = d.popitem(); print(f"After popitem(): {d}, popped: {last}")
    del d["b"]; print(f"After del d['b']: {d}")

    # Iterating
    print("\n=== Iterating ===")
    person = {"name": "Alice", "age": 30, "city": "New York"}
    for key in person:
        print(f"Key: {key}")
    for key, value in person.items():
        print(f"{key}: {value}")
    for value in person.values():
        print(f"Value: {value}")

    # Dictionary views
    print("\n=== Dictionary Views ===")
    keys = person.keys()
    values = person.values()
    items = person.items()
    print(f"Keys: {list(keys)}")
    print(f"Values: {list(values)}")
    print(f"Items: {list(items)}")
    person["country"] = "USA"
    print(f"Keys after adding: {list(keys)}")  # views are dynamic

    # Merging (Python 3.9+)
    d1 = {"a": 1, "b": 2}
    d2 = {"c": 3, "d": 4}
    merged = d1 | d2
    print(f"\nMerged (| operator): {merged}")

    # defaultdict and Counter
    from collections import defaultdict, Counter
    word_count = Counter("mississippi")
    print(f"\nCounter: {word_count}")
    print(f"Most common: {word_count.most_common(2)}")


if __name__ == "__main__":
    main()
