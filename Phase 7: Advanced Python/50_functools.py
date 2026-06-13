import functools
import time
from typing import Callable


# Using @functools.lru_cache
@functools.lru_cache(maxsize=128)
def fibonacci(n: int) -> int:
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


# Using @functools.cache (Python 3.9+)
@functools.cache
def factorial(n: int) -> int:
    if n <= 1:
        return 1
    return n * factorial(n - 1)


# Using @functools.total_ordering
@functools.total_ordering
class Person:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def __eq__(self, other):
        if not isinstance(other, Person):
            return NotImplemented
        return self.age == other.age

    def __lt__(self, other):
        if not isinstance(other, Person):
            return NotImplemented
        return self.age < other.age

    def __repr__(self):
        return f"Person('{self.name}', {self.age})"


def demonstrate_partial():
    """functools.partial: fix function arguments."""
    print("=== partial ===")
    power = lambda base, exp: base ** exp
    square = functools.partial(power, exp=2)
    cube = functools.partial(power, exp=3)

    print(f"  square(5) = {square(5)}")
    print(f"  cube(5) = {cube(5)}")

    # Real-world: logging with preset level
    import logging
    log_info = functools.partial(logging.info)
    log_error = functools.partial(logging.error)
    print("  Created partial log functions")


def demonstrate_reduce():
    """functools.reduce: cumulative operations."""
    print("\n=== reduce ===")
    numbers = [1, 2, 3, 4, 5]

    total = functools.reduce(lambda a, b: a + b, numbers)
    print(f"  Sum: {total}")

    product = functools.reduce(lambda a, b: a * b, numbers)
    print(f"  Product: {product}")

    # reduce with initial value
    result = functools.reduce(lambda a, b: a + b, numbers, 100)
    print(f"  Sum with initial 100: {result}")


def demonstrate_wraps():
    """functools.wraps: preserve metadata in decorators."""
    print("\n=== wraps ===")

    def my_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            """Wrapper docstring."""
            return func(*args, **kwargs)
        return wrapper

    @my_decorator
    def example():
        """Example function docstring."""
        pass

    print(f"  Function name: {example.__name__}")
    print(f"  Docstring: {example.__doc__}")


def demonstrate_singledispatch():
    """functools.singledispatch: generic functions."""
    print("\n=== singledispatch ===")

    @functools.singledispatch
    def process(value):
        raise NotImplementedError(f"Unsupported type: {type(value)}")

    @process.register(int)
    def _(value):
        return f"Processing integer: {value * 2}"

    @process.register(str)
    def _(value):
        return f"Processing string: {value.upper()}"

    @process.register(list)
    def _(value):
        return f"Processing list: {sum(value)}"

    @process.register(dict)
    def _(value):
        return f"Processing dict: keys={list(value.keys())}"

    print(f"  process(42): {process(42)}")
    print(f"  process('hello'): {process('hello')}")
    print(f"  process([1, 2, 3]): {process([1, 2, 3])}")
    print(f"  process({'a': 1}): {process({'a': 1})}")


def demonstrate_cached_property():
    """functools.cached_property: lazy caching."""
    print("\n=== cached_property ===")

    class DataProcessor:
        def __init__(self, data: list):
            self.data = data

        @functools.cached_property
        def expensive_computation(self):
            print("  (Computing expensive value...)")
            time.sleep(0.1)
            return sum(self.data) / len(self.data)

    dp = DataProcessor([1, 2, 3, 4, 5])
    print(f"  First access: {dp.expensive_computation}")
    print(f"  Second access (cached): {dp.expensive_computation}")


def main():
    demonstrate_partial()
    demonstrate_reduce()
    demonstrate_wraps()

    # lru_cache
    print("\n=== lru_cache ===")
    start = time.time()
    result = fibonacci(35)
    elapsed1 = time.time() - start
    print(f"  fibonacci(35) = {result} (uncached: {elapsed1:.4f}s)")

    start = time.time()
    result = fibonacci(35)
    elapsed2 = time.time() - start
    print(f"  fibonacci(35) = {result} (cached: {elapsed2:.4f}s)")
    print(f"  Cache info: {fibonacci.cache_info()}")

    # total_ordering
    print("\n=== total_ordering ===")
    people = [Person("Alice", 25), Person("Bob", 30), Person("Charlie", 20)]
    sorted_people = sorted(people)
    print(f"  Sorted: {sorted_people}")
    print(f"  Alice < Bob? {Person('Alice', 25) < Person('Bob', 30)}")
    print(f"  Alice >= Bob? {Person('Alice', 25) >= Person('Bob', 30)}")

    demonstrate_singledispatch()
    demonstrate_cached_property()


if __name__ == "__main__":
    main()
