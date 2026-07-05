from datetime import date, time

import pytest

from pawpal_system import (
    Pet,
    PlanEntry,
    Priority,
    Scheduler,
    Task,
)


# ---------------------------------------------------------------------------
# Existing sanity checks
# ---------------------------------------------------------------------------
def test_mark_complete_sets_task_completed():
    task = Task(title="Walk", description="Evening walk", duration=30)

    # A new task should start out incomplete.
    assert task.completed is False

    task.mark_complete()

    assert task.completed is True


def test_add_task_increases_pet_task_count():
    pet = Pet(name="Rocky", age=2)
    starting_count = len(pet.tasks)

    pet.add_task(Task(title="Feeding", duration=10))

    assert len(pet.tasks) == starting_count + 1


# ---------------------------------------------------------------------------
# 1. Recurring tasks: next_occurrence / complete_task
# ---------------------------------------------------------------------------
def test_next_occurrence_of_one_off_is_none():
    task = Task(title="Vet visit", recurrence_days=None)

    assert task.next_occurrence() is None


def test_next_occurrence_gets_fresh_identity_and_resets_completion():
    task = Task(title="Walk", recurrence_days=1, completed=True)
    task.mark_complete()

    nxt = task.next_occurrence()

    assert nxt is not None
    assert nxt.id != task.id          # brand-new instance, not the same object
    assert nxt.completed is False     # the copy starts fresh
    assert task.completed is True     # the source is untouched


def test_next_occurrence_advances_due_date_by_recurrence_days():
    task = Task(title="Meds", due_date=date(2026, 7, 2), recurrence_days=3)

    nxt = task.next_occurrence()

    assert nxt.due_date == date(2026, 7, 5)


def test_next_occurrence_advances_across_month_boundary():
    task = Task(title="Meds", due_date=date(2026, 7, 30), recurrence_days=3)

    nxt = task.next_occurrence()

    assert nxt.due_date == date(2026, 8, 2)


def test_next_occurrence_keeps_none_due_date():
    # A recurring task with no due date must not crash on the timedelta add.
    task = Task(title="Water", due_date=None, recurrence_days=2)

    nxt = task.next_occurrence()

    assert nxt is not None
    assert nxt.due_date is None


def test_complete_task_queues_next_occurrence_on_pet():
    pet = Pet(name="Rocky", age=2)
    task = Task(title="Walk", due_date=date(2026, 7, 2), recurrence_days=1)
    pet.add_task(task)

    upcoming = pet.complete_task(task)

    assert task.completed is True
    assert upcoming is not None
    assert upcoming in pet.tasks              # appended to the list
    assert pet.tasks[-1] is upcoming
    assert upcoming.pet_name == "Rocky"       # tagged with the pet's name
    assert len(pet.tasks) == 2                # exactly one new instance


def test_complete_task_on_one_off_adds_nothing():
    pet = Pet(name="Rocky", age=2)
    task = Task(title="Vet visit", recurrence_days=None)
    pet.add_task(task)

    upcoming = pet.complete_task(task)

    assert upcoming is None
    assert len(pet.tasks) == 1                # no cascade of new tasks


# ---------------------------------------------------------------------------
# 2. Sorting: tie-breakers, None-due-date sinking, non-mutation
# ---------------------------------------------------------------------------
def test_sort_by_priority_orders_high_first():
    sched = Scheduler()
    low = Task(title="low", priority=Priority.LOW)
    high = Task(title="high", priority=Priority.HIGH)
    med = Task(title="med", priority=Priority.MEDIUM)

    ordered = sched.sort_by_priority([low, high, med])

    assert [t.title for t in ordered] == ["high", "med", "low"]


def test_sort_by_priority_tie_breaks_by_due_date_then_duration():
    sched = Scheduler()
    # All HIGH; differ only on the secondary/tertiary keys.
    later = Task(title="later", priority=Priority.HIGH, due_date=date(2026, 7, 5), duration=10)
    earlier_long = Task(title="earlier_long", priority=Priority.HIGH, due_date=date(2026, 7, 2), duration=30)
    earlier_short = Task(title="earlier_short", priority=Priority.HIGH, due_date=date(2026, 7, 2), duration=5)

    ordered = sched.sort_by_priority([later, earlier_long, earlier_short])

    # Same due date breaks by shorter duration; both beat the later due date.
    assert [t.title for t in ordered] == ["earlier_short", "earlier_long", "later"]


def test_sort_by_priority_sinks_none_due_date_to_end():
    sched = Scheduler()
    dated = Task(title="dated", priority=Priority.HIGH, due_date=date(2026, 7, 2))
    undated = Task(title="undated", priority=Priority.HIGH, due_date=None)

    ordered = sched.sort_by_priority([undated, dated])

    assert [t.title for t in ordered] == ["dated", "undated"]


def test_sort_by_time_orders_shortest_first():
    sched = Scheduler()
    long = Task(title="long", duration=30)
    short = Task(title="short", duration=5)
    mid = Task(title="mid", duration=15)

    ordered = sched.sort_by_time([long, short, mid])

    assert [t.title for t in ordered] == ["short", "mid", "long"]


def test_sort_by_pet_groups_alphabetically_then_priority():
    sched = Scheduler()
    zeus_low = Task(title="zeus_low", pet_name="Zeus", priority=Priority.LOW)
    apple_low = Task(title="apple_low", pet_name="Apple", priority=Priority.LOW)
    apple_high = Task(title="apple_high", pet_name="Apple", priority=Priority.HIGH)

    ordered = sched.sort_by_pet([zeus_low, apple_low, apple_high])

    # Apple's tasks come first (A-Z), HIGH before LOW within Apple.
    assert [t.title for t in ordered] == ["apple_high", "apple_low", "zeus_low"]


