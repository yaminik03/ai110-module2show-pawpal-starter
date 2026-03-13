# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

# Testing PawPal+
Run the tests with: python -m pytest

The suite covers three categories. Core behavior tests confirm that mark_complete() flips the right flag, summary() reflects the correct status, and get_all_tasks() flattens tasks across pets. Scheduling logic tests verify that schedule_tasks() orders by priority, respects the time budget, and handles zero-minute budgets. Edge case tests check that operations on empty pets, empty task lists, and already-completed tasks never crash and return sensible empty results.

Confidence level: (4/5) — all core behaviors and the most likely edge cases are covered. The main gap is integration-level testing (UI + backend together) and duration-overlap conflict detection, which the scheduler does not yet implement.