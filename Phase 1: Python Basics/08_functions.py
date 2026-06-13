def greet(name: str) -> str:
    """Simple greeting function."""
    return f"Hello, {name}!"


def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b


def divide(a: float, b: float) -> float:
    """Divide a by b, with zero check."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


def process_items(*args, **kwargs) -> None:
    """Function with variable arguments."""
    print(f"Positional args (*args): {args}")
    print(f"Keyword args (**kwargs): {kwargs}")


def create_multiplier(factor: float):
    """Closure: returns a function that multiplies by factor."""
    def multiply(x: float) -> float:
        return x * factor
    return multiply


def main():
    # Basic function calls
    print("=== Basic Functions ===")
    print(greet("Alice"))
    print(f"5 + 3 = {add(5, 3)}")
    print(f"10 / 3 = {divide(10, 3):.2f}")

    # Variable arguments
    print("\n=== Variable Arguments ===")
    process_items(1, 2, 3, name="Alice", age=25)

    # Closure
    print("\n=== Closure ===")
    double = create_multiplier(2)
    triple = create_multiplier(3)
    print(f"Double 5: {double(5)}")
    print(f"Triple 5: {triple(5)}")

    # Lambda (anonymous) function
    square = lambda x: x ** 2
    print(f"\n=== Lambda ===")
    print(f"Square of 7: {square(7)}")

    # Default and keyword arguments
    def power(base: float, exp: float = 2) -> float:
        return base ** exp

    print(f"\n=== Default & Keyword Args ===")
    print(f"Power 3^2: {power(3)}")
    print(f"Power 2^10: {power(2, 10)}")
    print(f"Power with keyword: {power(exp=3, base=5)}")

    # Docstring
    print(f"\n=== Docstring ===")
    print(greet.__doc__)


if __name__ == "__main__":
    main()
