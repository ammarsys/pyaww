# Related third party imports

import pytest

# Local application/library specific imports

from pyaww import SchedTask


@pytest.mark.asyncio
async def test_update(scheduled_task: SchedTask) -> None:
    await scheduled_task.update(description="A")
    await scheduled_task.update(description="B")
    assert scheduled_task.description == "B"


@pytest.mark.asyncio
async def test_delete(client, scheduled_task: SchedTask) -> None:
    await client.cache.set("sched_task", object_=scheduled_task)

    assert await scheduled_task.delete() is None

    assert await client.cache.get("sched_task", scheduled_task.id) is None
