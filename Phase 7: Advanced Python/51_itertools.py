import itertools
import operator


def demonstrate_count():
    """itertools.count: infinite counter."""
    print("=== count ===")
    counter = itertools.count(start=0, step=2)
    first_five = list(itertools.islice(counter, 5))
    print(f"  First 5 even numbers: {first_five}")


def demonstrate_cycle():
    """itertools.cycle: infinite cycle."""
    print("\n=== cycle ===")
    colors = ["red", "green", "blue"]
    cycled = itertools.cycle(colors)
    first_eight = list(itertools.islice(cycled, 8))
    print(f"  First 8 from cycle: {first_eight}")


def demonstrate_repeat():
    """itertools.repeat: repeat a value."""
    print("\n=== repeat ===")
    repeated = list(itertools.repeat("Python", 4))
    print(f"  Repeated 'Python' 4 times: {repeated}")


def demonstrate_accumulate():
    """itertools.accumulate: running accumulation."""
    print("\n=== accumulate ===")
    numbers = [1, 2, 3, 4, 5]
    running_sum = list(itertools.accumulate(numbers))
    print(f"  Running sum: {running_sum}")

    running_product = list(itertools.accumulate(numbers, operator.mul))
    print(f"  Running product: {running_product}")


def demonstrate_chain():
    """itertools.chain: combine iterables."""
    print("\n=== chain ===")
    combined = list(itertools.chain([1, 2, 3], "abc", (10, 20)))
    print(f"  Chained: {combined}")

    # chain.from_iterable
    nested = [[1, 2], [3, 4], [5, 6]]
    flattened = list(itertools.chain.from_iterable(nested))
    print(f"  Flattened: {flattened}")


def demonstrate_combinations():
    """itertools.combinations, permutations, product."""
    print("\n=== Combinations ===")
    items = ["A", "B", "C"]
    combos = list(itertools.combinations(items, 2))
    print(f"  Combinations of 2 from {items}: {combos}")

    perms = list(itertools.permutations(items, 2))
    print(f"  Permutations of 2 from {items}: {perms}")

    prod = list(itertools.product([1, 2], ["a", "b"]))
    print(f"  Product of [1,2] x ['a','b']: {prod}")


def demonstrate_groupby():
    """itertools.groupby: group consecutive elements."""
    print("\n=== groupby ===")
    data = [("A", 1), ("A", 2), ("B", 3), ("B", 4), ("A", 5)]
    data.sort(key=lambda x: x[0])
    for key, group in itertools.groupby(data, key=lambda x: x[0]):
        print(f"  Group {key}: {list(group)}")


def demonstrate_compress():
    """itertools.compress: filter with selectors."""
    print("\n=== compress ===")
    data = ["apple", "banana", "cherry", "date"]
    selectors = [1, 0, 1, 0]
    selected = list(itertools.compress(data, selectors))
    print(f"  Compressed data: {selected}")


def demonstrate_dropwhile_takewhile():
    """itertools.dropwhile and takewhile."""
    print("\n=== dropwhile / takewhile ===")
    numbers = [1, 2, 3, 4, 5, 1, 2, 3]

    dropped = list(itertools.dropwhile(lambda x: x < 3, numbers))
    print(f"  dropwhile (x<3): {dropped}")

    taken = list(itertools.takewhile(lambda x: x < 4, numbers))
    print(f"  takewhile (x<4): {taken}")


def demonstrate_zip_longest():
    """itertools.zip_longest: zip with padding."""
    print("\n=== zip_longest ===")
    a = [1, 2, 3]
    b = ["a", "b"]
    zipped = list(itertools.zip_longest(a, b, fillvalue="*"))
    print(f"  zip_longest: {zipped}")


def demonstrate_tee():
    """itertools.tee: create multiple independent iterators."""
    print("\n=== tee ===")
    iterator = iter([1, 2, 3, 4, 5])
    it1, it2 = itertools.tee(iterator, 2)
    print(f"  First tee: {list(it1)}")
    print(f"  Second tee: {list(it2)}")


def demonstrate_paired_sliding():
    """Practical patterns."""
    print("\n=== Practical Patterns ===")

    # Sliding window
    data = [1, 2, 3, 4, 5]
    windowed = zip(data, data[1:])
    print(f"  Sliding pairs: {list(windowed)}")

    # Padded sliding window
    from itertools import pairwise
    pairs = list(pairwise(data))
    print(f"  pairwise (3.10+): {pairs}")

    # Batched processing
    def batched(iterable, n):
        it = iter(iterable)
        while True:
            batch = list(itertools.islice(it, n))
            if not batch:
                break
            yield batch

    print(f"  Batched (size 3): {list(batched(range(10), 3))}")


def main():
    demonstrate_count()
    demonstrate_cycle()
    demonstrate_repeat()
    demonstrate_accumulate()
    demonstrate_chain()
    demonstrate_combinations()
    demonstrate_groupby()
    demonstrate_compress()
    demonstrate_dropwhile_takewhile()
    demonstrate_zip_longest()
    demonstrate_tee()
    demonstrate_paired_sliding()


if __name__ == "__main__":
    main()
