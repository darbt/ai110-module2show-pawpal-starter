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

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

Before Formatting : 
    ```
    Scheduled 2 task(s) using 40 of 60 available minutes, ordered by priority (highest first):
  08:00 — Feeding (10 min) [priority: high]
  08:10 — Walk (30 min) [priority: high]
    ```

After Formatting: 
    ```
     Daily Plan
  -------------------------------------
  08:00-08:10   Feeding       10m  HIGH
  08:10-08:40   Walk          30m  HIGH
  -------------------------------------
  2 task(s) · 40/60 min used · 20 min free
    ```

```
# e.g.:
# Daily plan for Biscuit (Golden Retriever):
#   08:00 — Morning walk (30 min) [priority: high]
#   09:00 — Feeding (10 min) [priority: high]
#   ...
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
python -m pytest

# Run with coverage:
pytest --cov
```

Recurrence:	one-off → None; fresh id + completed=False on the copy while source stays completed; due-date advances by recurrence_days incl. month rollover (Jul 30 → Aug 2); None due-date survives; complete_task appends exactly one tagged instance; one-offs add nothing (no cascade)

Sorting: 	HIGH-first ordering; the full tie-break chain (due_date → duration); None due-date sinks to the end via date.max; shortest-first; pet A–Z then priority; inputs never mutated; empty & single-item

Greedy packing:	the key case — skip a too-long task but keep a later shorter one; exact-fit kept (<=); zero budget keeps only zero-duration

Conflicts:	back-to-back (touching) is NOT a conflict; different pets never conflict; overlap returns the pair in plan order; 3-way same-pet → all 3 pairs

generate_plan:	completed tasks dropped; start times chain back-to-back; empty plan → the exact "nothing fit" string

explain_plan:	emits UserWarning and appends double-booked lines on conflict (pytest.warns)

# Paste your pytest output here
```
============================================================================================================== test session starts ===============================================================================================================
platform win32 -- Python 3.13.14, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\trida\CodePath Assignments\ai110-module2show-pawpal-starter
collected 26 items                                                                                                                                                                                                                                

tests\test_pawpal.py ..........................                                                                                                                                                                                             [100%]

=============================================================================================================== 26 passed in 0.03s ===============================================================================================================

Confidence Level

I would give my confidence level a 4. Its not a perfect score because we have to leave 1 point for anything we could've potentially missed. 

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Sorting behavior  | sort_by_time, sort_by_Pet| by priority and pet name  |
| Filtering |filter_by_completion |skip tasks that are already completed|
| Conflict handling | find_conflicts, has_conflicts, conflict_warnings |checks for overlapping time slots for the same pet and issues a warning  |


## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
