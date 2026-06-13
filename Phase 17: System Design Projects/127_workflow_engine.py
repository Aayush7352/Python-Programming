"""
Workflow engine implementation with DAG execution.
"""
import time
import uuid
from typing import Dict, List, Callable, Optional, Any
from enum import Enum
from collections import deque


class WorkflowStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


class WorkflowTask:
    """A task/node in the workflow DAG."""

    def __init__(self, name: str, func: Callable,
                 dependencies: List[str] = None,
                 retries: int = 0):
        self.name = name
        self.func = func
        self.dependencies = dependencies or []
        self.retries = retries
        self.status = TaskStatus.PENDING
        self.result = None
        self.error = None
        self.execution_time = None

    def execute(self, context: dict) -> Any:
        """Execute the task with context."""
        self.status = TaskStatus.RUNNING
        start = time.time()
        try:
            self.result = self.func(context)
            self.status = TaskStatus.COMPLETED
        except Exception as e:
            self.error = str(e)
            self.status = TaskStatus.FAILED
        self.execution_time = time.time() - start
        return self.result


class Workflow:
    """DAG-based workflow."""

    def __init__(self, name: str):
        self.name = name
        self.tasks: Dict[str, WorkflowTask] = {}
        self.id = str(uuid.uuid4())[:8]
        self.status = WorkflowStatus.PENDING
        self.context = {}
        self.created_at = time.time()

    def add_task(self, task: WorkflowTask):
        self.tasks[task.name] = task

    def get_execution_order(self) -> List[str]:
        """Topological sort of tasks."""
        in_degree = {}
        for name, task in self.tasks.items():
            in_degree[name] = len(task.dependencies)

        queue = deque([name for name, deg in in_degree.items() if deg == 0])
        order = []

        while queue:
            name = queue.popleft()
            order.append(name)
            for other_name, other_task in self.tasks.items():
                if name in other_task.dependencies:
                    in_degree[other_name] -= 1
                    if in_degree[other_name] == 0:
                        queue.append(other_name)

        if len(order) != len(self.tasks):
            raise ValueError("Circular dependency detected in workflow")
        return order


class WorkflowEngine:
    """Executes workflows in order."""

    def __init__(self):
        self.workflows: Dict[str, Workflow] = {}
        self.history: List = []

    def register(self, workflow: Workflow):
        self.workflows[workflow.id] = workflow

    def execute(self, workflow_id: str) -> Workflow:
        workflow = self.workflows[workflow_id]
        workflow.status = WorkflowStatus.RUNNING
        print(f"  Executing workflow: {workflow.name} ({workflow_id})")

        try:
            order = workflow.get_execution_order()
            print(f"  Execution order: {order}")

            for task_name in order:
                task = workflow.tasks[task_name]
                deps_met = all(
                    workflow.tasks[d].status == TaskStatus.COMPLETED
                    for d in task.dependencies
                )

                if not deps_met:
                    task.status = TaskStatus.SKIPPED
                    print(f"    [SKIPPED] {task_name}: dependencies not met")
                    continue

                print(f"    [EXECUTING] {task_name}...")
                task.execute(workflow.context)
                status = task.status.value.upper()
                print(f"    [{status}] {task_name} "
                      f"({task.execution_time:.3f}s)")

                if task.status == TaskStatus.FAILED:
                    print(f"      Error: {task.error}")
                    if task.retries > 0:
                        for attempt in range(task.retries):
                            print(f"      Retry {attempt + 1}/{task.retries}...")
                            task.status = TaskStatus.PENDING
                            task.execute(workflow.context)
                            if task.status == TaskStatus.COMPLETED:
                                break

                if task.status == TaskStatus.FAILED:
                    workflow.status = WorkflowStatus.FAILED
                    self.history.append({
                        "workflow_id": workflow_id,
                        "status": "failed",
                        "failed_task": task_name,
                        "error": task.error,
                    })
                    return workflow

            workflow.status = WorkflowStatus.COMPLETED
            self.history.append({
                "workflow_id": workflow_id,
                "status": "completed",
                "duration": time.time() - workflow.created_at,
            })

        except Exception as e:
            workflow.status = WorkflowStatus.FAILED
            print(f"  Workflow failed: {e}")

        return workflow


def main():
    print("=== Workflow Engine ===\n")

    engine = WorkflowEngine()

    # Define tasks
    def fetch_data(ctx):
        print("    Fetching data from API...")
        time.sleep(0.2)
        ctx["data"] = [1, 2, 3, 4, 5]
        return ctx["data"]

    def validate_data(ctx):
        print("    Validating data...")
        data = ctx.get("data", [])
        assert len(data) > 0, "Empty data"
        ctx["validated"] = True
        return True

    def process_data(ctx):
        print("    Processing data...")
        data = ctx.get("data", [])
        ctx["processed"] = [x * 2 for x in data]
        return ctx["processed"]

    def analyze_results(ctx):
        print("    Analyzing results...")
        processed = ctx.get("processed", [])
        ctx["analysis"] = {
            "sum": sum(processed),
            "mean": sum(processed) / len(processed) if processed else 0,
            "count": len(processed),
        }
        return ctx["analysis"]

    def generate_report(ctx):
        print("    Generating report...")
        analysis = ctx.get("analysis", {})
        ctx["report"] = f"Report: {analysis}"
        return ctx["report"]

    def send_notification(ctx):
        print("    Sending notification...")
        time.sleep(0.1)
        ctx["notified"] = True
        return "Notification sent"

    # Create workflows
    workflow = Workflow("Data Processing Pipeline")

    workflow.add_task(WorkflowTask("fetch", fetch_data))
    workflow.add_task(WorkflowTask("validate", validate_data, ["fetch"]))
    workflow.add_task(WorkflowTask("process", process_data, ["validate"]))
    workflow.add_task(WorkflowTask("analyze", analyze_results, ["process"]))
    workflow.add_task(WorkflowTask("report", generate_report, ["analyze"]))
    workflow.add_task(WorkflowTask("notify", send_notification, ["report"]))

    engine.register(workflow)
    result = engine.execute(workflow.id)

    print(f"\nWorkflow status: {result.status.value}")
    print(f"Context keys: {list(result.context.keys())}")
    print(f"Analysis: {result.context.get('analysis')}")

    # Workflow with failure and retry
    print("\n--- Workflow with Failure ---")
    def potentially_failing(ctx):
        import random
        if random.random() < 0.7:
            raise ValueError("Random failure")
        ctx["success"] = True
        return "Success!"

    wf2 = Workflow("Retry Workflow")
    wf2.add_task(WorkflowTask("risky_task", potentially_failing, retries=2))
    engine.register(wf2)
    result2 = engine.execute(wf2.id)
    print(f"Workflow status: {result2.status.value}")

    print("\n=== Workflow Engine Features ===")
    print("  1. DAG-based task orchestration")
    print("  2. Topological execution order")
    print("  3. Dependency management")
    print("  4. Automatic retries on failure")
    print("  5. Context sharing between tasks")
    print("  6. Execution history tracking")
    print("  Production: Airflow, Prefect, Temporal")


if __name__ == "__main__":
    main()
