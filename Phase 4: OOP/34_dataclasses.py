from dataclasses import dataclass, field, asdict, astuple
from typing import List, Optional
from enum import Enum


class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


@dataclass(order=True)
class Task:
    """Simple dataclass with ordering support."""
    priority: Priority
    title: str = field(compare=False)
    completed: bool = field(default=False, compare=False)


@dataclass
class Employee:
    """Dataclass with computed fields and defaults."""
    name: str
    employee_id: str
    department: str
    salary: float = 0.0
    skills: List[str] = field(default_factory=list)
    metadata: dict = field(default_factory=dict, repr=False)

    @property
    def annual_bonus(self) -> float:
        return self.salary * 0.1 if self.salary > 0 else 0

    def add_skill(self, skill: str) -> None:
        if skill not in self.skills:
            self.skills.append(skill)


@dataclass(frozen=True)
class Point:
    """Immutable dataclass."""
    x: float
    y: float
    z: float = 0.0


@dataclass
class Project:
    """Dataclass with nested dataclass."""
    name: str
    members: List[Employee] = field(default_factory=list)
    tasks: List[Task] = field(default_factory=list)
    budget: float = 0.0

    def total_salary_cost(self) -> float:
        return sum(emp.salary for emp in self.members)


def main():
    print("=== Basic Dataclass ===")
    task1 = Task(Priority.HIGH, "Fix critical bug")
    task2 = Task(Priority.MEDIUM, "Write documentation")
    task3 = Task(Priority.LOW, "Refactor code", completed=True)

    print(f"  {task1}")
    print(f"  {task2}")
    print(f"  {task3}")

    print("\n=== Dataclass Comparison ===")
    tasks = [task1, task2, task3]
    sorted_tasks = sorted(tasks)
    for t in sorted_tasks:
        print(f"  {t.priority.name}: {t.title}")

    print("\n=== Dataclass with Properties ===")
    emp = Employee("Alice Smith", "E001", "Engineering", 85000)
    emp.add_skill("Python")
    emp.add_skill("Docker")
    print(f"  {emp}")
    print(f"  Annual bonus: ${emp.annual_bonus:.2f}")
    print(f"  Skills: {emp.skills}")

    print("\n=== Frozen (Immutable) Dataclass ===")
    p = Point(3.0, 4.0)
    print(f"  {p}")
    try:
        p.x = 10.0
    except Exception as e:
        print(f"  Cannot modify frozen: {e}")

    print("\n=== Serialization ===")
    print(f"  asdict: {asdict(emp)}")
    print(f"  astuple: {astuple(p)}")

    print("\n=== Nested Dataclasses ===")
    project = Project("AI Platform")
    project.members.append(emp)
    project.members.append(Employee("Bob Jones", "E002", "Engineering", 92000))
    project.tasks.extend([task1, task2])
    print(f"  {project.name}")
    print(f"  Total salary: ${project.total_salary_cost():,.2f}")
    print(f"  Task count: {len(project.tasks)}")


if __name__ == "__main__":
    main()
