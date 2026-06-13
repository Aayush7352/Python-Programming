"""
Model serving patterns and inference optimization.

Requires: pip install torch
"""
import sys
import time
import numpy as np
from typing import List, Optional
from dataclasses import dataclass


@dataclass
class ModelConfig:
    """Model configuration."""
    model_name: str
    max_batch_size: int = 32
    max_seq_length: int = 2048
    device: str = "cpu"
    precision: str = "fp32"


class ModelInferenceEngine:
    """Model inference engine with batching and caching."""

    def __init__(self, config: ModelConfig):
        self.config = config
        self.model = self._load_model()
        self.response_cache = {}
        self.request_queue: List[dict] = []

    def _load_model(self):
        """Simulate loading a model."""
        print(f"  Loading model '{self.config.model_name}'...")
        time.sleep(0.5)
        return {"loaded": True, "config": self.config}

    def predict_single(self, input_text: str) -> str:
        """Single prediction (no batching)."""
        time.sleep(0.1)  # Simulate compute
        return f"Response to: {input_text[:20]}..."

    def predict_batch(self, inputs: List[str]) -> List[str]:
        """Batch prediction (more efficient)."""
        batch_size = len(inputs)
        time.sleep(0.05 * batch_size)  # Sub-linear scaling
        return [f"Response to: {inp[:20]}..." for inp in inputs]

    def predict_with_cache(self, input_text: str) -> str:
        """Prediction with caching."""
        if input_text in self.response_cache:
            return self.response_cache[input_text]

        result = self.predict_single(input_text)
        self.response_cache[input_text] = result
        return result


class SimpleAPIServer:
    """Simulated API server for model serving."""

    def __init__(self, engine: ModelInferenceEngine):
        self.engine = engine
        self.requests_served = 0
        self.total_latency = 0.0

    def handle_request(self, input_text: str) -> dict:
        """Handle a single inference request."""
        start = time.time()
        result = self.engine.predict_single(input_text)
        latency = time.time() - start

        self.requests_served += 1
        self.total_latency += latency

        return {
            "result": result,
            "latency": latency,
            "model": self.engine.config.model_name,
        }

    def handle_batch_request(self, inputs: List[str]) -> List[dict]:
        """Handle batched inference request."""
        start = time.time()
        results = self.engine.predict_batch(inputs)
        latency = time.time() - start

        self.requests_served += len(inputs)
        self.total_latency += latency

        return [
            {"result": r, "latency": latency}
            for r in results
        ]

    def get_stats(self) -> dict:
        avg_latency = self.total_latency / max(self.requests_served, 1)
        return {
            "total_requests": self.requests_served,
            "avg_latency": avg_latency,
            "throughput": self.requests_served / max(self.total_latency, 0.001),
        }


def benchmark_throughput():
    """Benchmark single vs batch inference."""
    print("\n=== Throughput Comparison ===")

    config = ModelConfig("benchmark-model", max_batch_size=32, device="cpu")
    engine = ModelInferenceEngine(config)
    server = SimpleAPIServer(engine)

    n_requests = 20

    # Single requests
    start = time.time()
    for i in range(n_requests):
        server.handle_request(f"Request {i}")
    single_time = time.time() - start

    # Batched requests
    start = time.time()
    batch_size = 10
    for i in range(0, n_requests, batch_size):
        batch = [f"Batch request {j}" for j in range(i, min(i + batch_size, n_requests))]
        server.handle_batch_request(batch)
    batch_time = time.time() - start

    print(f"  Single: {single_time:.4f}s ({n_requests / single_time:.1f} req/s)")
    print(f"  Batch:  {batch_time:.4f}s ({n_requests / batch_time:.1f} req/s)")
    print(f"  Speedup: {single_time / batch_time:.1f}x")


def simulate_production_serving():
    """Simulate production serving scenario."""
    print("\n=== Production Serving Simulation ===")

    config = ModelConfig("production-model", device="cpu")
    engine = ModelInferenceEngine(config)

    # Warmup
    print("  Warming up...")
    for _ in range(3):
        engine.predict_single("warmup")

    # Load test
    n_requests = 50
    latencies = []

    print(f"  Serving {n_requests} requests...")
    start = time.time()
    for i in range(n_requests):
        t0 = time.time()
        engine.predict_single(f"User request {i}")
        latencies.append(time.time() - t0)

    total_time = time.time() - start
    p50 = sorted(latencies)[len(latencies) // 2]
    p99 = sorted(latencies)[int(len(latencies) * 0.99)]

    print(f"  Total time: {total_time:.2f}s")
    print(f"  Throughput: {n_requests / total_time:.1f} req/s")
    print(f"  P50 latency: {p50 * 1000:.1f}ms")
    print(f"  P99 latency: {p99 * 1000:.1f}ms")


def main():
    print("=== Model Serving Patterns ===\n")

    # Basic serving
    print("1. Basic Model Serving")
    config = ModelConfig("my-model")
    engine = ModelInferenceEngine(config)
    server = SimpleAPIServer(engine)

    result = server.handle_request("Hello, model!")
    print(f"   Response: {result['result']}")
    print(f"   Latency: {result['latency'] * 1000:.1f}ms")

    # Caching
    print("\n2. Response Caching")
    start = time.time()
    engine.predict_with_cache("test input")
    first_time = time.time() - start

    start = time.time()
    engine.predict_with_cache("test input")
    cached_time = time.time() - start
    print(f"  First call: {first_time * 1000:.1f}ms")
    print(f"  Cached call: {cached_time * 1000:.1f}ms")

    benchmark_throughput()
    simulate_production_serving()

    print("\n=== Model Serving Strategies ===")
    print("  1. Online: real-time, low latency")
    print("  2. Batch: higher throughput")
    print("  3. Streaming: token-by-token")
    print("  4. Async: non-blocking requests")
    print("  5. Serverless: auto-scaling")
    print("\n  Optimization:")
    print("    - Response caching")
    print("    - Request batching")
    print("    - Model quantization")
    print("    - GPU acceleration")
    print("    - Continuous batching")
    print("  Tools: TorchServe, Triton, BentoML, Ray Serve")


if __name__ == "__main__":
    main()
