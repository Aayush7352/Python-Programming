import sys


def divide_numbers(a: float, b: float) -> float:
    """Divide with error handling."""
    try:
        result = a / b
    except ZeroDivisionError:
        print(f"  Error: Cannot divide {a} by zero!")
        return float("inf")
    except TypeError as e:
        print(f"  Error: Invalid types: {e}")
        raise
    else:
        print(f"  Division successful: {a} / {b} = {result}")
        return result
    finally:
        print(f"  (Finally: cleanup in divide_numbers)")


def parse_integer(value: str) -> int:
    """Parse integer with multiple exception handlers."""
    try:
        return int(value)
    except ValueError:
        print(f"  Error: '{value}' is not a valid integer")
        return 0
    except (TypeError, OverflowError) as e:
        print(f"  Error: {type(e).__name__}: {e}")
        return -1


def read_file_safe(filepath: str) -> str:
    """Read file with comprehensive error handling."""
    try:
        with open(filepath, "r") as f:
            return f.read()
    except FileNotFoundError:
        print(f"  Error: File '{filepath}' not found")
        return ""
    except PermissionError:
        print(f"  Error: Permission denied reading '{filepath}'")
        return ""
    except IsADirectoryError:
        print(f"  Error: '{filepath}' is a directory")
        return ""
    except Exception as e:
        print(f"  Unexpected error: {type(e).__name__}: {e}")
        return ""


def nested_exception_handling():
    """Demonstrate nested try-except blocks."""
    print("  Outer try block")
    try:
        print("  Inner try block")
        try:
            result = 10 / 0
        except ZeroDivisionError:
            print("  Inner handler: caught division by zero")
            raise  # Re-raise to outer
    except ZeroDivisionError:
        print("  Outer handler: also caught the re-raised exception")


def exception_chaining():
    """Demonstrate exception chaining with 'raise from'."""
    try:
        try:
            int("not_a_number")
        except ValueError as original:
            raise RuntimeError("Failed to parse input") from original
    except RuntimeError as e:
        print(f"  Chained exception: {e}")
        print(f"  Original cause: {e.__cause__}")


def main():
    print("=== Basic Try-Except ===")
    divide_numbers(10, 2)
    divide_numbers(10, 0)

    print("\n=== Multiple Exception Types ===")
    print(f"  Parsed '123': {parse_integer('123')}")
    print(f"  Parsed 'abc': {parse_integer('abc')}")

    print("\n=== File Error Handling ===")
    read_file_safe("/tmp/nonexistent.txt")
    print(f"  Current exception info: {sys.exc_info()[0] if sys.exc_info()[0] else 'None'}")

    print("\n=== Nested Exception Handling ===")
    nested_exception_handling()

    print("\n=== Exception Chaining ===")
    exception_chaining()

    print("\n=== Try-Else-Finally ===")
    for value in ["42", "abc"]:
        try:
            num = int(value)
        except ValueError as e:
            print(f"  Error: {e}")
        else:
            print(f"  Successfully parsed: {num}")
        finally:
            print("  Finally block always executes")


if __name__ == "__main__":
    main()
