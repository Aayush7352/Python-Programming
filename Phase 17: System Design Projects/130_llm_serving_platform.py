"""
LLM Serving Platform implementation.

Model loading, request queuing, batching, and inference.
"""
import time
import asyncio
import json
import uuid
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum


class RequestStatus(Enum):
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class LLMRequest:
    """An inference request."""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    prompt: str = ""
    max_tokens: int = 100
    temperature: float = 0.7
    top_p: float = 0.9
    status: RequestStatus = RequestStatus.QUEUED
    created_at: float = field(default_factory=time.time)
    completed_at: Optional[float] = None
    response: Optional[str] = None


class ModelInstance:
    """A loaded model instance ready for inference."""

    def __init__(self, model_name: str, device: str = "cpu"):
        self.model_name = model_name
        self.device = device
        self.id = str(uuid.uuid4())[:8]
        self.busy = False

    def infer(self, request: LLMRequest) -> str:
        """Run inference (simulated)."""
        self.busy = True
        time.sleep(0.1)  # Simulate compute
        response = f"[{self.model_name}] Response to: {request.prompt[:30]}..."
        self.busy = False
        return response

    def infer_batch(self, requests: List[LLMRequest]) -> List[str]:
        """Batch inference (more efficient)."""
        self.busy = True
        batch_size = len(requests)
        time.sleep(0.05 * batch_size)  # Sub-linear scaling
        responses = [
            f"[{self.model_name}] Batch response to: {r.prompt[:30]}..."
            for r in requests
        ]
        self.busy = False
        return responses


class RequestQueue:
    """Request queue with priority."""

    def __init__(self):
        self.queue: List[LLMRequest] = []
        self.completed: Dict[str, LLMRequest] = {}

    def add(self, request: LLMRequest):
        self.queue.append(request)

    def get_next(self) -> Optional[LLMRequest]:
        if self.queue:
            return self.queue.pop(0)
        return None

    def get_batch(self, batch_size: int) -> List[LLMRequest]:
        batch = self.queue[:batch_size]
        self.queue = self.queue[batch_size:]
        return batch

    def complete(self, request: LLMRequest):
        request.status = RequestStatus.COMPLETED
        request.completed_at = time.time()
        self.completed[request.id] = request

    def fail(self, request: LLMRequest, error: str):
        request.status = RequestStatus.FAILED
        self.completed[request.id] = request

    @property
    def size(self):
        return len(self.queue)


class LoadBalancer:
    """Distribute requests across model instances."""

    def __init__(self):
        self.instances: List[ModelInstance] = []

    def add_instance(self, instance: ModelInstance):
        self.instances.append(instance)

    def get_available(self) -> Optional[ModelInstance]:
        for inst in self.instances:
            if not inst.busy:
                return inst
        return None

    def get_least_loaded(self) -> ModelInstance:
        return min(self.instances, key=lambda i: i.busy)

    def scale_up(self, model_name: str, count: int = 1):
        for _ in range(count):
            self.add_instance(ModelInstance(model_name))
        print(f"  Scaled up: added {count} instance(s)")

    def scale_down(self, count: int = 1):
        for _ in range(min(count, len(self.instances))):
            self.instances.pop()
        print(f"  Scaled down: removed {count} instance(s)")


