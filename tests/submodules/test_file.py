# Standard library imports

from typing import TYPE_CHECKING

# Related third party imports

import pytest

# Local application/library specific imports

if TYPE_CHECKING:
    from pyaww import File


@pytest.mark.asyncio
async def test_update(file: "File") -> None:  # This also tests read.
    with open("tests/assets/data.txt") as local_file:

        local_file_no_close = local_file
        local_file_no_close.close = lambda: None  # type: ignore

        await file.update(local_file_no_close)
        local_file_no_close.seek(0)

        assert (
            local_file_no_close.read() == await file.read()
        ), "contents of local file failed to match one on the server"


@pytest.mark.asyncio
async def test_share(file: "File") -> None:
    assert isinstance(await file.share(), str)


@pytest.mark.asyncio
async def test_unshare(file: "File") -> None:
    assert await file.unshare() is None


@pytest.mark.asyncio
async def test_sharing_status(file: "File") -> None:
    assert await file.is_shared() is False


@pytest.mark.asyncio
async def test_delete(file: "File") -> None:
    assert await file.delete() is None
