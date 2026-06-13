def main():
    # Basic input
    name = input("Enter your name: ")
    age = int(input("Enter your age: "))

    # Formatted output
    print(f"\nHello, {name}!")
    print(f"You are {age} years old.")
    print(f"Next year you will be {age + 1}.")

    # Different print styles
    print("\n=== Print Styles ===")
    print("Concatenation: " + name + " is " + str(age))
    print("Format method: {} is {}".format(name, age))
    print("F-string: {name} is {age}")
    print("Repr: {!r}".format(name))
    print("Str: {!s}".format(name))

    # Formatted string specifiers
    pi = 3.1415926535
    print(f"\nPi to 2 decimals: {pi:.2f}")
    print(f"Pi to 4 decimals: {pi:.4f}")
    print(f"Percentage: {0.856:.1%}")
    print(f"Left padded: {name:<10}|")
    print(f"Right padded: {name:>10}|")
    print(f"Center: {name:^10}|")


if __name__ == "__main__":
    main()
