# Related third party imports

import pytest

# Local application/library specific imports

from pyaww.user import File
from pyaww.errors import NotFound


def test_share(file: File) -> None:
    assert isinstance(file.share(), str)


def test_unshare(file: File) -> None:
    assert file.unshare() is None


def test_sharing_status(file: File) -> None:
    with pytest.raises(NotFound):
        assert file.is_shared() is False


def test_read(file: File) -> None:
    assert isinstance(file.read().decode(), str)


def test_update(throwaway_file: File) -> None:
    with open("tests/assets/data.txt") as f:
        throwaway_file.update(f)
        f.seek(0)
        assert throwaway_file.read().decode() == f.read()


def test_delete(throwaway_file: File) -> None:
    assert throwaway_file.delete() is None
