from pawpal_system import Pet, Task


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
