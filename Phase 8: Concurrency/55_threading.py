import threading
import time
import random
from typing import List


counter = 0
counter_lock = threading.Lock()


def increment_counter(thread_id: int, iterations: int) -> None:
    """Increment a shared counter with lock protection."""
    global counter
    for i in range(iterations):
        with counter_lock:
            current = counter
            time.sleep(0.0001)  # Force context switch
            counter = current + 1
    print(f"  Thread {thread_id} done")


def worker(name: str, delay: float) -> None:
    """Simple worker thread."""
    for i in range(3):
        time.sleep(delay)
        print(f"  {name}: working... step {i + 1}")
    print(f"  {name}: finished")


def daemon_worker() -> None:
    """Daemon thread that runs in background."""
    while True:
        time.sleep(0.5)
        print("  [Daemon] heartbeating...")
        if threading.Event().wait(0):  # never true, just to show intent
            break


def thread_with_args() -> None:
    """Create threads with different arguments."""
    print("=== Thread with Arguments ===")
    threads = []
    for i in range(3):
        t = threading.Thread(target=worker, args=(f"Worker-{i}", random.uniform(0.1, 0.3)))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
    print("  All workers done")


def thread_synchronization() -> None:
    """Demonstrate thread synchronization with Lock."""
    print("\n=== Thread Synchronization ===")
    global counter
    counter = 0

    threads = []
    for i in range(5):
        t = threading.Thread(target=increment_counter, args=(i, 100))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print(f"  Final counter value: {counter} (expected 500)")


def thread_event() -> None:
    """Using events for thread communication."""
    print("\n=== Thread Events ===")
    event = threading.Event()

    def waiter(event):
        print("  Waiter: waiting for event...")
        event.wait()
        print("  Waiter: event received, proceeding!")

    def setter(event):
        time.sleep(1)
        print("  Setter: setting event")
        event.set()

    w = threading.Thread(target=waiter, args=(event,))
    s = threading.Thread(target=setter, args=(event,))
    w.start()
    s.start()
    w.join()
    s.join()


def thread_local_data() -> None:
    """Thread-local storage."""
    print("\n=== Thread-Local Data ===")
    local_data = threading.local()

    def process_data(value):
        local_data.value = value
        time.sleep(random.uniform(0.1, 0.3))
        print(f"  Thread processing: {local_data.value}")

    threads = []
    for i in range(3):
        t = threading.Thread(target=process_data, args=(i * 10,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()


def thread_pool() -> None:
    """Using concurrent.futures for thread pooling."""
    from concurrent.futures import ThreadPoolExecutor

    print("\n=== Thread Pool ===")

    def task(n: int) -> str:
        time.sleep(random.uniform(0.1, 0.3))
        return f"Task {n} completed"

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(task, i) for i in range(8)]
        for future in futures:
            print(f"  {future.result()}")

    print("  All pool tasks done")


def main():
    print("=== Basic Threading ===")
    t = threading.Thread(target=worker, args=("Thread-1", 0.2))
    t.start()
    print("  Main thread continuing...")
    t.join()
    print("  Thread joined")

    thread_with_args()
    thread_synchronization()
    thread_event()
    thread_local_data()
    thread_pool()

    print(f"\n=== Thread Info ===")
    print(f"  Active threads: {threading.active_count()}")
    print(f"  Current thread: {threading.current_thread().name}")


if __name__ == "__main__":
    main()
