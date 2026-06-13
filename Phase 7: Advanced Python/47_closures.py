def make_counter():
    """Creates a counter using closure."""
    count = 0

    def counter():
        nonlocal count  # allows modifying the enclosing variable
        count += 1
        return count

    return counter


def make_multiplier(factor: float):
    """Creates a multiplier function via closure."""
    def multiplier(x: float) -> float:
        return x * factor
    return multiplier


def make_power_function(exponent: int):
    """Creates a power function via closure."""
    def power(base: int) -> int:
        return base ** exponent
    return power


def make_logger(prefix: str):
    """Creates a logger with a fixed prefix."""
    def log(message: str) -> str:
        return f"[{prefix}] {message}"
    return log


def make_averager():
    """Closure that maintains running average."""
    values = []

    def averager(value: float) -> float:
        values.append(value)
        return sum(values) / len(values)

    return averager


def make_limited_call(max_calls: int):
    """Closure that limits how many times a function can be called."""
    calls = 0

    def call(func, *args, **kwargs):
        nonlocal calls
        if calls >= max_calls:
            raise RuntimeError(f"Max calls ({max_calls}) exceeded")
        calls += 1
        return func(*args, **kwargs)

    return call


def inspect_closure(func):
    """Inspect closure variables."""
    print(f"  Function: {func.__name__}")
    if hasattr(func, "__closure__") and func.__closure__:
        for i, cell in enumerate(func.__closure__):
            print(f"    Cell {i}: {cell.cell_contents}")
    else:
        print("    No closure cells")


def main():
    print("=== Counter Closure ===")
    counter1 = make_counter()
    counter2 = make_counter()
    print(f"  counter1: {counter1()}, {counter1()}, {counter1()}")
    print(f"  counter2: {counter2()}, {counter2()}")

    print("\n=== Multiplier Closure ===")
    double = make_multiplier(2)
    triple = make_multiplier(3)
    print(f"  double(5) = {double(5)}")
    print(f"  triple(5) = {triple(5)}")

    print("\n=== Power Function Closure ===")
    square = make_power_function(2)
    cube = make_power_function(3)
    print(f"  square(4) = {square(4)}")
    print(f"  cube(4) = {cube(4)}")

    print("\n=== Logger Closure ===")
    info_logger = make_logger("INFO")
    error_logger = make_logger("ERROR")
    print(f"  {info_logger('Server started')}")
    print(f"  {error_logger('Connection failed')}")

    print("\n=== Running Average Closure ===")
    avg = make_averager()
    print(f"  avg(10) = {avg(10)}")
    print(f"  avg(20) = {avg(20)}")
    print(f"  avg(30) = {avg(30)}")

    print("\n=== Limited Call Closure ===")
    limited = make_limited_call(3)
    print(f"  limited(len, [1,2,3]) = {limited(len, [1, 2, 3])}")
    print(f"  limited(sum, [1,2,3]) = {limited(sum, [1, 2, 3])}")
    print(f"  limited(max, [1,2,3]) = {limited(max, [1, 2, 3])}")
    try:
        limited(min, [1, 2, 3])
    except RuntimeError as e:
        print(f"  Error: {e}")

    print("\n=== Closure Inspection ===")
    inspect_closure(double)
    inspect_closure(make_counter())


if __name__ == "__main__":
    main()
