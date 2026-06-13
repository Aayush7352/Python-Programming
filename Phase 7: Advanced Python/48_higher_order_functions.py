from typing import Callable, List, Any


def apply_twice(func: Callable, x: Any) -> Any:
    """Higher-order function: applies func twice."""
    return func(func(x))


def create_pipeline(*funcs: Callable) -> Callable:
    """Creates a function pipeline (composition left-to-right)."""
    def pipeline(x: Any) -> Any:
        result = x
        for func in funcs:
            result = func(result)
        return result
    return pipeline


def map_filter_reduce_example():
    """Demonstrate map, filter, reduce as HOFs."""
    from functools import reduce
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    # map
    squared = list(map(lambda x: x ** 2, numbers))
    print(f"  Map (squared): {squared}")

    # filter
    evens = list(filter(lambda x: x % 2 == 0, numbers))
    print(f"  Filter (evens): {evens}")

    # reduce
    total = reduce(lambda a, b: a + b, numbers)
    print(f"  Reduce (sum): {total}")

    # Combined
    result = reduce(
        lambda a, b: a + b,
        map(lambda x: x ** 2,
            filter(lambda x: x % 2 == 0, numbers))
    )
    print(f"  Combined (sum of squares of evens): {result}")


def partial_application():
    """Demonstrate partial application."""
    from functools import partial

    def power(base: float, exponent: float) -> float:
        return base ** exponent

    square = partial(power, exponent=2)
    cube = partial(power, exponent=3)

    print(f"  square(5) = {square(5)}")
    print(f"  cube(5) = {cube(5)}")

    # Real-world: partial for file writing
    def log(level: str, message: str) -> str:
        return f"[{level.upper()}] {message}"

    info = partial(log, "info")
    error = partial(log, "error")
    print(f"  {info('Server started')}")
    print(f"  {error('Connection timeout')}")


def function_as_return_value():
    """Return functions from other functions."""
    def get_operation(op: str) -> Callable:
        operations = {
            "add": lambda x, y: x + y,
            "subtract": lambda x, y: x - y,
            "multiply": lambda x, y: x * y,
            "divide": lambda x, y: x / y if y != 0 else float("inf"),
        }
        return operations.get(op, lambda x, y: None)

    add = get_operation("add")
    print(f"  add(10, 5) = {add(10, 5)}")
    multiply = get_operation("multiply")
    print(f"  multiply(10, 5) = {multiply(10, 5)}")


def decorator_as_hof():
    """Decorator is a higher-order function."""
    def uppercase(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            return result.upper() if isinstance(result, str) else result
        return wrapper

    @uppercase
    def greet(name: str) -> str:
        return f"Hello, {name}!"

    print(f"  {greet('Alice')}")


def main():
    print("=== apply_twice ===")
    result = apply_twice(lambda x: x * 2, 5)
    print(f"  apply_twice(double, 5) = {result}")

    print("\n=== Function Pipeline ===")
    pipeline = create_pipeline(
        lambda x: x + 1,
        lambda x: x * 2,
        lambda x: x ** 2,
    )
    print(f"  pipeline(3) = (3+1)*2 then squared = {pipeline(3)}")

    print("\n=== Map, Filter, Reduce ===")
    map_filter_reduce_example()

    print("\n=== Partial Application ===")
    partial_application()

    print("\n=== Function as Return Value ===")
    function_as_return_value()

    print("\n=== Decorator as HOF ===")
    decorator_as_hof()

    # Sorting with key functions
    print("\n=== Sorting with Key Functions ===")
    words = ["apple", "banana", "cherry", "date", "elderberry"]
    sorted_by_length = sorted(words, key=len)
    print(f"  Sorted by length: {sorted_by_length}")
    sorted_by_last = sorted(words, key=lambda w: w[-1])
    print(f"  Sorted by last char: {sorted_by_last}")


if __name__ == "__main__":
    main()
