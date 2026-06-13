def count_up_to(n: int):
    """Generator that counts from 1 to n."""
    i = 1
    while i <= n:
        yield i
        i += 1


def fibonacci_generator():
    """Infinite Fibonacci sequence generator."""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


def read_large_file(file_path: str):
    """Generator to read large files line by line (memory efficient)."""
    with open(file_path, "r") as f:
        for line in f:
            yield line.strip()


def pipeline_demo():
    """Generator pipeline example."""
    def numbers():
        for i in range(10):
            yield i

    def even_only(source):
        for num in source:
            if num % 2 == 0:
                yield num

    def multiply(source, factor):
        for num in source:
            yield num * factor

    pipeline = multiply(even_only(numbers()), 10)
    return list(pipeline)


def main():
    # Basic generator
    print("=== Basic Generator ===")
    gen = count_up_to(5)
    print(f"Generator type: {type(gen)}")
    for num in gen:
        print(f"  {num}")

    # Generator as iterator
    print("\n=== Generator is an Iterator ===")
    gen = count_up_to(3)
    print(f"next: {next(gen)}")
    print(f"next: {next(gen)}")
    print(f"next: {next(gen)}")

    # Fibonacci generator (lazy evaluation)
    print("\n=== Fibonacci Generator ===")
    from itertools import islice
    fib = fibonacci_generator()
    first_10 = list(islice(fib, 10))
    print(f"First 10 Fibonacci: {first_10}")

    # Yield from
    print("\n=== Yield From ===")
    def chain(*iterables):
        for it in iterables:
            yield from it

    chained = chain([1, 2, 3], "abc", (10, 20))
    print(f"Chained: {list(chained)}")

    # Generator pipeline
    print("\n=== Generator Pipeline ===")
    result = pipeline_demo()
    print(f"Pipeline result: {result}")

    # Generator expressions
    print("\n=== Generator Expressions ===")
    gen_exp = (x ** 2 for x in range(5))
    print(f"Generator expression: {list(gen_exp)}")

    # Send to generator
    print("\n=== Generator send() ===")
    def echo_generator():
        while True:
            received = yield
            print(f"Received: {received}")

    gen = echo_generator()
    next(gen)  # prime the generator
    gen.send("Hello")
    gen.send("World")

    # Generator with return value
    print("\n=== Generator return value ===")
    def gen_with_return():
        yield 1
        yield 2
        return "done"

    g = gen_with_return()
    print(f"Yielded: {next(g)}")
    print(f"Yielded: {next(g)}")
    try:
        next(g)
    except StopIteration as e:
        print(f"Return value: {e.value}")


if __name__ == "__main__":
    main()
