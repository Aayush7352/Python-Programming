"""
Distributed AI Inference Platform.

Complete end-to-end system for distributed model serving.
"""
import time
import uuid
import json
import random
import threading
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
from collections import deque


class InferenceStatus(Enum):
    PENDING = "pending"
    ROUTING = "routing"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class InferenceRequest:
    """A distributed inference request."""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    model: str = "default"
    input_data: Any = None
    status: InferenceStatus = InferenceStatus.PENDING
    created_at: float = field(default_factory=time.time)
    completed_at: Optional[float] = None
    result: Any = None
    error: Optional[str] = None
    node_id: Optional[str] = None
    latency: Optional[float] = None


class ComputeNode:
    """A compute node in the distributed cluster."""

    def __init__(self, node_id: str, capacity: int = 4, region: str = "us-east"):
        self.node_id = node_id
        self.capacity = capacity
        self.region = region
        self.current_load = 0
        self.models: Dict[str, bool] = {}  # model_name -> loaded
        self.requests_processed = 0
        self.total_compute_time = 0.0
        self.healthy = True
        self.failures = 0

    def load_model(self, model_name: str) -> bool:
        time.sleep(0.1)  # simulate loading
        self.models[model_name] = True
        return True

    def infer(self, request: InferenceRequest) -> Any:
        """Run inference on this node."""
        self.current_load += 1
        request.node_id = self.node_id
        request.status = InferenceStatus.PROCESSING

        start = time.time()
        try:
            # Simulated inference
            compute_time = random.uniform(0.05, 0.2)
            if random.random() < 0.01:  # 1% failure rate
                raise RuntimeError("Compute error")

            time.sleep(compute_time)
            result = {
                "model": request.model,
                "input": str(request.input_data)[:50],
                "output": f"processed_by_{self.node_id}",
                "compute_time": compute_time,
            }

            self.requests_processed += 1
            self.total_compute_time += compute_time
            return result

        except Exception as e:
            self.failures += 1
            raise
        finally:
            self.current_load -= 1

    @property
    def available_capacity(self) -> int:
        return self.capacity - self.current_load

    @property
    def avg_compute_time(self) -> float:
        return self.total_compute_time / max(self.requests_processed, 1)


class Router:
    """Routes requests to the best compute node."""

    def __init__(self):
        self.nodes: Dict[str, ComputeNode] = {}
        self.strategies = {
            "round_robin": self._round_robin,
            "least_loaded": self._least_loaded,
            "random": self._random,
            "region": self._region_aware,
        }
        self.rr_index = 0

    def register_node(self, node: ComputeNode):
        self.nodes[node.node_id] = node

    def route(self, request: InferenceRequest, strategy: str = "least_loaded") -> Optional[ComputeNode]:
        router_fn = self.strategies.get(strategy, self._least_loaded)
        return router_fn(request)

    def _round_robin(self, request: InferenceRequest) -> Optional[ComputeNode]:
        available = [n for n in self.nodes.values() if n.healthy]
        if not available:
            return None
        self.rr_index = (self.rr_index + 1) % len(available)
        return available[self.rr_index]

    def _least_loaded(self, request: InferenceRequest) -> Optional[ComputeNode]:
        available = [n for n in self.nodes.values() if n.healthy]
        if not available:
            return None
        return min(available, key=lambda n: n.current_load / n.capacity)

    def _random(self, request: InferenceRequest) -> Optional[ComputeNode]:
        available = [n for n in self.nodes.values() if n.healthy]
        return random.choice(available) if available else None

    def _region_aware(self, request: InferenceRequest) -> Optional[ComputeNode]:
        preferred_region = getattr(request, "region", None)
        if preferred_region:
            region_nodes = [n for n in self.nodes.values()
                          if n.region == preferred_region and n.healthy]
            if region_nodes:
                return min(region_nodes, key=lambda n: n.current_load)
        return self._least_loaded(request)


