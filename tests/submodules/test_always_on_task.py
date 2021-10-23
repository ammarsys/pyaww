# Local application/library specific imports

from pyaww.user import AlwaysOnTask


def test_restart(always_on_task: AlwaysOnTask) -> None:
    assert always_on_task.restart() is None
