"""PawPal+ domain model.

Implements the classes from diagrams/uml.mmd: Owner, Pet, Task, and Scheduler.
The Scheduler turns a set of tasks into a time-ordered daily plan under a
time budget, and can explain the plan it produced.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, time, timedelta
from enum import Enum
from uuid import uuid4


class Priority(Enum):
    """Task importance, used by the Scheduler to order tasks."""

    HIGH = 3
    MEDIUM = 2
    LOW = 1


@dataclass
class Task:
    """A single pet care task (walk, feeding, meds, etc.)."""

    title: str
    description: str = ""
    due_date: date | None = None
    duration: int = 0  # minutes
    priority: Priority = Priority.MEDIUM
    pet_name: str = ""  # which pet this task belongs to (for display)
    id: str = field(default_factory=lambda: uuid4().hex)
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark this task as done."""
        self.completed = True


@dataclass
class PlanEntry:
    """A task placed at a specific start time in the daily plan."""

    task: Task
    start_time: time


@dataclass
class Pet:
    """A pet and its list of care tasks."""

    name: str
    age: int = 0
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Append a task to this pet's list, tagging it with the pet's name."""
        task.pet_name = self.name
        self.tasks.append(task)

    def edit_task(self, task: Task) -> None:
        """Replace an existing task (matched by id) with an updated version.

        Raises ValueError if no task with that id belongs to this pet.
        """
        for index, existing in enumerate(self.tasks):
            if existing.id == task.id:
                task.pet_name = self.name
                self.tasks[index] = task
                return
        raise ValueError(f"No task with id {task.id!r} on pet {self.name!r}")


@dataclass
class Owner:
    """A pet owner who manages one or more pets."""

    name: str
    email: str = ""
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Register a pet under this owner."""
        self.pets.append(pet)

    def all_tasks(self) -> list[Task]:
        """Return every task across all of this owner's pets, as a flat list."""
        return [task for pet in self.pets for task in pet.tasks]

    def edit_task(self, pet: Pet, task: Task) -> None:
        """Edit a task on one of this owner's pets. Delegates to Pet.edit_task."""
        pet.edit_task(task)


@dataclass
class Scheduler:
    """Builds a daily plan from a set of tasks under a time budget."""

    available_minutes: int = 240  # total time the owner has today
    day_start: time = time(8, 0)  # when the plan begins

    def sort_by_priority(self, tasks: list[Task]) -> list[Task]:
        """Return a new list sorted highest-priority first.

        Ties break by earlier due_date, then shorter duration, so the order
        is deterministic (important for stable tests).
        """
        return sorted(
            tasks,
            key=lambda t: (
                -t.priority.value,        # HIGH(3) first
                t.due_date or date.max,   # earlier deadlines first; None sinks to the end
                t.duration,               # shorter tasks first
            ),
        )

    def filter_by_time(self, tasks: list[Task]) -> list[Task]:
        """Keep tasks (in the given order) that fit the time budget.

        Greedy: walk the list and include each task whose duration fits in the
        remaining minutes; skip the ones that don't. A later, shorter task can
        still fit after an earlier, longer one was skipped.
        """
        remaining = self.available_minutes
        kept: list[Task] = []
        for task in tasks:
            if task.duration <= remaining:
                kept.append(task)
                remaining -= task.duration
        return kept

    def generate_plan(self, tasks: list[Task]) -> list[PlanEntry]:
        """Return a time-ordered daily plan.

        Tasks are prioritized, trimmed to the time budget, then assigned
        back-to-back start times beginning at day_start.
        """
        prioritized = self.sort_by_priority(tasks)
        packed = self.filter_by_time(prioritized)

        plan: list[PlanEntry] = []
        clock = datetime.combine(date.min, self.day_start)
        for task in packed:
            plan.append(PlanEntry(task=task, start_time=clock.time()))
            clock += timedelta(minutes=task.duration)
        return plan

    def explain_plan(self, plan: list[PlanEntry]) -> str:
        """Render the plan as an aligned, terminal-friendly table."""
        if not plan:
            return "No tasks scheduled — nothing fit the available time."

        # Column widths sized to the longest value in each column.
        title_w = max(len(e.task.title) for e in plan)
        pet_w = max(len(e.task.pet_name) for e in plan)
        used = sum(e.task.duration for e in plan)
        free = self.available_minutes - used

        rows = []
        for entry in plan:
            task = entry.task
            end = (datetime.combine(date.min, entry.start_time)
                   + timedelta(minutes=task.duration)).time()
            rows.append(
                f"  {entry.start_time:%H:%M}-{end:%H:%M}   "
                f"{task.title:<{title_w}}   "
                f"{task.pet_name:<{pet_w}}   "
                f"{task.duration:>3}m  {task.priority.name}"
            )

        width = max(len(r) for r in rows)
        divider = "  " + "-" * (width - 2)
        footer = (
            f"  {len(plan)} task(s) · {used}/{self.available_minutes} min used "
            f"· {free} min free"
        )
        return "\n".join(["  Daily Plan", divider, *rows, divider, footer])
