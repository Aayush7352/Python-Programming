import multiprocessing
import os
import time
import random
from typing import List


def worker(name: str, delay: float) -> str:
    """Simple worker process."""
    pid = os.getpid()
    print(f"  [{pid}] {name}: starting, delay={delay}")
    time.sleep(delay)
    print(f"  [{pid}] {name}: finished")
    return f"Result from {name}"


def cpu_intensive(n: int) -> int:
    """CPU-intensive task (no GIL)."""
    count = 0
    for i in range(n):
        count += i ** 2
    return count


def demonstrate_basic_process():
    """Basic process creation."""
    print("=== Basic Process ===")
    p = multiprocessing.Process(target=worker, args=("Process-1", 0.5))
    print(f"  Starting process: {p.name}")
    p.start()
    print(f"  Process PID: {p.pid}")
    p.join()
    print("  Process joined")


def demonstrate_processes():
    """Multiple processes."""
    print("\n=== Multiple Processes ===")
    processes = []
    for i in range(4):
        p = multiprocessing.Process(
            target=worker,
            args=(f"Worker-{i}", random.uniform(0.5, 1.5))
        )
        processes.append(p)
        p.start()

    for p in processes:
        p.join()
    print("  All workers done")


def demonstrate_pool():
    """Process pool."""
    from concurrent.futures import ProcessPoolExecutor
    print("\n=== Process Pool ===")
    numbers = [10_000_000, 20_000_000, 30_000_000]

    start = time.time()
    with ProcessPoolExecutor(max_workers=3) as executor:
        results = list(executor.map(cpu_intensive, numbers))
    elapsed = time.time() - start

    for n, result in zip(numbers, results):
        print(f"  cpu_intensive({n}) = {result}")
    print(f"  Total time: {elapsed:.4f}s")


def demonstrate_shared_memory():
    """Sharing data between processes."""
    print("\n=== Shared Memory ===")

    def increment(val, lock):
        for _ in range(100):
            with lock:
                val.value += 1

    value = multiprocessing.Value("i", 0)
    lock = multiprocessing.Lock()

    processes = []
    for _ in range(4):
        p = multiprocessing.Process(target=increment, args=(value, lock))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    print(f"  Final value: {value.value} (expected 400)")


def demonstrate_queue():
    """Inter-process communication with Queue."""
    print("\n=== Process Queue ===")

    def producer(queue, items):
        for item in items:
            queue.put(item)
            time.sleep(0.1)
        queue.put(None)  # sentinel

    def consumer(queue):
        while True:
            item = queue.get()
            if item is None:
                break
            print(f"  Consumer got: {item}")

    queue = multiprocessing.Queue()
    items = ["apple", "banana", "cherry", "date", "elderberry"]

    p1 = multiprocessing.Process(target=producer, args=(queue, items))
    p2 = multiprocessing.Process(target=consumer, args=(queue,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()


def main():
    print(f"Main PID: {os.getpid()}")
    print(f"CPU count: {multiprocessing.cpu_count()}")

    demonstrate_basic_process()
    demonstrate_processes()
    demonstrate_pool()
    demonstrate_shared_memory()
    demonstrate_queue()

    print("\n=== Process Info ===")
    current = multiprocessing.current_process()
    print(f"  Current process: {current.name}")
    print(f"  PID: {current.pid}")


if __name__ == "__main__":
    # Required for multiprocessing on some platforms
    multiprocessing.set_start_method("spawn", force=True)
    main()
