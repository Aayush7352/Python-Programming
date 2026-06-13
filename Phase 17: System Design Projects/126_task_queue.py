"""
Task queue implementation with workers.
"""
import time
import uuid
import threading
import random
from typing import Callable, Dict, Optional, List
from enum import Enum
from collections import deque


class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class Task:
    """Represents a unit of work."""

    def __init__(self, func: Callable, *args, **kwargs):
        self.id = str(uuid.uuid4())[:8]
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.status = TaskStatus.PENDING
        self.result = None
        self.error = None
        self.created_at = time.time()
        self.started_at = None
        self.completed_at = None
        self.retries = 0
        self.max_retries = 3

    def execute(self):
        """Execute the task."""
        self.status = TaskStatus.RUNNING
        self.started_at = time.time()
        try:
            self.result = self.func(*self.args, **self.kwargs)
            self.status = TaskStatus.COMPLETED
        except Exception as e:
            self.error = str(e)
            if self.retries < self.max_retries:
                self.retries += 1
                self.status = TaskStatus.PENDING
            else:
                self.status = TaskStatus.FAILED
        self.completed_at = time.time()

    @property
    def duration(self) -> Optional[float]:
        if self.started_at and self.completed_at:
            return self.completed_at - self.started_at
        return None

    def __repr__(self):
        return f"Task({self.id}, {self.func.__name__}, {self.status.value})"


class TaskQueue:
    """Queue that manages task execution."""

    def __init__(self, num_workers: int = 2):
        self.queue = deque()
        self.tasks: Dict[str, Task] = {}
        self.results: Dict[str, Task] = {}
        self.lock = threading.Lock()
        self.condition = threading.Condition(self.lock)
        self.running = True
        self.workers = []
        self.num_workers = num_workers
        self._start_workers()

    def enqueue(self, func: Callable, *args, **kwargs) -> str:
        """Add a task to the queue."""
        task = Task(func, *args, **kwargs)
        with self.lock:
            self.queue.append(task)
            self.tasks[task.id] = task
            self.condition.notify()
        return task.id

    def get_task(self, task_id: str) -> Optional[Task]:
        return self.tasks.get(task_id)

    def get_result(self, task_id: str) -> Optional[Task]:
        return self.results.get(task_id)

    def wait_for_result(self, task_id: str, timeout: float = 10.0) -> Optional[Task]:
        """Wait for a task to complete."""
        start = time.time()
        while time.time() - start < timeout:
            result = self.get_result(task_id)
            if result:
                return result
            time.sleep(0.1)
        return None

    def _worker_loop(self, worker_id: int):
        """Worker thread that processes tasks."""
        while self.running:
            task = None
            with self.lock:
                while not self.queue and self.running:
                    self.condition.wait(timeout=1.0)
                if self.queue and self.running:
                    task = self.queue.popleft()

            if task:
                print(f"  [Worker {worker_id}] Executing {task}")
                task.execute()
                with self.lock:
                    self.results[task.id] = task
                print(f"  [Worker {worker_id}] Completed {task} "
                      f"(duration={task.duration:.3f}s)")

    def _start_workers(self):
        for i in range(self.num_workers):
            worker = threading.Thread(
                target=self._worker_loop, args=(i,), daemon=True
            )
            worker.start()
            self.workers.append(worker)

    def shutdown(self):
        self.running = False
        with self.lock:
            self.condition.notify_all()


# Sample tasks
def process_data(n: int) -> str:
    time.sleep(random.uniform(0.1, 0.5))
    return f"Processed {n}"

def compute_sum(data: list) -> int:
    time.sleep(random.uniform(0.2, 0.6))
    return sum(data)

def failing_task() -> str:
    time.sleep(0.1)
    raise ValueError("Simulated failure")


def main():
    print("=== Task Queue ===\n")

    queue = TaskQueue(num_workers=3)

    # Enqueue tasks
    print("Enqueuing tasks...")
    task_ids = []

    for i in range(5):
        task_id = queue.enqueue(process_data, i * 10)
        task_ids.append(task_id)
        print(f"  Enqueued: {task_id}")

    task_id = queue.enqueue(compute_sum, [1, 2, 3, 4, 5])
    task_ids.append(task_id)
    print(f"  Enqueued: {task_id}")

    task_id = queue.enqueue(failing_task)
    task_ids.append(task_id)
    print(f"  Enqueued: {task_id}")

    # Wait for results
    print("\nWaiting for results...")
    time.sleep(2)

    print("\nResults:")
    for tid in task_ids:
        task = queue.get_result(tid) or queue.get_task(tid)
        if task:
            print(f"  [{task.status.value.upper()}] {task.func.__name__} "
                  f"({task.duration:.3f}s): {task.result}")

    # Queue stats
    print(f"\nQueue stats:")
    print(f"  Pending: {sum(1 for t in queue.tasks.values() if t.status == TaskStatus.PENDING)}")
    print(f"  Completed: {sum(1 for t in queue.tasks.values() if t.status == TaskStatus.COMPLETED)}")
    print(f"  Failed: {sum(1 for t in queue.tasks.values() if t.status == TaskStatus.FAILED)}")

    queue.shutdown()

    print("\n=== Task Queue Architecture ===")
    print("  1. Producers enqueue tasks")
    print("  2. Workers process tasks from queue")
    print("  3. Retry mechanism for failures")
    print("  4. Result storage for async retrieval")
    print("  5. Horizontal worker scaling")
    print("  Production: Celery, Redis Queue, SQS")


if __name__ == "__main__":
    main()
