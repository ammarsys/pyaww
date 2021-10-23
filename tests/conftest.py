"""
PyAwws test file. To properly test the module, use a "fresh account". Some guidlines:

- one pre-started console
- no webapps
- no scheduled & always_on tasks
- glastonbury image must be available

"""
# Standard library imports

from typing import Iterator

# Related third party imports

import pytest

# Local library/libraary specific imports

from pyaww.user import User, File, Console, SchedTask, AlwaysOnTask, WebApp
from pyaww.errors import PythonAnywhereError


USERNAME = "ammarsysdev"
AUTH = "119b1a7eac245332ba623bbcb5d2a5151af3757a"

TEST_STARTED_CONSOLE = 22004897  # start the console in browser, should be bash
TEST_PATH_TO_LISTDIR = f"/home/{USERNAME}/mysite/mysite"  # preferably something that doesn't have too many subdirs
TEST_PATH_TO_FILE = f"/home/{USERNAME}/mysite/mysite/asgi.py"
TEST_RELATIVE_PATH_TO_FILE = (
    r"tests\assets\data.txt"  # should be full path
)
TEST_PATH_FOR_NEW_FILE = f"/home/{USERNAME}/mysite/mysite/data.txt"
TEST_STUDENT_TO_REMOVE = "someone"


@pytest.fixture
def webapp(client: User) -> WebApp:
    """Construct a webapp"""
    return client.create_webapp(
        domain_name=f"{USERNAME}.pythonanywhere.com", python_version="python39"
    )


@pytest.fixture(scope="session")
def client() -> User:
    """Construct the User (client) class"""
    return User(username=USERNAME, auth=AUTH)


@pytest.fixture
def unstarted_console(client) -> Console:
    """Create an unstarted console, this means you cannot send input to it"""
    return client.create_console(executable="bash")


@pytest.fixture
def started_console(client) -> Console:
    """Get a started console"""
    return client.get_console_by_id(id_=TEST_STARTED_CONSOLE)


@pytest.fixture
def contents_of_a_path(client) -> Iterator[str]:
    """Recursively go through paths subdirs, aka listdir"""
    return client.listdir(TEST_PATH_TO_LISTDIR, recursive=True)


@pytest.fixture
def file(client) -> File:
    """Get a PythonAnywhere file"""
    return client.get_file_by_path(TEST_PATH_TO_FILE)


@pytest.fixture
def throwaway_file(client: User) -> File:
    with open(TEST_RELATIVE_PATH_TO_FILE, "r") as f:
        return client.create_file(TEST_PATH_FOR_NEW_FILE, f)


@pytest.fixture
def student_name() -> str:
    """Return a student to remove"""
    return TEST_STUDENT_TO_REMOVE


@pytest.fixture(scope="session")
def scheduled_task(client: User) -> SchedTask:
    """Create a scheduled task"""
    return client.create_sched_task(command="echo hello world", hour="5", minute="5")


@pytest.fixture
def always_on_task(client: User):
    """Create an always_on task"""
    try:
        return client.create_always_on_task(command="cd")
    except PythonAnywhereError:
        pytest.skip(
            "Max always_on tasks or a free account, skipping always_on task tests."
        )
