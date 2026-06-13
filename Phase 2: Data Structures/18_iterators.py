class CountUpTo:
    """Custom iterator that counts up to a limit."""
    def __init__(self, limit: int):
        self.limit = limit
        self.current = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.current >= self.limit:
            raise StopIteration
        self.current += 1
        return self.current


class FibonacciIterator:
    """Custom iterator for Fibonacci sequence."""
    def __init__(self, n: int):
        self.n = n
        self.count = 0
        self.a, self.b = 0, 1

    def __iter__(self):
        return self

    def __next__(self):
        if self.count >= self.n:
            raise StopIteration
        self.count += 1
        value = self.a
        self.a, self.b = self.b, self.a + self.b
        return value


class ReversibleList:
    """Iterator that can go forward and backward."""
    def __init__(self, data: list):
        self.data = data

    def __iter__(self):
        return iter(self.data)

    def __reversed__(self):
        return reversed(self.data)


def main():
    # Using custom iterators
    print("=== Custom Iterators ===")
    counter = CountUpTo(5)
    for num in counter:
        print(f"Count: {num}")

    print("\nFibonacci (first 10):")
    for num in FibonacciIterator(10):
        print(f"  {num}", end="")
    print()

    # Built-in iterators
    print("\n=== Built-in Iterators ===")
    lst = [1, 2, 3, 4, 5]
    it = iter(lst)
    print(f"next(it): {next(it)}")
    print(f"next(it): {next(it)}")
    print(f"next(it): {next(it)}")

    # Iterator tools
    print("\n=== Iterator Tools ===")
    from itertools import islice, cycle, repeat, count

    print("First 5 of infinite count:")
    for i in islice(count(0), 5):
        print(f"  {i}", end="")
    print()

    print("Cycle through [1,2,3] (first 7):")
    cycled = cycle([1, 2, 3])
    for i in islice(cycled, 7):
        print(f"  {i}", end="")
    print()

    # For loop mechanics
    print("\n=== For Loop Mechanics ===")
    custom_list = [10, 20, 30]
    iterator = iter(custom_list)
    while True:
        try:
            item = next(iterator)
            print(f"Manually iterated: {item}")
        except StopIteration:
            break

    # Reversible
    rl = ReversibleList([1, 2, 3, 4, 5])
    print(f"\nForward: {list(rl)}")
    print(f"Reverse: {list(reversed(rl))}")


if __name__ == "__main__":
    main()
