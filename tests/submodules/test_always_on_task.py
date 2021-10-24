# Local application/library specific imports

from pyaww.user import AlwaysOnTask, User


def test_restart(always_on_task: AlwaysOnTask) -> None:
    assert always_on_task.restart() is None


def test_get_always_on_task_by_id(client: User, always_on_task: AlwaysOnTask) -> None:
    assert client.get_always_on_task_by_id(always_on_task.id) == always_on_task


def test_update(always_on_task: AlwaysOnTask) -> None:
    always_on_task.update(description="A")
    always_on_task.update(description="B")
    assert always_on_task.description == "B"
