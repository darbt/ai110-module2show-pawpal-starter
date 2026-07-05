from datetime import date

from pawpal_system import Task, Owner, Pet, Priority, Scheduler

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