def test_sorts_do_not_mutate_input_list():
    sched = Scheduler()
    a = Task(title="a", priority=Priority.LOW, duration=30, pet_name="B")
    b = Task(title="b", priority=Priority.HIGH, duration=5, pet_name="A")
    original = [a, b]

    sched.sort_by_priority(original)
    sched.sort_by_time(original)
    sched.sort_by_pet(original)

    assert original == [a, b]   # untouched


def test_sorts_handle_empty_and_single():
    sched = Scheduler()
    solo = [Task(title="solo")]

    assert sched.sort_by_priority([]) == []
    assert sched.sort_by_time([]) == []
    assert sched.sort_by_pet([]) == []
    assert [t.title for t in sched.sort_by_priority(solo)] == ["solo"]


# ---------------------------------------------------------------------------
# 3. Time-budget packing: greedy filter_by_time
# ---------------------------------------------------------------------------
def test_filter_by_time_skips_too_long_but_keeps_later_shorter():
    sched = Scheduler(available_minutes=20)
    long = Task(title="long", duration=30)     # doesn't fit, skipped
    short = Task(title="short", duration=15)    # fits after the skip

    kept = sched.filter_by_time([long, short])

    assert [t.title for t in kept] == ["short"]


def test_filter_by_time_keeps_exact_fit():
    sched = Scheduler(available_minutes=30)
    exact = Task(title="exact", duration=30)

    kept = sched.filter_by_time([exact])

    assert [t.title for t in kept] == ["exact"]


def test_filter_by_time_zero_budget_keeps_only_zero_duration():
    sched = Scheduler(available_minutes=0)
    freebie = Task(title="freebie", duration=0)
    costly = Task(title="costly", duration=5)

    kept = sched.filter_by_time([costly, freebie])

    assert [t.title for t in kept] == ["freebie"]


# ---------------------------------------------------------------------------
# 4. Conflict detection: interval boundaries
# ---------------------------------------------------------------------------
def _entry(title, pet, start, duration):
    return PlanEntry(task=Task(title=title, pet_name=pet, duration=duration), start_time=start)


def test_back_to_back_same_pet_is_not_a_conflict():
    sched = Scheduler()
    plan = [
        _entry("walk", "Rocky", time(8, 0), 30),   # 08:00-08:30
        _entry("feed", "Rocky", time(8, 30), 10),  # 08:30-08:40 (touching)
    ]

    assert sched.find_conflicts(plan) == []
    assert sched.has_conflicts(plan) is False


def test_different_pets_never_conflict_even_at_same_time():
    sched = Scheduler()
    plan = [
        _entry("walk", "Rocky", time(8, 0), 30),
        _entry("meds", "Cookie", time(8, 0), 30),
    ]

    assert sched.find_conflicts(plan) == []


def test_same_pet_overlap_is_a_conflict_in_plan_order():
    sched = Scheduler()
    a = _entry("walk", "Rocky", time(8, 0), 30)    # 08:00-08:30
    b = _entry("feed", "Rocky", time(8, 15), 10)   # 08:15-08:25 overlaps
    conflicts = sched.find_conflicts([a, b])

    assert len(conflicts) == 1
    assert conflicts[0] == (a, b)   # order follows the plan
    assert sched.has_conflicts([a, b]) is True


def test_three_way_same_pet_overlap_yields_all_pairs():
    sched = Scheduler()
    a = _entry("a", "Rocky", time(8, 0), 30)
    b = _entry("b", "Rocky", time(8, 0), 30)
    c = _entry("c", "Rocky", time(8, 0), 30)

    conflicts = sched.find_conflicts([a, b, c])

    assert len(conflicts) == 3   # (a,b), (a,c), (b,c)


# ---------------------------------------------------------------------------
# 5. generate_plan integration
# ---------------------------------------------------------------------------
def test_generate_plan_drops_completed_and_chains_start_times():
    sched = Scheduler(available_minutes=240, day_start=time(8, 0))
    done = Task(title="done", duration=30, priority=Priority.HIGH, completed=True)
    first = Task(title="first", duration=30, priority=Priority.HIGH)
    second = Task(title="second", duration=10, priority=Priority.MEDIUM)

    plan = sched.generate_plan([done, first, second])

    assert [e.task.title for e in plan] == ["first", "second"]   # completed dropped
    assert plan[0].start_time == time(8, 0)
    assert plan[1].start_time == time(8, 30)   # back-to-back after 30m


def test_generate_plan_empty_when_nothing_fits():
    sched = Scheduler(available_minutes=5)
    plan = sched.generate_plan([Task(title="big", duration=60)])

    assert plan == []
    assert sched.explain_plan(plan) == (
        "No tasks scheduled — nothing fit the available time."
    )


# ---------------------------------------------------------------------------
# 6. explain_plan warnings on conflict
# ---------------------------------------------------------------------------
def test_explain_plan_warns_and_appends_lines_on_conflict():
    sched = Scheduler()
    plan = [
        _entry("walk", "Rocky", time(8, 0), 30),
        _entry("feed", "Rocky", time(8, 0), 10),   # same pet + time
    ]

    with pytest.warns(UserWarning, match="conflict"):
        rendered = sched.explain_plan(plan)

    assert "double-booked" in rendered
