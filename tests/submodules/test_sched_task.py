# Related third party imports

import pytest

# Local application/library specific imports

from pyaww import SchedTask, User


@pytest.mark.asyncio
async def test_update(scheduled_task: SchedTask) -> None:
    await scheduled_task.update(description="A")
    await scheduled_task.update(description="B")
    assert scheduled_task.description == "B"


@pytest.mark.asyncio
async def test_get_sched_task_by_id(client: User, scheduled_task: SchedTask) -> None:
    assert await client.get_sched_task_by_id(scheduled_task.id) == scheduled_task


@pytest.mark.asyncio
async def test_delete(scheduled_task: SchedTask) -> None:
    assert await scheduled_task.delete() is None
