"""
Multi-Agent System (MAS) implementation.

Multiple agents coordinate to solve complex tasks.
"""
import time
import json
from typing import Dict, List, Callable, Any, Optional
from dataclasses import dataclass, field
from enum import Enum


class MessageType(Enum):
    TASK = "task"
    RESULT = "result"
    QUERY = "query"
    RESPONSE = "response"
    BROADCAST = "broadcast"
    STATUS = "status"


@dataclass
class AgentMessage:
    """Message exchanged between agents."""
    sender: str
    receiver: str
    msg_type: MessageType
    content: str
    metadata: dict = field(default_factory=dict)
    id: str = ""


@dataclass
class AgentCapability:
    """What an agent can do."""
    name: str
    description: str
    execute: Callable


class Agent:
    """Base agent class."""

    def __init__(self, name: str, capabilities: List[AgentCapability] = None):
        self.name = name
        self.capabilities = capabilities or []
        self.mailbox: List[AgentMessage] = []
        self.knowledge: Dict[str, Any] = {}
        self.busy = False

    def can_handle(self, task: str) -> bool:
        """Check if any capability can handle the task."""
        task_lower = task.lower()
        for cap in self.capabilities:
            if cap.name.lower() in task_lower:
                return True
        return False

    def process_message(self, msg: AgentMessage) -> AgentMessage:
        """Process an incoming message and return response."""
        self.busy = True

        if msg.msg_type == MessageType.TASK:
            result = self._execute_task(msg.content)
            self.busy = False
            return AgentMessage(
                sender=self.name,
                receiver=msg.sender,
                msg_type=MessageType.RESULT,
                content=result,
            )

        elif msg.msg_type == MessageType.QUERY:
            response = self._answer_query(msg.content)
            self.busy = False
            return AgentMessage(
                sender=self.name,
                receiver=msg.sender,
                msg_type=MessageType.RESPONSE,
                content=response,
            )

        self.busy = False
        return AgentMessage(
            sender=self.name, receiver=msg.sender,
            msg_type=MessageType.RESPONSE,
            content=f"I don't understand this message type: {msg.msg_type}"
        )

    def _execute_task(self, task: str) -> str:
        """Execute a task using capabilities."""
        task_lower = task.lower()
        for cap in self.capabilities:
            if cap.name.lower() in task_lower:
                return cap.execute(task)
        return f"Task '{task}' not supported by {self.name}"

    def _answer_query(self, query: str) -> str:
        """Answer a query from knowledge or capabilities."""
        for key, value in self.knowledge.items():
            if key.lower() in query.lower():
                return f"{key}: {value}"
        return f"I don't have information about that."

    def send_message(self, receiver: "Agent", msg: AgentMessage):
        receiver.mailbox.append(msg)


class CoordinatorAgent(Agent):
    """Coordinator that delegates tasks to specialist agents."""

    def __init__(self, name: str = "Coordinator"):
        super().__init__(name, [
            AgentCapability("coordinate", "Coordinate tasks between agents",
                           lambda t: "Task coordinated")
        ])
        self.specialists: Dict[str, Agent] = {}

    def register_agent(self, agent: Agent):
        self.specialists[agent.name] = agent
        print(f"  Registered agent: {agent.name}")

    def delegate_task(self, task: str) -> str:
        """Find the right agent and delegate."""
        print(f"\n  [Coordinator] Analyzing task: '{task}'")

        # Find capable agent
        for name, agent in self.specialists.items():
            if agent.can_handle(task):
                print(f"  [Coordinator] Delegating to {name}")
                msg = AgentMessage(
                    sender=self.name, receiver=name,
                    msg_type=MessageType.TASK,
                    content=task,
                )
                response = agent.process_message(msg)
                return f"[{name}]: {response.content}"

        # If no specialist, try broadcasting
        print(f"  [Coordinator] Broadcasting to all agents")
        for name, agent in self.specialists.items():
            msg = AgentMessage(
                sender=self.name, receiver=name,
                msg_type=MessageType.TASK, content=task,
            )
            response = agent.process_message(msg)
            if "not supported" not in response.content:
                return f"[{name}]: {response.content}"

        return "No agent can handle this task"


def main():
    print("=== Multi-Agent System ===\n")

    # Create specialist agents
    def research_fn(task: str) -> str:
        time.sleep(0.1)
        return f"Research results for: {task}"

    def code_fn(task: str) -> str:
        time.sleep(0.1)
        return f"Generated code for: {task}"

    def math_fn(task: str) -> str:
        time.sleep(0.05)
        import re
        nums = re.findall(r"\d+", task)
        if nums:
            total = sum(int(n) for n in nums)
            return f"Calculated: {total}"
        return "No numbers found to calculate"

    researcher = Agent("Researcher", [
        AgentCapability("research", "Research topics", research_fn),
        AgentCapability("search", "Search information", research_fn),
    ])

    coder = Agent("Coder", [
        AgentCapability("code", "Write code", code_fn),
        AgentCapability("programming", "Programming tasks", code_fn),
        AgentCapability("python", "Python programming", code_fn),
    ])

    mathematician = Agent("Mathematician", [
        AgentCapability("math", "Do math", math_fn),
        AgentCapability("calculate", "Calculate", math_fn),
        AgentCapability("compute", "Compute values", math_fn),
    ])

    # Add knowledge
    researcher.knowledge = {
        "Python": "Python is created by Guido van Rossum",
        "AI": "Artificial Intelligence",
    }

    # Coordinator
    coordinator = CoordinatorAgent()
    coordinator.register_agent(researcher)
    coordinator.register_agent(coder)
    coordinator.register_agent(mathematician)

    # Tasks
    tasks = [
        "Research the history of Python",
        "Write Python code for a calculator",
        "Calculate 10 + 20 + 30 + 40",
        "What is the capital of France?",
    ]

    print("Delegating tasks:")
    for task in tasks:
        result = coordinator.delegate_task(task)
        print(f"  Result: {result}")
        time.sleep(0.1)

    # Agent communication
    print("\n=== Direct Agent Communication ===")
    msg = AgentMessage(
        sender="User", receiver="Researcher",
        msg_type=MessageType.QUERY,
        content="Python",
    )
    response = researcher.process_message(msg)
    print(f"  Query 'Python' -> Researcher: {response.content}")

    # Status
    print("\n=== System Status ===")
    print(f"  Registered agents: {list(coordinator.specialists.keys())}")
    for name, agent in coordinator.specialists.items():
        print(f"  {name}: busy={agent.busy}, "
              f"capabilities={[c.name for c in agent.capabilities]}, "
              f"knowledge={len(agent.knowledge)} items")

    print("\n=== Multi-Agent System Features ===")
    print("  1. Specialized agents with capabilities")
    print("  2. Coordinator for task delegation")
    print("  3. Direct inter-agent communication")
    print("  4. Shared knowledge and messaging")
    print("  5. Distributed task execution")
    print("  Production: CrewAI, AutoGen, LangGraph")


if __name__ == "__main__":
    main()
