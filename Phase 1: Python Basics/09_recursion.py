import sys


def factorial(n: int) -> int:
    """Calculate factorial using recursion."""
    if n <= 1:
        return 1
    return n * factorial(n - 1)


def fibonacci(n: int) -> int:
    """Fibonacci number using recursion (inefficient for large n)."""
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


def fibonacci_memo(n: int, memo: dict = None) -> int:
    """Fibonacci with memoization for efficiency."""
    if memo is None:
        memo = {}
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    memo[n] = fibonacci_memo(n - 1, memo) + fibonacci_memo(n - 2, memo)
    return memo[n]


def binary_search(arr: list, target: int, low: int, high: int) -> int:
    """Binary search using recursion."""
    if low > high:
        return -1
    mid = (low + high) // 2
    if arr[mid] == target:
        return mid
    elif arr[mid] > target:
        return binary_search(arr, target, low, mid - 1)
    else:
        return binary_search(arr, target, mid + 1, high)


def tower_of_hanoi(n: int, source: str, aux: str, dest: str) -> None:
    """Solve Tower of Hanoi recursively."""
    if n == 1:
        print(f"Move disk 1 from {source} to {dest}")
        return
    tower_of_hanoi(n - 1, source, dest, aux)
    print(f"Move disk {n} from {source} to {dest}")
    tower_of_hanoi(n - 1, aux, source, dest)


def main():
    print(f"Factorial of 5: {factorial(5)}")
    print(f"Factorial of 10: {factorial(10)}")

    print(f"\nFibonacci (memoized) of 10: {fibonacci_memo(10)}")
    print(f"Fibonacci (memoized) of 35: {fibonacci_memo(35)}")

    arr = [1, 3, 5, 7, 9, 11, 13, 15]
    target = 11
    result = binary_search(arr, target, 0, len(arr) - 1)
    print(f"\nBinary search for {target} in {arr}: index {result}")

    print("\nTower of Hanoi (3 disks):")
    tower_of_hanoi(3, "A", "B", "C")

    # Recursion limit
    print(f"\nRecursion limit: {sys.getrecursionlimit()}")


if __name__ == "__main__":
    main()
