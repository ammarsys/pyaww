# Local application/library specific imports

from pyaww import SchedTask, User


def test_update(scheduled_task: SchedTask) -> None:
    scheduled_task.update(description="A")
    scheduled_task.update(description="B")
    assert scheduled_task.description == "B"


def test_get_sched_task_by_id(client: User, scheduled_task: SchedTask) -> None:
    assert client.get_sched_task_by_id(scheduled_task.id) == scheduled_task


def test_delete(scheduled_task: SchedTask) -> None:
    assert scheduled_task.delete() is None
