from datetime import date, time

from pawpal_system import Task, Owner, Pet, PlanEntry, Priority, Scheduler

# Tasks must be defined before they're used in a Pet's task list.
rockyTask1 = Task(
    title="Walk",
    description="Take Rocky on a walk to the park",
    due_date=date(2026, 7, 2),
    duration=30,
    priority=Priority.HIGH,
)
rockyTask2 = Task(
    title="Feeding",
    description="Morning kibble and fresh water",
    due_date=date(2026, 7, 2),
    duration=10,
    priority=Priority.HIGH,
)
cookieTask1 = Task(
    title="Meds",
    description="Give Cookie her allergy medication",
    due_date=date(2026, 7, 2),
    duration=5,
    priority=Priority.MEDIUM,
)
cookieTask2 = Task(
    title="Grooming",
    description="Brush Cookie's coat",
    due_date=date(2026, 7, 3),
    duration=20,
    priority=Priority.LOW,
)

pet1 = Pet(name ="Rocky", 
           age = 2, 
           tasks = [rockyTask1, rockyTask2])
pet2 = Pet(
    name ="Cookie",
     age =  4, 
     tasks = [cookieTask1, cookieTask2])

owner1 = Owner(
    name = "Katie", 
    email = "katieemail@hotmail.com", 
    pets = [pet1, pet2])

scheduler = Scheduler(available_minutes= 60);

plan = scheduler.generate_plan(pet1.tasks)

print(scheduler.explain_plan(plan))


# ---------------------------------------------------------------------------
# Demo: exercise the sorting and filtering methods.
# Add a few tasks out of order (via add_task so pet_name gets set), mark one
# complete, then run each method and print the resulting order.
# ---------------------------------------------------------------------------

# Make sure the constructor-built tasks are tagged with their pet's name too,
# so sort_by_pet has something to group on.
for pet in owner1.pets:
    for task in pet.tasks:
        task.pet_name = pet.name

# Extra tasks added deliberately out of priority / duration / pet order.
pet2.add_task(Task(
    title="Play",
    description="Laser pointer session with Cookie",
    due_date=date(2026, 7, 1),
    duration=15,
    priority=Priority.HIGH,
))
pet1.add_task(Task(
    title="Nail trim",
    description="Clip Rocky's nails",
    due_date=date(2026, 7, 4),
    duration=25,
    priority=Priority.LOW,
))

pet1.add_task(Task(
    title="Bath",
    description="Give Rocky a bat",
    due_date=date(2026, 7, 4),
    duration=25,
    priority=Priority.MEDIUM,
))

# Mark one task complete so the completion filter has something to drop.
rockyTask2.mark_complete()  # "Feeding"


def show(label, tasks):
    """Print a task list compactly: title, pet, duration, priority, done?"""
    print(f"\n{label}")
    for t in tasks:
        done = "x" if t.completed else " "
        print(f"  [{done}] {t.title:<10} {t.pet_name:<7} "
              f"{t.duration:>3}m  {t.priority.name}")


all_tasks = owner1.all_tasks()

show("Original order (out of order):", all_tasks)
show("sort_by_priority (HIGH first):", scheduler.sort_by_priority(all_tasks))
show("sort_by_time (shortest first):", scheduler.sort_by_time(all_tasks))
show("sort_by_pet (grouped A-Z):", scheduler.sort_by_pet(all_tasks))
show("filter_by_completion() -> to-do:", scheduler.filter_by_completion(all_tasks))
show("filter_by_completion(True) -> done:",
     scheduler.filter_by_completion(all_tasks, completed=True))


# ---------------------------------------------------------------------------
# Demo: conflict detection. generate_plan packs tasks back-to-back, so it
# never self-conflicts. To test the warning we hand-build a plan that puts
# two of Rocky's tasks at the SAME start time, then explain it.
# ---------------------------------------------------------------------------

print("\nBuilding a plan with two of Rocky's tasks at 08:00 (a conflict):")
conflicting_plan = [
    PlanEntry(task=rockyTask1, start_time=time(8, 0)),  # Walk, 30m
    PlanEntry(task=cookieTask1, start_time=time(8, 0)),  # different pet: no conflict
    PlanEntry(task=rockyTask2, start_time=time(8, 0)),  # Feeding, same pet + time
]

# explain_plan emits a warnings.warn(...) AND appends the conflict lines,
# without stopping the program.
print(scheduler.explain_plan(conflicting_plan))
print("\n=== program finished normally despite the conflict ===")
