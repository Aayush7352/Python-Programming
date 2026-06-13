import asyncio
import random
import threading
from queue import Queue, PriorityQueue, LifoQueue
from typing import List


def demonstrate_queue_basics() -> None:
    """Basic queue operations."""
    print("=== Queue Basics ===")
    q = Queue(maxsize=5)

    # Put items
    for i in range(5):
        q.put(i)
        print(f"  Put: {i}, Size: {q.qsize()}")

    # Get items
    while not q.empty():
        item = q.get()
        print(f"  Got: {item}, Size: {q.qsize()}")
        q.task_done()

    q.join()
    print("  All tasks done")


def demonstrate_lifo_queue() -> None:
    """LIFO queue (stack)."""
    print("\n=== LIFO Queue (Stack) ===")
    q = LifoQueue()

    for i in range(5):
        q.put(i)
        print(f"  Push: {i}")

    while not q.empty():
        print(f"  Pop: {q.get()}")


def demonstrate_priority_queue() -> None:
    """Priority queue."""
    print("\n=== Priority Queue ===")
    q = PriorityQueue()

    tasks = [
        (3, "Low priority task"),
        (1, "High priority task"),
        (2, "Medium priority task"),
        (1, "Another high priority"),
        (4, "Very low priority"),
    ]

    for priority, task in tasks:
        q.put((priority, task))
        print(f"  Added: (priority={priority}) {task}")

    print("\n  Processing (by priority):")
    while not q.empty():
        priority, task = q.get()
        print(f"  Processing: {task}")
        q.task_done()
    q.join()


def demonstrate_threaded_queue() -> None:
    """Queue with threading."""
    print("\n=== Threaded Queue ===")

    def worker(q: Queue):
        while True:
            item = q.get()
            if item is None:
                q.task_done()
                break
            print(f"  [{threading.current_thread().name}] Processing: {item}")
            import time
            time.sleep(random.uniform(0.1, 0.3))
            q.task_done()

    q = Queue()
    num_workers = 3

    threads = []
    for i in range(num_workers):
        t = threading.Thread(target=worker, args=(q,), name=f"Worker-{i}")
        t.start()
        threads.append(t)

    for i in range(10):
        q.put(f"Job-{i}")

    q.join()

    for _ in range(num_workers):
        q.put(None)

    for t in threads:
        t.join()

    print("  All jobs processed")


async def demonstrate_async_queue() -> None:
    """Asyncio queue."""
    print("\n=== Async Queue ===")

    async def producer(queue: asyncio.Queue, n: int):
        for i in range(n):
            await asyncio.sleep(random.uniform(0.05, 0.15))
            item = f"Item-{i}"
            await queue.put(item)
            print(f"  [Producer] Put: {item}")
        await queue.put(None)  # sentinel

    async def consumer(name: str, queue: asyncio.Queue):
        while True:
            item = await queue.get()
            if item is None:
                await queue.put(None)  # pass sentinel to others
                queue.task_done()
                break
            await asyncio.sleep(random.uniform(0.1, 0.2))
            print(f"  [{name}] Got: {item}")
            queue.task_done()

    queue = asyncio.Queue(maxsize=5)

    consumers = [asyncio.create_task(consumer(f"Consumer-{i}", queue)) for i in range(2)]
    prod = asyncio.create_task(producer(queue, 8))

    await asyncio.gather(prod, *consumers)
    await queue.join()
    print("  Async queue processing complete")


def main():
    demonstrate_queue_basics()
    demonstrate_lifo_queue()
    demonstrate_priority_queue()
    demonstrate_threaded_queue()

    # Async queue
    asyncio.run(demonstrate_async_queue())

    print("\n=== Queue Attributes ===")
    q = Queue()
    print(f"  Empty: {q.empty()}")
    q.put("test")
    print(f"  Not empty: {q.empty()}")
    print(f"  Size: {q.qsize()}")
    print(f"  Maxsize: {q.maxsize}")


if __name__ == "__main__":
    main()
