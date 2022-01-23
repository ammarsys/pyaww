# Standard library imports

from typing import Iterator, TYPE_CHECKING
from types import AsyncGeneratorType

# Related third party imports

import pytest

# Local application/library specific imports

from pyaww import User, InvalidInfo

if TYPE_CHECKING:
    from pyaww import SchedTask


def test_bad_client_token() -> None:
    with pytest.raises(InvalidInfo):
        User(username="bad username", auth="bad info")


@pytest.mark.asyncio
async def test_get_cpu_info(client) -> None:
    assert isinstance(await client.get_cpu_info(), dict)


@pytest.mark.asyncio
async def test_get_consoles(client) -> None:
    assert isinstance(await client.consoles(), list)
    assert isinstance(await client.shared_consoles(), list)

    assert await client.cache.all("console")


@pytest.mark.asyncio
async def test_get_students(client: User) -> None:
    assert isinstance(await client.students(), dict)


@pytest.mark.asyncio
async def test_remove_student(client: User, student_name: str) -> None:
    assert await client.remove_student(student_name) is None


@pytest.mark.asyncio
async def test_get_tasks(client: User) -> None:
    assert isinstance(await client.scheduled_tasks(), list)
    assert isinstance(await client.always_on_tasks(), list)


@pytest.mark.asyncio
async def test_get_python_versions(client: User) -> None:
    assert isinstance(await client.python_versions(), list)


@pytest.mark.asyncio
async def test_get_sched_task_by_id(client: User, scheduled_task: "SchedTask") -> None:
    assert await client.get_sched_task_by_id(scheduled_task.id) == scheduled_task, "IDs between two instances do not match (__eq__)"


@pytest.mark.asyncio
async def test_set_python_version(client: User) -> None:
    assert await client.set_python_version(3.8, "python3") is None


@pytest.mark.asyncio
async def test_get_system_image(client: User) -> None:
    assert isinstance(await client.get_system_image(), dict)


@pytest.mark.asyncio
async def test_set_system_image(client: User) -> None:
    assert await client.set_system_image("glastonbury") is None


@pytest.mark.asyncio
async def test_listdir(contents_of_a_path: Iterator[str]) -> None:
    assert isinstance(contents_of_a_path, AsyncGeneratorType)


@pytest.mark.asyncio
async def test_get_webapps(client: User) -> None:
    assert isinstance(await client.webapps(), list)
