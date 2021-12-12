"""
PyAwws test file. To properly test the module, use a "fresh account". Some guidlines:

- one pre-started console
- no webapps
- no scheduled & always_on tasks
- glastonbury image must be available

Basically, create an account, start a console, fill out the env file.
"""

# Standard library imports

import asyncio
from typing import AsyncIterator

# Related third party imports

import pytest

# Local library/libraary specific imports

from pyaww import (
    User,
    File,
    Console,
    SchedTask,
    WebApp,
    StaticFile,
    StaticHeader,
    PythonAnywhereError,
)
from dotenv import dotenv_values

values = dotenv_values("tests/assets/.env")

USERNAME = values["USERNAME"]
AUTH = values["AUTH"]
STARTED_CONSOLE = values["STARTED_CONSOLE"]

TEST_PATH_TO_LISTDIR = f"/home/{USERNAME}/"
TEST_PATH_FOR_NEW_FILE = f"/home/{USERNAME}/pyaww_test_data.txt"

TEST_RELATIVE_PATH_TO_FILE = r"tests/assets/data.txt"
TEST_STUDENT_TO_REMOVE = "ANYTHING_HERE"


@pytest.fixture(scope="session")
def event_loop():
    # It's safe to ignore these warnings.

    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def webapp(client: User) -> WebApp:
    """Construct a webapp"""
    return await client.create_webapp(
        domain_name=f"{USERNAME}.pythonanywhere.com", python_version="python39"
    )


@pytest.fixture(scope="session")
def client() -> User:
    """Construct the User (client) class"""
    return User(username=USERNAME, auth=AUTH)


@pytest.fixture
async def unstarted_console(client) -> Console:
    """Create an unstarted console, this means you cannot send input to it"""
    return await client.create_console(executable="bash")


@pytest.fixture
async def started_console(client) -> Console:
    """Get a started console"""
    return await client.get_console_by_id(id_=int(STARTED_CONSOLE))


@pytest.fixture
async def contents_of_a_path(client) -> AsyncIterator[str]:
    """Recursively go through paths subdirs, aka listdir"""
    return client.listdir(TEST_PATH_TO_LISTDIR, recursive=True)


@pytest.fixture
async def file(client: User) -> File:
    with open(TEST_RELATIVE_PATH_TO_FILE, "r") as file:
        return await client.create_file(TEST_PATH_FOR_NEW_FILE, file)


@pytest.fixture
async def student_name() -> str:
    """Return a student to remove"""
    return TEST_STUDENT_TO_REMOVE


@pytest.fixture(scope="session")
async def scheduled_task(client: User) -> SchedTask:
    """Create a scheduled task"""
    return await client.create_sched_task(
        command="echo hello world", hour="5", minute="5"
    )


@pytest.fixture
async def always_on_task(client: User):
    """Create an always_on task"""
    try:
        return await client.create_always_on_task(command="cd")
    except PythonAnywhereError:
        pytest.skip(
            "Max always_on tasks or a free account, skipping always_on task tests."
        )


@pytest.fixture
async def static_file(webapp: WebApp) -> StaticFile:
    """Create a static file. Webapp restart required."""
    static_file = await webapp.create_static_file(
        file_path=f"/home/{USERNAME}/README.txt", url="PYAWW URL FIXTURE"
    )
    await webapp.restart()
    return static_file


@pytest.fixture(scope="session")
async def static_header(webapp: WebApp) -> StaticHeader:
    """Create a static file. Webapp restart required."""
    static_header = await webapp.create_static_header(
        value={"PYAWW KEY": "PYAWW VALUE"},
        url="PYAWW URL FIXTURE",
        name="PYAWW SAMPLE NAME",
    )
    await webapp.restart()
    return static_header
