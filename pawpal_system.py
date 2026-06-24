"""PawPal+ domain model.

Class skeletons generated from diagrams/uml.mmd. No scheduling logic yet —
methods raise NotImplementedError so tests can drive the implementation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from enum import Enum


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


@dataclass
class Pet:
    """A pet and its list of care tasks."""

    name: str
    age: int = 0
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        raise NotImplementedError

    def edit_task(self, task: Task) -> None:
        raise NotImplementedError


@dataclass
class Owner:
    """A pet owner who manages one or more pets."""

    name: str
    email: str = ""
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        raise NotImplementedError

    def edit_task(self, pet: Pet, task: Task) -> None:
        raise NotImplementedError


@dataclass
class Scheduler:
    """Builds a daily plan from a set of tasks under a time budget."""

    available_minutes: int = 0

    def generate_plan(self, tasks: list[Task]) -> list[Task]:
        """Return the ordered list of tasks that fit the time budget."""
        raise NotImplementedError

    def sort_by_priority(self, tasks: list[Task]) -> list[Task]:
        """Return tasks sorted from highest to lowest priority."""
        raise NotImplementedError

    def filter_by_time(self, tasks: list[Task]) -> list[Task]:
        """Drop tasks that exceed the remaining available time."""
        raise NotImplementedError

    def explain_plan(self, plan: list[Task]) -> str:
        """Return a human-readable explanation of why this plan was chosen."""
        raise NotImplementedError
