# Standard library imports

from typing import TYPE_CHECKING

# Related third party imports

import pytest

# Local application/library specific imports

if TYPE_CHECKING:
    from pyaww import AlwaysOnTask, User


@pytest.mark.asyncio
async def test_restart(always_on_task: "AlwaysOnTask") -> None:
    assert await always_on_task.restart() is None


@pytest.mark.asyncio
async def test_get_always_on_task_by_id(
    client: "User", always_on_task: "AlwaysOnTask"
) -> None:
    assert await client.get_always_on_task_by_id(always_on_task.id) == always_on_task


@pytest.mark.asyncio
async def test_update(always_on_task: "AlwaysOnTask") -> None:
    await always_on_task.update(description="A")
    await always_on_task.update(description="B")
    assert always_on_task.description == "B"
