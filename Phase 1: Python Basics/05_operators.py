def main():
    a, b = 10, 3

    # Arithmetic operators
    print("=== Arithmetic Operators ===")
    print(f"{a} + {b} = {a + b}")
    print(f"{a} - {b} = {a - b}")
    print(f"{a} * {b} = {a * b}")
    print(f"{a} / {b} = {a / b}")
    print(f"{a} // {b} = {a // b} (floor division)")
    print(f"{a} % {b} = {a % b} (modulus)")
    print(f"{a} ** {b} = {a ** b} (exponentiation)")

    # Comparison operators
    print("\n=== Comparison Operators ===")
    print(f"{a} == {b}: {a == b}")
    print(f"{a} != {b}: {a != b}")
    print(f"{a} > {b}: {a > b}")
    print(f"{a} < {b}: {a < b}")
    print(f"{a} >= {b}: {a >= b}")
    print(f"{a} <= {b}: {a <= b}")

    # Logical operators
    print("\n=== Logical Operators ===")
    print(f"True and False: {True and False}")
    print(f"True or False: {True or False}")
    print(f"not True: {not True}")

    # Bitwise operators
    print("\n=== Bitwise Operators ===")
    print(f"{a} & {b} = {a & b} (AND)")
    print(f"{a} | {b} = {a | b} (OR)")
    print(f"{a} ^ {b} = {a ^ b} (XOR)")
    print(f"~{a} = {~a} (NOT)")
    print(f"{a} << 1 = {a << 1} (left shift)")
    print(f"{a} >> 1 = {a >> 1} (right shift)")

    # Assignment operators
    print("\n=== Assignment Operators ===")
    x = 5
    x += 3; print(f"x += 3: {x}")
    x -= 2; print(f"x -= 2: {x}")
    x *= 4; print(f"x *= 4: {x}")

    # Identity & Membership
    print("\n=== Identity & Membership ===")
    print(f"a is b: {a is b}")
    print(f"3 in [1,2,3,4,5]: {3 in [1, 2, 3, 4, 5]}")


if __name__ == "__main__":
    main()
