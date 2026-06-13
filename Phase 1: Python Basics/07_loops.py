def main():
    # For loop with range
    print("=== For Loop with Range ===")
    for i in range(5):
        print(f"Count: {i}")

    # For loop with list
    print("\n=== For Loop with List ===")
    fruits = ["apple", "banana", "cherry"]
    for fruit in fruits:
        print(f"Fruit: {fruit}")

    # For loop with enumerate
    print("\n=== For Loop with Enumerate ===")
    for index, fruit in enumerate(fruits):
        print(f"{index}: {fruit}")

    # For loop with dictionary
    print("\n=== For Loop with Dictionary ===")
    grades = {"Alice": 85, "Bob": 92, "Charlie": 78}
    for name, grade in grades.items():
        print(f"{name}: {grade}")

    # While loop
    print("\n=== While Loop ===")
    count = 0
    while count < 5:
        print(f"Count: {count}")
        count += 1

    # Break and Continue
    print("\n=== Break and Continue ===")
    for i in range(10):
        if i == 3:
            print("Skipping 3 (continue)")
            continue
        if i == 7:
            print("Stopping at 7 (break)")
            break
        print(f"Number: {i}")

    # Nested loops
    print("\n=== Nested Loops ===")
    for i in range(1, 4):
        for j in range(1, 4):
            print(f"{i} * {j} = {i * j:2d}", end="  ")
        print()

    # Else clause on loops
    print("\n=== For-Else ===")
    for i in range(3):
        print(f"Loop iteration: {i}")
    else:
        print("Loop completed without break!")


if __name__ == "__main__":
    main()
