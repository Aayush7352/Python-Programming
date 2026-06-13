import types
import time


class Calculator:
    """Simple calculator for monkey patching demos."""

    def add(self, a: float, b: float) -> float:
        return a + b

    def subtract(self, a: float, b: float) -> float:
        return a - b

    def multiply(self, a: float, b: float) -> float:
        return a * b

    def divide(self, a: float, b: float) -> float:
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b

    def all_operations(self, a: float, b: float) -> dict:
        return {
            "add": self.add(a, b),
            "subtract": self.subtract(a, b),
            "multiply": self.multiply(a, b),
            "divide": self.divide(a, b),
        }


def patch_method_replacement():
    """Replace a method on an instance."""
    print("=== Method Replacement on Instance ===")
    calc = Calculator()

    # Define a new method
    def patched_add(self, a, b):
        return a + b + 1  # off by one

    calc.add = types.MethodType(patched_add, calc)
    print(f"  Patched add: 2 + 3 = {calc.add(2, 3)} (expected 5 + 1 = 6)")


def patch_class_method():
    """Patch a method on the entire class."""
    print("\n=== Patch Class Method ===")
    def safe_divide(self, a, b):
        if b == 0:
            return float("inf")
        return a / b

    Calculator.divide = safe_divide

    calc = Calculator()
    print(f"  Safe divide: 10 / 0 = {calc.divide(10, 0)} (instead of error)")


def patch_with_monkey():
    """Monkey patch to add logging."""
    print("\n=== Add Logging via Monkey Patch ===")

    original_add = Calculator.add

    def logged_add(self, a, b):
        result = original_add(self, a, b)
        print(f"  LOG: add({a}, {b}) = {result}")
        return result

    Calculator.add = logged_add

    calc = Calculator()
    calc.add(3, 4)


def patch_at_runtime():
    """Monkey patch while code is running."""
    print("\n=== Runtime Monkey Patch ===")

    def timer_decorator(func):
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            elapsed = time.perf_counter() - start
            print(f"  TIMER: {func.__name__} took {elapsed:.6f}s")
            return result
        return wrapper

    # Apply timer to all Calculator methods
    for attr_name in dir(Calculator):
        if not attr_name.startswith("_") and callable(getattr(Calculator, attr_name)):
            original = getattr(Calculator, attr_name)
            setattr(Calculator, attr_name, timer_decorator(original))

    calc = Calculator()
    print(f"  Result: {calc.all_operations(10, 3)}")


def patch_builtin_or_thirdparty():
    """Monkey patching external modules (use carefully)."""
    print("\n=== Patching External Modules ===")
    import math

    original_sqrt = math.sqrt

    def patched_sqrt(x):
        if x < 0:
            raise ValueError(f"Cannot sqrt negative number: {x}")
        return original_sqrt(x)

    math.sqrt = patched_sqrt
    print(f"  sqrt(16) = {math.sqrt(16)}")

    try:
        math.sqrt(-1)
    except ValueError as e:
        print(f"  Patched sqrt(-1) error: {e}")

    # Restore
    math.sqrt = original_sqrt


def main():
    patch_method_replacement()
    patch_class_method()
    patch_with_monkey()
    patch_at_runtime()
    patch_builtin_or_thirdparty()

    print("\n=== Monkey Patching Considerations ===")
    print("  - Useful for testing (mocking)")
    print("  - Can be dangerous in production")
    print("  - Makes code harder to understand")
    print("  - Use context managers for temporary patches")
    print("  - Prefer dependency injection when possible")


if __name__ == "__main__":
    main()
