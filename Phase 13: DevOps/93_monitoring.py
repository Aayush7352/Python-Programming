"""
Monitoring and observability patterns in Python.

Demonstrates metrics collection, health checks, and profiling.
"""
import time
import functools
import threading
from typing import Dict, List, Callable
from collections import defaultdict
import json


class MetricsCollector:
    """Simple metrics collection system."""

    def __init__(self):
        self._counters = defaultdict(int)
        self._gauges = defaultdict(float)
        self._histograms = defaultdict(list)
        self._lock = threading.Lock()

    def increment(self, name: str, value: int = 1):
        with self._lock:
            self._counters[name] += value

    def gauge(self, name: str, value: float):
        with self._lock:
            self._gauges[name] = value

    def observe(self, name: str, value: float):
        with self._lock:
            self._histograms[name].append(value)
            # Keep only last 1000 observations
            if len(self._histograms[name]) > 1000:
                self._histograms[name] = self._histograms[name][-1000:]

    def get_snapshot(self) -> dict:
        with self._lock:
            histograms = {}
            for name, values in self._histograms.items():
                if values:
                    histograms[name] = {
                        "count": len(values),
                        "min": min(values),
                        "max": max(values),
                        "avg": sum(values) / len(values),
                        "p50": sorted(values)[len(values) // 2],
                    }
                else:
                    histograms[name] = {"count": 0}

            return {
                "counters": dict(self._counters),
                "gauges": dict(self._gauges),
                "histograms": histograms,
            }

    def report(self):
        """Print metrics snapshot."""
        snapshot = self.get_snapshot()
        print(json.dumps(snapshot, indent=2))


metrics = MetricsCollector()


def monitor(func: Callable) -> Callable:
    """Decorator that monitors function calls."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        metrics.increment(f"{func.__name__}.calls")
        start = time.perf_counter()
        try:
            result = func(*args, **kwargs)
            elapsed = time.perf_counter() - start
            metrics.observe(f"{func.__name__}.duration", elapsed)
            metrics.increment(f"{func.__name__}.success")
            return result
        except Exception as e:
            metrics.increment(f"{func.__name__}.errors")
            raise
    return wrapper


class HealthChecker:
    """System health checker."""

    def __init__(self):
        self._checks: Dict[str, Callable] = {}
        self._results: Dict[str, dict] = {}

    def register(self, name: str, check_fn: Callable, interval: float = 30.0):
        self._checks[name] = check_fn
        self._results[name] = {
            "status": "unknown",
            "last_check": 0,
            "interval": interval,
        }

    def check_all(self) -> dict:
        now = time.time()
        for name, check_fn in self._checks.items():
            result = self._results[name]
            if now - result["last_check"] >= result["interval"]:
                try:
                    check_fn()
                    result["status"] = "healthy"
                except Exception as e:
                    result["status"] = "unhealthy"
                    result["error"] = str(e)
                result["last_check"] = now
        return self.get_status()

    def get_status(self) -> dict:
        overall = all(r["status"] == "healthy" for r in self._results.values())
        return {
            "status": "healthy" if overall else "degraded",
            "checks": dict(self._results),
        }


class Profiler:
    """Simple code profiler."""

    def __init__(self):
        self._timings: Dict[str, List[float]] = defaultdict(list)

    @contextmanager
    def profile(self, name: str):
        start = time.perf_counter()
        try:
            yield
        finally:
            elapsed = time.perf_counter() - start
            self._timings[name].append(elapsed)

    def summary(self) -> dict:
        result = {}
        for name, times in self._timings.items():
            result[name] = {
                "calls": len(times),
                "total": sum(times),
                "avg": sum(times) / len(times) if times else 0,
                "min": min(times) if times else 0,
                "max": max(times) if times else 0,
            }
        return result


@monitor
def process_data(n: int) -> int:
    """Simulate data processing."""
    time.sleep(0.01)
    return sum(range(n))


@monitor
def query_database(query: str) -> str:
    """Simulate database query."""
    time.sleep(0.02)
    if "error" in query.lower():
        raise RuntimeError("Simulated error")
    return f"Results for: {query}"


def main():
    from contextlib import contextmanager

    print("=== Metrics Collection ===")
    for i in range(50):
        process_data(1000)
        if i % 10 == 0:
            try:
                query_database("SELECT * FROM users")
            except RuntimeError:
                pass

    metrics.gauge("memory_usage_mb", 45.2)
    metrics.gauge("cpu_percent", 23.5)

    print("  Metrics snapshot:")
    metrics.report()

    print("\n=== Health Check ===")
    health = HealthChecker()
    health.register("database", lambda: None)  # would be real check
    health.register("cache", lambda: time.sleep(0.01))
    health.register("disk_space", lambda: None)

    status = health.check_all()
    print(f"  System status: {json.dumps(status, indent=4)}")

    print("\n=== Profiling ===")
    profiler = Profiler()
    for _ in range(100):
        with profiler.profile("fast_operation"):
            time.sleep(0.001)
        with profiler.profile("slow_operation"):
            time.sleep(0.005)

    profile_summary = profiler.summary()
    for name, stats in profile_summary.items():
        print(f"  {name}: {stats}")

    print("\n=== Monitoring Best Practices ===")
    print("  1. Collect RED metrics (Rate, Errors, Duration)")
    print("  2. Use USE method (Utilization, Saturation, Errors)")
    print("  3. Implement health checks for all services")
    print("  4. Set up alerting on key metrics")
    print("  5. Use structured logging with metrics")
    print("  6. Monitor both technical and business metrics")
    print("  7. Distributed tracing for microservices")


if __name__ == "__main__":
    main()
