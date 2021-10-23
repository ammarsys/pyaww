"""
PyAwws test file. To properly test the module, use a "fresh account". This means:

- one pre-started console
- no webapps
- no scheduled & always_on tasks
- available "glastonbury" system image
"""

# Standard library imports

from typing import Iterator
from types import GeneratorType

# Related third party imports

import pytest

# Local application/library specific imports

from pyaww.user import User, SchedTask, AlwaysOnTask, WebApp
from pyaww.errors import InvalidInfo


def test_bad_client_token() -> None:
    with pytest.raises(InvalidInfo):
        User(username="bad username", auth="bad info")


def test_get_cpu_info(client) -> None:
    assert isinstance(client.get_cpu_info(), dict)


def test_get_consoles(client) -> None:
    assert isinstance(client.consoles(), dict)


def test_get_students(client: User) -> None:
    assert isinstance(client.students(), dict)


def test_remove_student(client: User, student_name: str) -> None:
    assert client.remove_student(student_name) is None


def test_get_tasks(client: User) -> None:
    assert isinstance(client.tasks(), dict)


def test_get_sched_task_by_id(client: User, scheduled_task: SchedTask) -> None:
    assert client.get_sched_task_by_id(scheduled_task.id) == scheduled_task


def test_get_python_versions(client: User) -> None:
    assert isinstance(client.python_versions(), list)


def test_set_python_version(client: User) -> None:
    assert client.set_python_version(3.8, "python3") is None


def test_get_system_image(client: User) -> None:
    assert isinstance(client.get_system_image(), dict)


def test_set_system_image(client: User) -> None:
    assert client.set_system_image("glastonbury") is None


def test_listdir(contents_of_a_path: Iterator[str]) -> None:
    assert isinstance(contents_of_a_path, GeneratorType)


def test_get_always_on_task_by_id(client: User, always_on_task: AlwaysOnTask) -> None:
    assert client.get_always_on_task_by_id(always_on_task.id) == always_on_task


def test_get_webapps(client: User) -> None:
    assert isinstance(client.webapps(), list)


def test_get_webapp_by_domain(client: User, webapp: WebApp) -> None:
    assert client.get_webapp_by_domain_name(webapp.domain_name) == webapp
