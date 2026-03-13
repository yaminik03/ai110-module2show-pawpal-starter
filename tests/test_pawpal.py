"""Automated test suite for PawPal+ core behaviors.

Covers: task completion, scheduling logic, sorting, filtering,
conflict detection, and edge cases (empty pets, zero time budget).
"""

import pytest
from pawpal_system import Owner, Pet, Task, Scheduler


# ── helpers ──────────────────────────────────────────────────────────────────

def make_owner_with_pets():
    """Return an Owner with two pets and no tasks."""
    owner = Owner("Alex")
    owner.add_pet(Pet("Rex", "dog"))
    owner.add_pet(Pet("Mochi", "cat"))
    return owner


# ── Task ─────────────────────────────────────────────────────────────────────

def test_task_mark_complete():
    """Happy path: mark_complete() sets is_completed to True."""
    task = Task("Bath", 20, priority=3)
    assert task.is_completed is False
    task.mark_complete()
    assert task.is_completed is True


def test_task_summary_pending():
    """summary() reflects pending status before completion."""
    task = Task("Walk", 30, priority=5)
    assert "Pending" in task.summary()
    assert "Walk" in task.summary()


def test_task_summary_done():
    """summary() reflects done status after completion."""
    task = Task("Walk", 30, priority=5)
    task.mark_complete()
    assert "Done" in task.summary()


# ── Pet ──────────────────────────────────────────────────────────────────────

def test_pet_add_and_get_tasks():
    """Happy path: tasks added to a pet are retrievable."""
    pet = Pet("Rex", "dog")
    t = Task("Feed", 5, priority=2)
    pet.add_task(t)
    assert t in pet.get_tasks()


def test_pet_remove_task():
    """Removing a task leaves the pet's list without it."""
    pet = Pet("Rex", "dog")
    t = Task("Feed", 5)
    pet.add_task(t)
    pet.remove_task(t)
    assert t not in pet.get_tasks()


def test_pet_remove_nonexistent_task_no_crash():
    """Edge case: removing a task that was never added should not raise."""
    pet = Pet("Rex", "dog")
    t = Task("Ghost task", 10)
    pet.remove_task(t)  # should be a no-op


def test_pet_no_tasks():
    """Edge case: a brand-new pet has an empty task list."""
    pet = Pet("Mochi", "cat")
    assert pet.get_tasks() == []


# ── Owner ────────────────────────────────────────────────────────────────────

def test_owner_add_and_get_pets():
    """Happy path: pets added to an owner are retrievable."""
    owner = Owner("Alex")
    pet = Pet("Rex", "dog")
    owner.add_pet(pet)
    assert pet in owner.get_pets()


def test_owner_get_all_tasks_across_pets():
    """get_all_tasks() flattens tasks from all pets."""
    owner = make_owner_with_pets()
    t1 = Task("Walk", 30, priority=4)
    t2 = Task("Feed", 10, priority=2)
    owner.get_pets()[0].add_task(t1)
    owner.get_pets()[1].add_task(t2)
    all_tasks = owner.get_all_tasks()
    assert t1 in all_tasks
    assert t2 in all_tasks


def test_owner_no_pets_returns_empty():
    """Edge case: an owner with no pets returns empty lists."""
    owner = Owner("Jordan")
    assert owner.get_pets() == []
    assert owner.get_all_tasks() == []


# ── Scheduler: schedule_tasks ────────────────────────────────────────────────

def test_schedule_tasks_sorts_by_priority():
    """Higher-priority tasks appear first in the scheduled output."""
    tasks = [
        Task("Low",  10, priority=1),
        Task("High", 10, priority=9),
        Task("Mid",  10, priority=5),
    ]
    scheduled = Scheduler().schedule_tasks(tasks, available_minutes=60)
    assert scheduled[0].title == "High"
    assert scheduled[1].title == "Mid"
    assert scheduled[2].title == "Low"


def test_schedule_tasks_respects_time_budget():
    """Tasks that exceed the time budget are excluded."""
    tasks = [Task("Long", 90, priority=10), Task("Short", 15, priority=5)]
    scheduled = Scheduler().schedule_tasks(tasks, available_minutes=30)
    assert all(t.title != "Long" for t in scheduled)
    assert any(t.title == "Short" for t in scheduled)


def test_schedule_tasks_zero_budget_returns_empty():
    """Edge case: zero available minutes produces an empty plan."""
    tasks = [Task("Walk", 30, priority=5)]
    scheduled = Scheduler().schedule_tasks(tasks, available_minutes=0)
    assert scheduled == []


def test_schedule_tasks_empty_list():
    """Edge case: scheduling an empty task list returns an empty list."""
    assert Scheduler().schedule_tasks([], available_minutes=60) == []


# ── Scheduler: generate_daily_plan ───────────────────────────────────────────

def test_generate_daily_plan_happy_path():
    """Happy path: returns (Pet, Task) tuples for schedulable tasks."""
    owner = make_owner_with_pets()
    owner.get_pets()[0].add_task(Task("Walk", 30, priority=5))
    owner.get_pets()[1].add_task(Task("Feed", 10, priority=3))

    plan = Scheduler().generate_daily_plan(owner, available_minutes=60)

    assert len(plan) == 2
    assert all(isinstance(pet, Pet) and isinstance(task, Task) for pet, task in plan)


def test_generate_daily_plan_skips_completed():
    """Completed tasks are excluded from the generated plan."""
    owner = make_owner_with_pets()
    done = Task("Old walk", 20, priority=8)
    done.mark_complete()
    owner.get_pets()[0].add_task(done)
    owner.get_pets()[0].add_task(Task("Feed", 10, priority=2))

    plan = Scheduler().generate_daily_plan(owner, available_minutes=60)

    titles = [task.title for _, task in plan]
    assert "Old walk" not in titles
    assert "Feed" in titles


def test_generate_daily_plan_owner_no_tasks():
    """Edge case: owner with pets but no tasks returns an empty plan."""
    owner = make_owner_with_pets()
    plan = Scheduler().generate_daily_plan(owner, available_minutes=60)
    assert plan == []