import time
import functools


def timer(func):
    """Decorator that measures function execution time."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"  {func.__name__} took {elapsed:.4f}s")
        return result
    return wrapper


def debug(func):
    """Decorator that prints function call details."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        print(f"  Calling {func.__name__}({signature})")
        result = func(*args, **kwargs)
        print(f"  {func.__name__} returned {result!r}")
        return result
    return wrapper


def repeat(n: int):
    """Decorator factory: repeats function n times."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            results = []
            for i in range(n):
                result = func(*args, **kwargs)
                results.append(result)
            return results
        return wrapper
    return decorator


def validate_types(**types):
    """Decorator that validates argument types."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for arg_name, expected_type in types.items():
                if arg_name in kwargs:
                    value = kwargs[arg_name]
                    if not isinstance(value, expected_type):
                        raise TypeError(
                            f"Argument '{arg_name}' must be {expected_type.__name__}, "
                            f"got {type(value).__name__}"
                        )
            return func(*args, **kwargs)
        return wrapper
    return decorator


def cache(func):
    """Simple memoization decorator."""
    memo = {}
    @functools.wraps(func)
    def wrapper(*args):
        if args not in memo:
            memo[args] = func(*args)
        return memo[args]
    return wrapper


class CountCalls:
    """Class-based decorator that counts function calls."""

    def __init__(self, func):
        functools.update_wrapper(self, func)
        self.func = func
        self.count = 0

    def __call__(self, *args, **kwargs):
        self.count += 1
        print(f"  {self.func.__name__} called {self.count} time(s)")
        return self.func(*args, **kwargs)


@timer
@debug
def slow_function(n: int) -> int:
    """A slow function for demonstration."""
    time.sleep(0.1)
    return sum(range(n))


@repeat(3)
def greet(name: str) -> str:
    return f"Hello, {name}!"


@validate_types(a=int, b=int)
def add(a, b):
    return a + b


@cache
def fibonacci(n: int) -> int:
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


@CountCalls
def say_hello(name: str) -> str:
    return f"Hi, {name}!"


def main():
    print("=== Timer + Debug Decorators ===")
    result = slow_function(1000)
    print(f"  Result: {result}")

    print("\n=== Repeat Decorator ===")
    results = greet("Alice")
    print(f"  Results: {results}")

    print("\n=== Type Validation Decorator ===")
    print(f"  add(3, 4) = {add(3, 4)}")
    try:
        add("3", "4")
    except TypeError as e:
        print(f"  Error: {e}")

    print("\n=== Cache/Memoization Decorator ===")
    start = time.time()
    result = fibonacci(35)
    elapsed1 = time.time() - start
    print(f"  fibonacci(35) = {result} (first call: {elapsed1:.4f}s)")

    start = time.time()
    result = fibonacci(35)
    elapsed2 = time.time() - start
    print(f"  fibonacci(35) = {result} (cached call: {elapsed2:.4f}s)")

    print("\n=== Class-based Decorator ===")
    print(f"  {say_hello('Alice')}")
    print(f"  {say_hello('Bob')}")
    print(f"  {say_hello('Charlie')}")
    print(f"  Total calls: {say_hello.count}")

    print("\n=== Decorator Info Preservation ===")
    print(f"  Name: {slow_function.__name__}")
    print(f"  Doc: {slow_function.__doc__}")


if __name__ == "__main__":
    main()
