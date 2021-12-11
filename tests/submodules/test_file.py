# Related third party imports

import pytest

# Local application/library specific imports

from pyaww import File


@pytest.mark.asyncio
async def test_update(file: File) -> None:  # This also tests read.
    with open("tests/assets/data.txt") as f:

        # Prevent aiohttp from closing the file but allow the context manager to call __exit__
        file_no_close = f
        file_no_close.close = lambda: None

        await file.update(file_no_close)
        file = await file.read()

        file_no_close.seek(0)
        assert file == file_no_close.read()


@pytest.mark.asyncio
async def test_share(file: File) -> None:
    assert isinstance(await file.share(), str)


@pytest.mark.asyncio
async def test_unshare(file: File) -> None:
    assert await file.unshare() is None


@pytest.mark.asyncio
async def test_sharing_status(file: File) -> None:
    assert await file.is_shared() is False


@pytest.mark.asyncio
async def test_delete(file: File) -> None:
    assert await file.delete() is None
