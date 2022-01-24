# Standard library imports

from typing import TYPE_CHECKING

# Related third party imports

import pytest

# Local application/library specific imports

if TYPE_CHECKING:
    from pyaww import Console, User


@pytest.mark.asyncio
async def test_send_input(
    started_console: "Console",
) -> None:  # this method also tests pyaww.Console.outputs()
    assert isinstance(await started_console.send_input("echo hello!"), str)


@pytest.mark.asyncio
async def test_delete(
    client: "User", unstarted_console: "Console"
) -> None:  # cleanup + test
    await client.cache.set("console", object_=unstarted_console)

    assert await unstarted_console.delete() is None

    assert await client.cache.get("console", unstarted_console.id) is None
