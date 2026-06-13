import asyncio
from typing import AsyncGenerator, AsyncIterator


async def producer() -> AsyncGenerator[int, None]:
    """Async generator that produces values."""
    for i in range(5):
        await asyncio.sleep(0.1)
        print(f"  Produced: {i}")
        yield i


async def consumer(name: str, source: AsyncIterator[int]) -> None:
    """Consumer that processes values from an async iterator."""
    print(f"  {name} started consuming")
    async for value in source:
        print(f"  {name} received: {value}")
        await asyncio.sleep(0.15)
    print(f"  {name} finished")


async def transform(source: AsyncIterator[int], factor: int = 2) -> AsyncGenerator[int, None]:
    """Async transform: maps values through a function."""
    async for value in source:
        yield value * factor


class AsyncCounter:
    """Async iterator class."""

    def __init__(self, limit: int, delay: float = 0.1):
        self.limit = limit
        self.delay = delay
        self.current = 0

    def __aiter__(self):
        return self

    async def __anext__(self) -> int:
        if self.current >= self.limit:
            raise StopAsyncIteration
        await asyncio.sleep(self.delay)
        value = self.current
        self.current += 1
        return value


async def chain_async(*coroutines):
    """Chain multiple coroutines."""
    results = []
    for coro in coroutines:
        result = await coro
        results.append(result)
    return results


async def demonstrate_async_generator_basics() -> None:
    """Basic async generator usage."""
    print("=== Async Generator ===")
    async for value in producer():
        print(f"  Main received: {value}")


async def demonstrate_async_pipeline() -> None:
    """Pipeline with async generators."""
    print("\n=== Async Pipeline ===")
    stream = producer()
    transformed = transform(stream, 10)
    async for value in transformed:
        print(f"  Pipeline output: {value}")


async def demonstrate_async_iterator_class() -> None:
    """Async iterator implemented as a class."""
    print("\n=== Async Iterator Class ===")
    async for value in AsyncCounter(5, 0.2):
        print(f"  Counter: {value}")


async def demonstrate_coroutine_chaining() -> None:
    """Chain coroutines and await results."""
    print("\n=== Coroutine Chaining ===")

    async def add(a, b):
        await asyncio.sleep(0.1)
        return a + b

    async def multiply(a, b):
        await asyncio.sleep(0.1)
        return a * b

    results = await chain_async(
        add(10, 20),
        multiply(5, 6),
        add(100, 200),
    )
    print(f"  Chained results: {results}")


async def demonstrate_concurrent_consumers() -> None:
    """Multiple consumers sharing an async generator."""
    print("\n=== Concurrent Consumers ===")

    async def feed_queue(queue: asyncio.Queue, n: int):
        for i in range(n):
            await queue.put(i)
            await asyncio.sleep(0.1)
        for _ in range(2):
            await queue.put(None)  # sentinels

    async def worker(name: str, queue: asyncio.Queue):
        while True:
            item = await queue.get()
            if item is None:
                queue.task_done()
                break
            print(f"  {name} processed {item}")
            queue.task_done()

    queue = asyncio.Queue()
    feeder = asyncio.create_task(feed_queue(queue, 6))
    workers = [asyncio.create_task(worker(f"Worker-{i}", queue)) for i in range(2)]

    await feeder
    await queue.join()
    for w in workers:
        w.cancel()

    print("  All items processed")


async def main():
    await demonstrate_async_generator_basics()
    await demonstrate_async_pipeline()
    await demonstrate_async_iterator_class()
    await demonstrate_coroutine_chaining()
    await demonstrate_concurrent_consumers()


if __name__ == "__main__":
    asyncio.run(main())