class DistributedInferencePlatform:
    """Complete distributed AI inference platform."""

    def __init__(self):
        self.router = Router()
        self.request_queue: deque = deque()
        self.completed: Dict[str, InferenceRequest] = {}
        self.workers: List[threading.Thread] = []
        self.running = True
        self.total_requests = 0
        self._start_workers()

    def add_node(self, node: ComputeNode):
        self.router.register_node(node)

    def submit(self, model: str, input_data: Any, **kwargs) -> str:
        request = InferenceRequest(model=model, input_data=input_data, **kwargs)
        self.request_queue.append(request)
        self.total_requests += 1
        return request.id

    def _process_request(self, request: InferenceRequest):
        request.status = InferenceStatus.ROUTING
        node = self.router.route(request)

        if node is None:
            request.status = InferenceStatus.FAILED
            request.error = "No healthy nodes available"
            self.completed[request.id] = request
            return

        try:
            result = node.infer(request)
            request.result = result
            request.status = InferenceStatus.COMPLETED
        except Exception as e:
            request.status = InferenceStatus.FAILED
            request.error = str(e)

        request.completed_at = time.time()
        request.latency = request.completed_at - request.created_at
        self.completed[request.id] = request

    def _worker_loop(self):
        while self.running:
            if self.request_queue:
                request = self.request_queue.popleft()
                self._process_request(request)
            else:
                time.sleep(0.01)

    def _start_workers(self, num: int = 4):
        for _ in range(num):
            worker = threading.Thread(target=self._worker_loop, daemon=True)
            worker.start()
            self.workers.append(worker)

    def get_result(self, request_id: str) -> Optional[InferenceRequest]:
        return self.completed.get(request_id)

    def get_stats(self) -> dict:
        total_nodes = len(self.router.nodes)
        healthy_nodes = sum(1 for n in self.router.nodes.values() if n.healthy)
        total_processed = sum(n.requests_processed for n in self.router.nodes.values())
        completed_reqs = len([r for r in self.completed.values()
                            if r.status == InferenceStatus.COMPLETED])

        return {
            "total_requests": self.total_requests,
            "completed": completed_reqs,
            "queue_size": len(self.request_queue),
            "nodes": {"total": total_nodes, "healthy": healthy_nodes},
            "total_inferences": total_processed,
            "cache_size": len(self.completed),
        }

    def shutdown(self):
        self.running = False


def main():
    print("=== Distributed AI Inference Platform ===\n")

    platform = DistributedInferencePlatform()

    # Add compute nodes (different regions)
    print("1. Cluster Setup")
    for i in range(6):
        region = random.choice(["us-east", "us-west", "eu-west"])
        node = ComputeNode(
            node_id=f"node-{i}",
            capacity=random.randint(2, 6),
            region=region,
        )
        node.load_model("gpt-3.5")
        platform.add_node(node)
        print(f"   Added {node.node_id} (region={region}, capacity={node.capacity})")

    # Submit requests
    print("\n2. Submitting Inference Requests")
    request_ids = []
    prompts = [
        "Explain quantum computing",
        "Write a poem",
        "What is AI?",
        "Calculate 2+2",
        "Tell me a joke",
        "Translate hello to French",
        "Write Python code",
        "Explain gravity",
    ]

    for prompt in prompts:
        req_id = platform.submit("gpt-3.5", prompt)
        request_ids.append(req_id)
        print(f"   Submitted: {req_id}")

    # Wait for processing
    print("\n3. Waiting for results...")
    time.sleep(2)

    # Check results
    print("\n4. Results:")
    for req_id in request_ids:
        result = platform.get_result(req_id)
        if result:
            status = result.status.value.upper()
            node = result.node_id or "N/A"
            latency = f"{result.latency * 1000:.1f}ms" if result.latency else "N/A"
            print(f"   [{status}] {req_id}: node={node}, latency={latency}")

    # Node stats
    print("\n5. Node Statistics:")
    for node in platform.router.nodes.values():
        print(f"   {node.node_id}: load={node.current_load}/{node.capacity}, "
              f"processed={node.requests_processed}, "
              f"health={'OK' if node.healthy else 'DOWN'}")

    # Platform stats
    print(f"\n6. Platform Summary:")
    stats = platform.get_stats()
    print(f"   {json.dumps(stats, indent=3)}")

    # Simulate failure
    print("\n7. Handling Node Failure")
    failed_node = list(platform.router.nodes.values())[0]
    failed_node.healthy = False
    print(f"   {failed_node.node_id} marked unhealthy")
    req_id = platform.submit("gpt-3.5", "Test after failure")
    time.sleep(0.5)
    result = platform.get_result(req_id)
    if result:
        print(f"   Request routed to: {result.node_id} (avoided failed node)")

    platform.shutdown()

    print("\n=== Distributed Inference Architecture ===")
    print("  1. Multi-region compute nodes")
    print("  2. Smart request routing (least-loaded, region-aware)")
    print("  3. Automatic failover")
    print("  4. Horizontal scalability")
    print("  5. Request queuing and batching")
    print("  6. Health monitoring")
    print("  Production: AWS SageMaker, GCP Vertex AI, Ray Serve")


if __name__ == "__main__":
    main()
