# Standard library imports

from typing import TYPE_CHECKING

# Related third party imports

import pytest

# Local application/library specific imports

if TYPE_CHECKING:
    from pyaww import SchedTask, User


@pytest.mark.asyncio
async def test_update(client: "User", scheduled_task: "SchedTask") -> None:
    await scheduled_task.update(description="A")
    await scheduled_task.update(description="B")
    assert scheduled_task.description == "B"

    cached = await client.cache.get("sched_task", scheduled_task.id)
    assert scheduled_task.description == cached.description  # type: ignore


@pytest.mark.asyncio
async def test_delete(client: "User", scheduled_task: "SchedTask") -> None:
    await client.cache.set("sched_task", object_=scheduled_task)

    assert await scheduled_task.delete() is None

    assert await client.cache.get("sched_task", scheduled_task.id) is None
