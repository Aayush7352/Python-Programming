import asyncio
import time
import random


async def say_hello(delay: float, name: str) -> str:
    """Async function that sleeps and returns."""
    await asyncio.sleep(delay)
    message = f"Hello, {name}! (after {delay}s)"
    return message


async def fetch_data(url: str, delay: float) -> dict:
    """Simulate fetching data from a URL."""
    print(f"  Fetching {url}...")
    await asyncio.sleep(delay)
    result = {"url": url, "data": f"Data from {url}", "delay": delay}
    print(f"  Done fetching {url}")
    return result


async def count_down(name: str, count: int, delay: float) -> None:
    """Count down with delays."""
    for i in range(count, 0, -1):
        print(f"  {name}: {i}")
        await asyncio.sleep(delay)
    print(f"  {name}: Liftoff!")


async def demonstrate_gather() -> None:
    """Run multiple coroutines concurrently with gather."""
    print("=== gather() ===")
    results = await asyncio.gather(
        say_hello(1, "Alice"),
        say_hello(0.5, "Bob"),
        say_hello(0.2, "Charlie"),
        say_hello(0.8, "Diana"),
    )
    for result in results:
        print(f"  {result}")


async def demonstrate_create_task() -> None:
    """Create tasks manually."""
    print("\n=== create_task() ===")
    task1 = asyncio.create_task(count_down("Timer 1", 3, 0.5))
    task2 = asyncio.create_task(count_down("Timer 2", 5, 0.3))

    print("  Tasks created, waiting for completion...")
    await task1
    await task2
    print("  All tasks done")


async def demonstrate_as_completed() -> None:
    """Process results as they complete."""
    print("\n=== as_completed() ===")

    async def random_delay_task(n: int) -> str:
        delay = random.uniform(0.5, 2.0)
        await asyncio.sleep(delay)
        return f"Task {n} done in {delay:.2f}s"

    tasks = [random_delay_task(i) for i in range(5)]
    for coro in asyncio.as_completed(tasks):
        result = await coro
        print(f"  {result}")


async def demonstrate_timeout() -> None:
    """Handle timeouts with asyncio."""
    print("\n=== Timeout ===")

    async def slow_task() -> str:
        await asyncio.sleep(5)
        return "Slow result"

    try:
        result = await asyncio.wait_for(slow_task(), timeout=1.0)
        print(f"  Result: {result}")
    except TimeoutError:
        print("  Task timed out (as expected)")


async def demonstrate_async_generator() -> None:
    """Async generator and async iteration."""
    print("\n=== Async Generator ===")

    async def produce_numbers(max_n: int):
        for i in range(max_n):
            await asyncio.sleep(0.1)
            yield i

    async def square_numbers(numbers):
        async for num in numbers:
            yield num ** 2

    async for squared in square_numbers(produce_numbers(5)):
        print(f"  Squared: {squared}")


async def demonstrate_semaphore() -> None:
    """Limit concurrency with semaphore."""
    print("\n=== Semaphore (Limit Concurrency) ===")
    sem = asyncio.Semaphore(3)

    async def limited_task(n: int) -> str:
        async with sem:
            print(f"  Task {n}: starting")
            await asyncio.sleep(random.uniform(0.5, 1.5))
            print(f"  Task {n}: finished")
        return f"Task {n} done"

    tasks = [limited_task(i) for i in range(8)]
    results = await asyncio.gather(*tasks)
    print(f"  All {len(results)} tasks done")


async def main():
    start = time.time()

    await demonstrate_gather()
    await demonstrate_create_task()
    await demonstrate_as_completed()
    await demonstrate_timeout()
    await demonstrate_async_generator()
    await demonstrate_semaphore()

    elapsed = time.time() - start
    print(f"\nTotal elapsed: {elapsed:.2f}s")


if __name__ == "__main__":
    asyncio.run(main())
