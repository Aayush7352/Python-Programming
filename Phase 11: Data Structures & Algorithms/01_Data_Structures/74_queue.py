from collections import deque
from typing import Any, Optional


class Queue:
    """Queue implementation using collections.deque."""

    def __init__(self):
        self._items = deque()

    def enqueue(self, item):
        self._items.append(item)

    def dequeue(self):
        if self.is_empty:
            raise IndexError("Dequeue from empty queue")
        return self._items.popleft()

    def peek(self):
        if self.is_empty:
            raise IndexError("Peek from empty queue")
        return self._items[0]

    @property
    def is_empty(self):
        return len(self._items) == 0

    @property
    def size(self):
        return len(self._items)

    def __repr__(self):
        return f"Queue({list(self._items)})"


class CircularQueue:
    """Circular queue using array."""

    def __init__(self, capacity: int = 10):
        self.capacity = capacity
        self._items = [None] * capacity
        self._front = 0
        self._rear = 0
        self._size = 0

    def enqueue(self, item):
        if self._size == self.capacity:
            raise OverflowError("Queue is full")
        self._items[self._rear] = item
        self._rear = (self._rear + 1) % self.capacity
        self._size += 1

    def dequeue(self):
        if self._size == 0:
            raise IndexError("Dequeue from empty queue")
        item = self._items[self._front]
        self._front = (self._front + 1) % self.capacity
        self._size -= 1
        return item

    @property
    def is_empty(self):
        return self._size == 0

    @property
    def is_full(self):
        return self._size == self.capacity


class PriorityQueue:
    """Simple priority queue using list (min-heap based)."""

    def __init__(self):
        self._items = []

    def enqueue(self, item, priority: int):
        self._items.append((priority, item))
        self._items.sort(key=lambda x: x[0])

    def dequeue(self):
        if self.is_empty:
            raise IndexError("Dequeue from empty priority queue")
        return self._items.pop(0)[1]

    @property
    def is_empty(self):
        return len(self._items) == 0

    @property
    def size(self):
        return len(self._items)


def hot_potato(names: list, k: int) -> str:
    """Hot potato game using queue."""
    q = Queue()
    for name in names:
        q.enqueue(name)

    while q.size > 1:
        for _ in range(k - 1):
            q.enqueue(q.dequeue())
        q.dequeue()
    return q.dequeue()


def print_binary_numbers(n: int) -> list:
    """Generate first n binary numbers using queue."""
    q = Queue()
    q.enqueue("1")
    result = []

    for _ in range(n):
        current = q.dequeue()
        result.append(current)
        q.enqueue(current + "0")
        q.enqueue(current + "1")

    return result


def main():
    print("=== Queue Basics ===")
    q = Queue()
    for v in [1, 2, 3, 4, 5]:
        q.enqueue(v)
    print(f"  Queue: {q}")
    print(f"  Dequeue: {q.dequeue()}")
    print(f"  Peek: {q.peek()}")
    print(f"  Size: {q.size}")
    print(f"  Empty: {q.is_empty}")

    print("\n=== Circular Queue ===")
    cq = CircularQueue(5)
    for v in range(5):
        cq.enqueue(v)
    print(f"  Full: {cq.is_full}")
    print(f"  Dequeue: {cq.dequeue()}")
    cq.enqueue(99)
    print(f"  After wrap-around enqueue: {cq.dequeue()}")

    print("\n=== Priority Queue ===")
    pq = PriorityQueue()
    pq.enqueue("Low", 3)
    pq.enqueue("High", 1)
    pq.enqueue("Medium", 2)
    while not pq.is_empty:
        print(f"  Dequeue: {pq.dequeue()}")

    print("\n=== Hot Potato ===")
    names = ["Alice", "Bob", "Charlie", "Diana", "Eve"]
    winner = hot_potato(names, 3)
    print(f"  Winner: {winner}")

    print("\n=== Binary Numbers ===")
    print(f"  First 10 binary numbers: {print_binary_numbers(10)}")

    print("\n=== Queue Applications ===")
    print("  - Task scheduling")
    print("  - BFS graph traversal")
    print("  - Print spooling")
    print("  - Message passing")
    print("  - Buffering")


if __name__ == "__main__":
    main()
