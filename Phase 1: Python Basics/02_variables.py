def main():
    name = "Alice"
    age = 25
    height = 5.6
    is_student = True

    print(f"Name: {name}, Type: {type(name)}")
    print(f"Age: {age}, Type: {type(age)}")
    print(f"Height: {height}, Type: {type(height)}")
    print(f"Is Student: {is_student}, Type: {type(is_student)}")

    a = b = c = 100
    x, y, z = 1, 2, 3
    print(f"Multiple assignment: a={a}, b={b}, c={c}")
    print(f"Tuple unpacking: x={x}, y={y}, z={z}")


if __name__ == "__main__":
    main()
