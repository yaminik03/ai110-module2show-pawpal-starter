"""Simple PawPal+ system class skeletons.

Contains beginner-friendly class definitions for Owner, Pet, Task, and Scheduler.
This module provides attributes and method stubs only (no implementations).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Tuple


@dataclass
class Task:
    """Represents a single pet care task.

    Attributes:
        title: Short title describing the task.
        duration_minutes: Estimated duration in minutes.
        priority: Higher numbers mean higher priority.
        is_completed: Whether the task is completed.
    """

    title: str
    duration_minutes: int
    priority: int = 0
    is_completed: bool = False

    def mark_complete(self) -> None:
        """Mark the task as completed."""
        self.is_completed = True

    def summary(self) -> str:
        """Return a short textual summary of the task."""
        status = "Done" if self.is_completed else "Pending"
        return f"[{status}] {self.title} ({self.duration_minutes} min, priority {self.priority})"


@dataclass
class Pet:
    """Represents a pet and its associated tasks.

    Attributes:
        name: Pet's name.
        species: Species (e.g., 'dog', 'cat').
        age: Optional age in years.
        tasks: List of Task objects for this pet.
    """

    name: str
    species: str = "Unknown"
    age: Optional[int] = None
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a Task to this pet."""
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a Task from this pet (no-op if not found)."""
        if task in self.tasks:
            self.tasks.remove(task)

    def get_tasks(self) -> List[Task]:
        """Return the list of tasks for this pet."""
        return self.tasks


class Owner:
    """Represents an owner who can have multiple pets.

    Attributes:
        name: Owner's name.
        contact_info: Contact information string.
        pets: List of Pet objects owned by this owner.
    """

    def __init__(self, name: str, contact_info: str = "") -> None:
        self.name: str = name
        self.contact_info: str = contact_info
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a Pet to the owner."""
        self.pets.append(pet)

    def remove_pet(self, pet: Pet) -> None:
        """Remove a Pet from the owner (no-op if not found)."""
        if pet in self.pets:
            self.pets.remove(pet)

    def get_pets(self) -> List[Pet]:
        """Return the owner's pets."""
        return self.pets

    def get_all_tasks(self) -> List[Task]:
        """Collect and return all tasks across the owner's pets."""
        return [task for pet in self.pets for task in pet.tasks]


class Scheduler:
    """Generates a daily plan from available tasks.

    The scheduler reads tasks (from an Owner or list of Pets) and produces an
    ordered plan that fits within available time.
    """

    def generate_daily_plan(self, owner: Owner, available_minutes: int) -> List[Tuple[Pet, Task]]:
        """Generate a daily plan for an Owner given available minutes.

        Collects all incomplete tasks, sorts by priority (highest first),
        and picks tasks that fit within available_minutes.
        Returns a list of (Pet, Task) tuples in scheduled order.
        """
        # Build (pet, task) pairs for every incomplete task
        candidates = [
            (pet, task)
            for pet in owner.get_pets()
            for task in pet.get_tasks()
            if not task.is_completed
        ]

        # Sort by priority descending so highest-priority tasks are picked first
        candidates.sort(key=lambda pair: pair[1].priority, reverse=True)

        plan: List[Tuple[Pet, Task]] = []
        time_used = 0

        for pet, task in candidates:
            if time_used + task.duration_minutes <= available_minutes:
                plan.append((pet, task))
                time_used += task.duration_minutes

        return plan

    def schedule_tasks(self, tasks: List[Task], available_minutes: int) -> List[Task]:
        """Schedule a list of tasks into the available minutes.

        Sorts by priority (highest first) and returns the ordered subset
        of tasks whose total duration fits within available_minutes.
        """
        sorted_tasks = sorted(tasks, key=lambda t: t.priority, reverse=True)

        scheduled: List[Task] = []
        time_used = 0

        for task in sorted_tasks:
            if time_used + task.duration_minutes <= available_minutes:
                scheduled.append(task)
                time_used += task.duration_minutes

        return scheduled