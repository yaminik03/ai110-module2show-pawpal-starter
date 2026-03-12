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
		"""Mark the task as completed (stub)."""
		pass

	def summary(self) -> str:
		"""Return a short textual summary of the task (stub)."""
		pass


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
		"""Add a Task to this pet (stub)."""
		pass

	def remove_task(self, task: Task) -> None:
		"""Remove a Task from this pet (stub)."""
		pass

	def get_tasks(self) -> List[Task]:
		"""Return the list of tasks for this pet (stub)."""
		pass


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
		"""Add a Pet to the owner (stub)."""
		pass

	def remove_pet(self, pet: Pet) -> None:
		"""Remove a Pet from the owner (stub)."""
		pass

	def get_pets(self) -> List[Pet]:
		"""Return the owner's pets (stub)."""
		pass

	def get_all_tasks(self) -> List[Task]:
		"""Collect and return all tasks across the owner's pets (stub)."""
		pass


class Scheduler:
	"""Generates a daily plan from available tasks.

	The scheduler reads tasks (from an Owner or list of Pets) and produces an
	ordered plan that fits within available time. Methods are stubs only.
	"""

	def generate_daily_plan(self, owner: Owner, available_minutes: int) -> List[Tuple[Pet, Task]]:
		"""Generate a daily plan for an Owner given available minutes (stub).

		Returns a list of (Pet, Task) tuples in scheduled order.
		"""
		pass

	def schedule_tasks(self, tasks: List[Task], available_minutes: int) -> List[Task]:
		"""Schedule a list of tasks into the available minutes (stub).

		Returns the ordered list of tasks that fit into available_minutes.
		"""
		pass