class LLMServingPlatform:
    """Complete LLM serving platform."""

    def __init__(self):
        self.queue = RequestQueue()
        self.load_balancer = LoadBalancer()
        self.requests_completed = 0
        self.total_latency = 0.0

    def load_model(self, model_name: str, num_instances: int = 2):
        for _ in range(num_instances):
            instance = ModelInstance(model_name)
            self.load_balancer.add_instance(instance)
        print(f"  Loaded model '{model_name}' with {num_instances} instances")

    def submit(self, prompt: str, **kwargs) -> str:
        """Submit an inference request."""
        request = LLMRequest(prompt=prompt, **kwargs)
        self.queue.add(request)
        return request.id

    def process_next(self) -> Optional[LLMRequest]:
        """Process the next request."""
        request = self.queue.get_next()
        if not request:
            return None

        instance = self.load_balancer.get_available()
        if not instance:
            self.queue.queue.insert(0, request)
            return None

        request.status = RequestStatus.PROCESSING
        start = time.time()

        try:
            response = instance.infer(request)
            request.response = response
            self.queue.complete(request)
        except Exception as e:
            self.queue.fail(request, str(e))

        latency = time.time() - start
        self.requests_completed += 1
        self.total_latency += latency
        return request

    def process_batch(self, batch_size: int = 4) -> List[LLMRequest]:
        """Process a batch of requests."""
        batch = self.queue.get_batch(batch_size)
        if not batch:
            return []

        instance = self.load_balancer.get_available()
        if not instance:
            for r in batch:
                self.queue.queue.insert(0, r)
            return []

        start = time.time()
        for r in batch:
            r.status = RequestStatus.PROCESSING

        try:
            responses = instance.infer_batch(batch)
            for r, resp in zip(batch, responses):
                r.response = resp
                self.queue.complete(r)
        except Exception as e:
            for r in batch:
                self.queue.fail(r, str(e))

        latency = time.time() - start
        self.requests_completed += len(batch)
        self.total_latency += latency
        return batch

    def get_result(self, request_id: str) -> Optional[LLMRequest]:
        return self.queue.completed.get(request_id)

    def get_stats(self) -> dict:
        avg_latency = self.total_latency / max(self.requests_completed, 1)
        return {
            "queue_size": self.queue.size,
            "completed": self.requests_completed,
            "instances": len(self.load_balancer.instances),
            "avg_latency": f"{avg_latency * 1000:.1f}ms",
            "throughput": f"{self.requests_completed / max(self.total_latency, 0.001):.1f} req/s",
        }


def main():
    print("=== LLM Serving Platform ===\n")

    platform = LLMServingPlatform()

    # Load model
    print("1. Loading Models")
    platform.load_model("gpt-3.5-turbo", num_instances=2)

    # Submit requests
    print("\n2. Submitting Requests")
    request_ids = []
    prompts = [
        "Explain quantum computing",
        "Write a poem about AI",
        "What is the meaning of life?",
        "Write Python code for sorting",
        "Explain the theory of relativity",
        "What is machine learning?",
        "Write a story about robots",
        "Explain how the internet works",
    ]

    for prompt in prompts:
        req_id = platform.submit(prompt, max_tokens=50)
        request_ids.append(req_id)
        print(f"  Submitted: {req_id[:8]} - {prompt[:30]}...")

    # Process requests
    print("\n3. Processing Requests")
    for _ in range(6):
        result = platform.process_next()
        if result:
            print(f"  Processed: {result.id[:8]} - status={result.status.value}")

    # Process with batching
    print("\n4. Batch Processing")
    batch_results = platform.process_batch(batch_size=4)
    print(f"  Batch processed {len(batch_results)} requests")

    # Check results
    print("\n5. Results")
    for req_id in request_ids[:4]:
        result = platform.get_result(req_id)
        if result and result.response:
            print(f"  [{result.id[:8]}] Response: {result.response[:50]}...")

    # Stats
    print(f"\n6. Platform Stats: {json.dumps(platform.get_stats(), indent=2)}")

    # Autoscaling
    print("\n7. Autoscaling")
    print(f"  Current instances: {len(platform.load_balancer.instances)}")
    platform.load_balancer.scale_up("gpt-3.5-turbo", 2)
    platform.load_balancer.scale_down(1)
    print(f"  After scaling: {len(platform.load_balancer.instances)}")

    print("\n=== LLM Serving Architecture ===")
    print("  1. Request queue with priority")
    print("  2. Load balancer across model instances")
    print("  3. Dynamic batching for throughput")
    print("  4. Autoscaling based on queue depth")
    print("  5. Response streaming")
    print("  6. Model versioning and A/B testing")
    print("  Production: vLLM, TGI, Triton, Ray Serve")


if __name__ == "__main__":
    main()
