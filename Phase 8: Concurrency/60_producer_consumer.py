import asyncio
import random
import time
import threading
from queue import Queue
from typing import List


class ProducerConsumer:
    """Producer-Consumer pattern with threading."""

    def __init__(self, num_producers: int = 2, num_consumers: int = 3):
        self.queue = Queue(maxsize=10)
        self.num_producers = num_producers
        self.num_consumers = num_consumers
        self.stop_event = threading.Event()

    def produce(self, producer_id: int) -> None:
        """Producer function."""
        while not self.stop_event.is_set():
            item = f"P{producer_id}-Item-{random.randint(1, 100)}"
            self.queue.put(item)
            print(f"  [Producer {producer_id}] Produced: {item}")
            time.sleep(random.uniform(0.1, 0.3))
        print(f"  [Producer {producer_id}] Stopped")

    def consume(self, consumer_id: int) -> None:
        """Consumer function."""
        while True:
            try:
                item = self.queue.get(timeout=1)
                # Process item
                time.sleep(random.uniform(0.2, 0.4))
                print(f"  [Consumer {consumer_id}] Consumed: {item}")
                self.queue.task_done()
            except Exception:
                if self.stop_event.is_set() and self.queue.empty():
                    break
        print(f"  [Consumer {consumer_id}] Stopped")

    def run(self, duration: float = 3.0) -> None:
        """Run producers and consumers for a duration."""
        threads = []

        for i in range(self.num_producers):
            t = threading.Thread(target=self.produce, args=(i,))
            threads.append(t)
            t.start()

        for i in range(self.num_consumers):
            t = threading.Thread(target=self.consume, args=(i,))
            threads.append(t)
            t.start()

        time.sleep(duration)
        self.stop_event.set()

        for t in threads:
            t.join(timeout=2)

        print(f"  Queue remaining: {self.queue.qsize()}")


class AsyncProducerConsumer:
    """Producer-Consumer with asyncio."""

    def __init__(self, num_producers: int = 2, num_consumers: int = 3):
        self.queue = asyncio.Queue(maxsize=10)
        self.num_producers = num_producers
        self.num_consumers = num_consumers

    async def produce(self, producer_id: int) -> None:
        """Async producer."""
        for i in range(5):
            item = f"P{producer_id}-Item-{i}"
            await self.queue.put(item)
            print(f"  [Async Producer {producer_id}] Produced: {item}")
            await asyncio.sleep(random.uniform(0.1, 0.3))

        # Sentinel for each consumer
        for _ in range(self.num_consumers):
            await self.queue.put(None)

    async def consume(self, consumer_id: int) -> None:
        """Async consumer."""
        while True:
            item = await self.queue.get()
            if item is None:
                self.queue.task_done()
                break
            await asyncio.sleep(random.uniform(0.2, 0.4))
            print(f"  [Async Consumer {consumer_id}] Consumed: {item}")
            self.queue.task_done()

    async def run(self) -> None:
        """Run async producers and consumers."""
        producers = [
            asyncio.create_task(self.produce(i))
            for i in range(self.num_producers)
        ]
        consumers = [
            asyncio.create_task(self.consume(i))
            for i in range(self.num_consumers)
        ]

        await asyncio.gather(*producers)
        await self.queue.join()

        for c in consumers:
            c.cancel()

        print("  Async producer-consumer complete")


class BoundedBuffer:
    """Bounded buffer with threading conditions."""

    def __init__(self, size: int = 5):
        self.buffer: List[int] = []
        self.size = size
        self.lock = threading.Lock()
        self.not_full = threading.Condition(self.lock)
        self.not_empty = threading.Condition(self.lock)

    def put(self, item: int) -> None:
        with self.not_full:
            while len(self.buffer) >= self.size:
                self.not_full.wait()
            self.buffer.append(item)
            self.not_empty.notify()

    def get(self) -> int:
        with self.not_empty:
            while len(self.buffer) == 0:
                self.not_empty.wait()
            item = self.buffer.pop(0)
            self.not_full.notify()
            return item


def demonstrate_bounded_buffer() -> None:
    """Demonstrate bounded buffer with conditions."""
    print("\n=== Bounded Buffer ===")
    buffer = BoundedBuffer(3)
    results = []

    def producer():
        for i in range(6):
            buffer.put(i)
            print(f"  [BB Producer] Put: {i}")
            time.sleep(random.uniform(0.1, 0.3))

    def consumer():
        for _ in range(6):
            item = buffer.get()
            print(f"  [BB Consumer] Got: {item}")
            results.append(item)
            time.sleep(random.uniform(0.2, 0.4))

    p = threading.Thread(target=producer)
    c = threading.Thread(target=consumer)
    p.start()
    c.start()
    p.join()
    c.join()
    print(f"  Consumed items: {results}")


def main():
    print("=== Threading Producer-Consumer ===")
    pc = ProducerConsumer(num_producers=2, num_consumers=3)
    pc.run(duration=2.0)

    print("\n=== Async Producer-Consumer ===")
    asyncio.run(AsyncProducerConsumer(2, 3).run())

    demonstrate_bounded_buffer()

    print("\n=== Summary ===")
    print("  Producer-Consumer pattern decouples:")
    print("  - Producers: create data/tasks")
    print("  - Queue: buffers between producers and consumers")
    print("  - Consumers: process data/tasks")
    print("  Benefits: load leveling, parallel processing")


if __name__ == "__main__":
    main()
