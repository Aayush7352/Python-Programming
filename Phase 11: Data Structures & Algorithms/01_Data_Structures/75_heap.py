import heapq
import random


class MinHeap:
    """Min-heap implementation using heapq."""

    def __init__(self):
        self._items = []

    def push(self, item):
        heapq.heappush(self._items, item)

    def pop(self):
        if self.is_empty:
            raise IndexError("Pop from empty heap")
        return heapq.heappop(self._items)

    def peek(self):
        if self.is_empty:
            raise IndexError("Peek from empty heap")
        return self._items[0]

    @property
    def is_empty(self):
        return len(self._items) == 0

    @property
    def size(self):
        return len(self._items)

    def __repr__(self):
        return f"MinHeap({self._items})"


class MaxHeap:
    """Max-heap using heapq with negated values."""

    def __init__(self):
        self._items = []

    def push(self, item):
        heapq.heappush(self._items, -item)

    def pop(self):
        if self.is_empty:
            raise IndexError("Pop from empty heap")
        return -heapq.heappop(self._items)

    def peek(self):
        if self.is_empty:
            raise IndexError("Peek from empty heap")
        return -self._items[0]

    @property
    def is_empty(self):
        return len(self._items) == 0


class MedianFinder:
    """Find median from a stream of numbers using two heaps."""

    def __init__(self):
        self._small = []  # max-heap (negated)
        self._large = []  # min-heap

    def add_num(self, num: int):
        if not self._small or num <= -self._small[0]:
            heapq.heappush(self._small, -num)
        else:
            heapq.heappush(self._large, num)

        # Balance heaps
        if len(self._small) > len(self._large) + 1:
            heapq.heappush(self._large, -heapq.heappop(self._small))
        elif len(self._large) > len(self._small):
            heapq.heappush(self._small, -heapq.heappop(self._large))

    def find_median(self) -> float:
        if len(self._small) == len(self._large):
            return (-self._small[0] + self._large[0]) / 2
        return float(-self._small[0])


def heap_sort(arr: list) -> list:
    """Sort using heap (heapify + repeated pop)."""
    heapq.heapify(arr)
    return [heapq.heappop(arr) for _ in range(len(arr))]


def k_smallest(arr: list, k: int) -> list:
    """Find k smallest elements."""
    return heapq.nsmallest(k, arr)


def k_largest(arr: list, k: int) -> list:
    """Find k largest elements."""
    return heapq.nlargest(k, arr)


def merge_sorted_arrays(arrays: list[list]) -> list:
    """Merge multiple sorted arrays using heap."""
    result = []
    heap = []

    for arr_idx, arr in enumerate(arrays):
        if arr:
            heapq.heappush(heap, (arr[0], arr_idx, 0))

    while heap:
        value, arr_idx, elem_idx = heapq.heappop(heap)
        result.append(value)
        if elem_idx + 1 < len(arrays[arr_idx]):
            next_val = arrays[arr_idx][elem_idx + 1]
            heapq.heappush(heap, (next_val, arr_idx, elem_idx + 1))

    return result


def main():
    print("=== Min Heap ===")
    min_heap = MinHeap()
    values = [5, 3, 8, 1, 9, 2, 7, 4, 6]
    for v in values:
        min_heap.push(v)
    print(f"  Heap: {min_heap}")
    sorted_vals = []
    while not min_heap.is_empty:
        sorted_vals.append(min_heap.pop())
    print(f"  Sorted: {sorted_vals}")

    print("\n=== Max Heap ===")
    max_heap = MaxHeap()
    for v in values:
        max_heap.push(v)
    max_vals = []
    while not max_heap.is_empty:
        max_vals.append(max_heap.pop())
    print(f"  Sorted descending: {max_vals}")

    print("\n=== Heap Sort ===")
    arr = [random.randint(1, 100) for _ in range(10)]
    print(f"  Original: {arr}")
    print(f"  Sorted: {heap_sort(arr.copy())}")

    print("\n=== k Smallest / Largest ===")
    arr = [random.randint(1, 100) for _ in range(20)]
    print(f"  Array: {arr}")
    print(f"  3 smallest: {k_smallest(arr, 3)}")
    print(f"  5 largest: {k_largest(arr, 5)}")

    print("\n=== Median Finder ===")
    mf = MedianFinder()
    numbers = [5, 3, 8, 1, 9, 2, 7, 4, 6]
    for n in numbers:
        mf.add_num(n)
        print(f"  Added {n}, median: {mf.find_median()}")

    print("\n=== Merge Sorted Arrays ===")
    arrays = [
        [1, 4, 7, 10],
        [2, 5, 8, 11],
        [3, 6, 9, 12],
    ]
    print(f"  Merged: {merge_sorted_arrays(arrays)}")

    print("\n=== Heap Operations ===")
    print(f"  heapq.heapify converts list to heap in O(n)")
    print(f"  heapq.heappush/pop in O(log n)")
    print(f"  heapq.nsmallest/nlargest in O(n log k)")


if __name__ == "__main__":
    main()
