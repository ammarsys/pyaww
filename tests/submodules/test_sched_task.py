# Local application/library specific imports

from pyaww.user import SchedTask


def test_update(scheduled_task: SchedTask) -> None:
    scheduled_task.update(description="A")
    scheduled_task.update(description="B")
    assert scheduled_task.description == "B"


def test_delete(scheduled_task: SchedTask) -> None:
    assert scheduled_task.delete() is None
