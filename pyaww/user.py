# Standard library imports

import asyncio
import json

from typing import AsyncIterator, Optional, TextIO, Union, Any

# Related third party imports

import aiohttp


# Local application/library specific imports

from .console import Console
from .file import File
from .sched_task import SchedTask
from .always_on_task import AlwaysOnTask
from .webapp import WebApp
from .errors import raise_error, raise_limit_error_and_await
from .utils import Cache
from .utils.limiter import Route


async def _parse_json(
    resp: aiohttp.ClientResponse, return_json: bool
) -> Union[dict, aiohttp.ClientResponse]:
    """Parse the JSON and raise errors."""
    if not return_json:
        return resp

    jsoned = await resp.json(content_type=None)

    if jsoned:
        for key in ("detail", "error", "error_message", "non_field_errors"):
            if key in jsoned:
                raise_error((resp.status, jsoned[key]))

    return jsoned


class User:
    """
    The brain of the operation. All modules are connected to this class in one way or another.

    Constructors:
        `User.create_console`;`User.get_console_by_id`;`User.consoles()`  -> **Console**

        `User.get_file_by_path`;`User.create_file` -> **File**

        `User.tasks`;`User.get_sched_task_by_id`;`User.create_sched_task` -> **SchedTask**

        `User.tasks`;`User.create_always_on_task`;`User.get_always_on_task_by_id` -> **AlwaysOnTask**

        `User.get_webapp_by_domain_name`;`User.webapps`;`User.create_webapp` -> **WebApp**
    """

    def __init__(
        self,
        username: str,
        auth: str,
        async_session: aiohttp.ClientSession = None,
        from_eu: bool = False,
    ) -> None:
        """
        Args:
            username (str): Username of the account
            auth (str): API token of the account
            from_eu (bool): Whether you are from europe or not, because European accounts API URL is different
        """
        self.use_cache = True
        self.use_limiter = True
        self.disable_limiter_for_routes = []
        self.cache = Cache()

        self.from_eu = from_eu
        self.username = username
        self.token = auth

        self.session = async_session
        self.sem = asyncio.Semaphore(10)
        self.lock = asyncio.Lock()
        self.routes = {}

        self.headers = {"Authorization": f"Token {self.token}"}
        self.request_url = (
            "https://www.pythonanywhere.com"
            if not self.from_eu
            else "https://eu.pythonanywhere.com"
        )

        if len(self.token) != 40:
            raise_error((401, "Invalid token."))


    def limiter(self, url: str) -> None:
        """ creates Route object for new routes and calls raise_limit_error if route is not callable"""
        if url not in self.routes:
            self.routes[url] = Route(url)
        if self.routes[url].callable() == False:
            raise_limit_error_and_await(self.routes[url])

    async def request(
        self, method: str, url: str, return_json: bool = False, **kwargs
    ) -> Any:
        """Request function for the module"""

        if self.use_limiter and url not in self.disable_limiter_for_routes:
            self.limiter(url)
        if not self.session:
            self.session = aiohttp.ClientSession()

        async with self.sem:
            resp = await self.session.request(
                method=method,
                url=self.request_url + url,
                headers=self.headers,
                **kwargs,
            )
            return await _parse_json(resp, return_json)

    async def get_cpu_info(self) -> dict:
        """
        Gets CPU information.

        Returns:
            dict: dictionary that contains relevant information (next_reset_time, time_left, time_left_untiL_reset)
        """
        return await self.request(
            "GET", f"/api/v0/user/{self.username}/cpu/", return_json=True
        )

    async def shared_consoles(self) -> list[Console]:
        """
        Return shared consoles for the user. This is not being cached because shared consoles are accessed by several
        people therefore, it's likely that the cache will be inaccurate.

        Returns:
            list[Console]: list of shared consoles
        """
        return [
            Console(console, self)
            for console in await self.request(
                "GET",
                f"/api/v0/user/{self.username}/consoles/shared_with_you/",
                return_json=True,
            )
        ]

    async def consoles(self) -> list[Console]:
        """
        Return a list of personal consoles for the user.

        Returns:
            list[Console]: list of shared personal consoles
        """
        consoles = await self.cache.all("console") or [
            Console(console, self)
            for console in await self.request(
                "GET",
                f"/api/v0/user/{self.username}/consoles//",
                return_json=True,
            )
        ]
        await self.cache.set("console", object_=consoles, allow_all_usage=True)

        return consoles

    async def get_console_by_id(self, id_: int) -> Console:
        """Get a console by its id."""
        console = await self.cache.get("console", id_=id_) or Console(
            await self.request(
                "GET", f"/api/v0/user/{self.username}/consoles/{id_}", return_json=True
            ),
            self,
        )
        await self.cache.set("console", object_=console)

        return console

    async def create_console(
        self, executable: str, workingdir: str = None, arguments: str = ""
    ) -> Optional[Console]:
        """
        Creates a console. Console must be started upon creation to send input to it.

        Args:
            executable (str): executable for the console to use (example python3.8)
            workingdir (str): console arguments
            arguments (str): working directory for console

        Examples:
            >>> user = User(...)
            >>> await user.create_console('python3.8')

        Returns:
            Optional[Console]: console object, console sucessfully created or None if console limit was hit
        """
        url = f"/api/v0/user/{self.username}/consoles/"

        try:
            resp = await self.request(
                "POST",
                url,
                return_json=True,
                data={
                    "executable": executable,
                    "arguments": arguments,
                    "working_directory": workingdir,
                },
            )
        except json.decoder.JSONDecodeError:
            raise_error((429, "Console limit reached."))

        # noinspection PyUnboundLocalVariable
        console = Console(resp, self)
        await self.cache.set("console", object_=console)

        return console

    async def listdir(
        self, path: str, recursive: bool = False, only_subdirectories: bool = True
    ) -> AsyncIterator[str]:
        """
        List dir that crawls into dirs (if recursive is set to true), if not, list files and sub-dirs in a directory.

        Args:
            path (str): path to be "searched" for files / subdirs
            recursive (bool): option whether subdirs and subdirs inside should be searched and so-on
            only_subdirectories (bool): self explanatory

        Examples:
            >>> user = User(...)
            >>> async for await user.listdir('/home/yourname/my_site/', recursive=True)

        Returns:
            AsyncIterator[str]: generator with paths
        """
        resp = await self.request(
            "GET",
            f"/api/v0/user/{self.username}/files/tree/?path={path}",
            return_json=True,
        )

        if not recursive:
            yield resp
            return

        for path in resp:
            if path.endswith("/"):
                async for item in self.listdir(path, True, not only_subdirectories):
                    yield item
                    await asyncio.sleep(0)
            elif only_subdirectories:
                yield path
                await asyncio.sleep(0)

    async def get_file_by_path(self, path: str) -> File:
        """
        Function to get a file. Does not error if not found.

        Args:
            path (str): path to the file

        Returns:
            File: File class (see pyaww.file)
        """
        return File(path, self)

    async def create_file(self, path: str, file: TextIO) -> File:
        """
        Create or update a file at a path.

        Args:
            path (str): path as to where the file shall be created (must include name + file extension in path)
            file (TextIO): file to be created / updated

        Examples:
            >>> user = User(...)
            >>> with open('./grocery_list.txt') as f:
            >>>    await user.create_file('/home/yourname/grocery_list.txt', f)
        """
        await self.request(
            "POST",
            f"/api/v0/user/{self.username}/files/path/{path}",
            return_json=True,
            data={"content": file},
        )

        return File(path, self)

    async def students(self) -> dict:
        """List students of the user."""
        return await self.request(
            "GET", f"/api/v0/user/{self.username}/students/", return_json=True
        )

    async def remove_student(self, student: str) -> None:
        """Remove a student from the students list."""
        try:
            await self.request(
                "DELETE", f"/api/v0/user/{self.username}/students/{student}"
            )
        except json.decoder.JSONDecodeError:
            pass

    async def always_on_tasks(self) -> list[AlwaysOnTask]:
        """Get always on tasks"""
        always_on = await self.request(
            "GET", f"/api/v0/user/{self.username}/always_on", return_json=True
        )

        return [AlwaysOnTask(i, self) for i in always_on]

    async def scheduled_tasks(self) -> list[SchedTask]:
        """Get scheduled tasks."""
        sched_tasks = await self.cache.all("sched_task") or [
            SchedTask(sched_task, self)
            for sched_task in await self.request(
                "GET", f"/api/v0/user/{self.username}/schedule/", return_json=True
            )
        ]
        await self.cache.set("sched_task", object_=sched_tasks, allow_all_usage=True)

        return sched_tasks

    async def get_sched_task_by_id(self, id_: int) -> SchedTask:
        """Get a scheduled task via it's id."""
        sched_task = await self.cache.get("sched_task", id_=id_) or SchedTask(
            await self.request(
                "GET", f"/api/v0/user/{self.username}/schedule/{id_}/", return_json=True
            ),
            self,
        )
        await self.cache.set("sched_task", object_=sched_task)

        return sched_task

    async def create_sched_task(
        self,
        command: str,
        minute: str,
        hour: str,
        interval: str = "daily",
        enabled: bool = True,
        description: str = "",
    ) -> SchedTask:
        """
        Create a scheduled task. All times are in UTC.

        Args:
            command (str): command to be executed every x time
            minute (str): minute: minute when the task should be executed
            hour (str): hour when the task should be executed
            interval (str): frequency the task should happen (example, daily)
            enabled (bool): option as to whether the task should be enabled
            description (str): description of the task

        Examples:
            >>> user = User(...)
            >>> await user.create_sched_task('cmd', '5', '5', 'daily', False, 'do "cmd"')

        Returns:
            SchedTask
        """
        sched_task = SchedTask(
            await self.request(
                "POST",
                f"/api/v0/user/{self.username}/schedule/",
                return_json=True,
                data={
                    "command": command,
                    "enabled": enabled,
                    "interval": interval,
                    "hour": hour,
                    "minute": minute,
                    "description": description,
                },
            ),
            self,
        )
        await self.cache.set("sched_task", object_=sched_task)

        return sched_task

    async def create_always_on_task(
        self, command: str, description: str = "", enabled: bool = True
    ) -> AlwaysOnTask:
        """
        Creates a always_on task, do not confuse it with a scheduled task.

        Args:
            command (str): command to be executed
            description (str): description of the task
            enabled (bool): whether the task should be enabled upon creation

        Examples:
            >>> user = User(...)
            >>> await user.create_always_on_task('/home/yourname/myscript.py', 'Scrape a website', True)

        Returns:
            AlwaysOnTask
        """
        data = {"command": command, "description": description, "enabled": enabled}

        resp = await self.request(
            "POST",
            f"/api/v0/user/{self.username}/always_on/",
            return_json=True,
            data=data,
        )
        return AlwaysOnTask(resp, self)

    async def get_always_on_task_by_id(self, id_: int) -> AlwaysOnTask:
        """Gets an always_on task."""
        resp = await self.request(
            "GET", f"/api/v0/user/{self.username}/always_on/{id_}/", return_json=True
        )
        return AlwaysOnTask(resp, self)

    async def python_versions(self) -> list:
        """Get all 3 ("python3", "python" and "run button") versions."""
        return [
            await self.request(
                "GET",
                f"/api/v0/user/{self.username}/default_python3_version/",
                return_json=True,
            ),
            await self.request(
                "GET",
                f"/api/v0/user/{self.username}/default_python_version/",
                return_json=True,
            ),
            await self.request(
                "GET",
                f"/api/v0/user/{self.username}/default_save_and_run_python_version/",
                return_json=True,
            ),
        ]

    async def set_python_version(self, version: float, command: str) -> None:
        """
        Set default python version.

        Args:
            version (float): version to be set
            command (str): takes "python3", "python" and/or "save_and_run_python"

        Examples:
            >>> user = User(...)
            >>> user.set_python_version(3.8, 'python3')
        """
        await self.request(
            "PATCH",
            f"/api/v0/user/{self.username}/default_{command}_version/",
            data={f"default_{command}_version": version},
        )

    async def get_system_image(self) -> dict:
        """
        Get the current system image.

        The system image for your account determines the versions of Python that you can use and the packages that
        are pre-installed.
        """
        return await self.request(
            "GET", f"/api/v0/user/{self.username}/system_image/", return_json=True
        )

    async def set_system_image(self, system_image: str) -> None:
        """
        Set the system image. Please see https://help.pythonanywhere.com/pages/ChangingSystemImage for the table.

        Args:
            system_image (str): system image to be set
        """
        await self.request(
            "PATCH",
            f"/api/v0/user/{self.username}/system_image/",
            data={"system_image": system_image},
        )

    async def get_webapp_by_domain_name(self, domain_name: str) -> WebApp:
        """Get a webapp via its domain."""
        resp = await self.request(
            "GET",
            f"/api/v0/user/{self.username}/webapps/{domain_name}/",
            return_json=True,
        )
        return WebApp(resp, self)

    async def webapps(self) -> list[WebApp]:
        """Get webapps for the user."""
        resp = await self.request(
            "GET", f"/api/v0/user/{self.username}/webapps/", return_json=True
        )
        return [WebApp(i, self) for i in resp]

    async def create_webapp(self, domain_name: str, python_version: str) -> WebApp:
        """
        Creata a webapp.

        Args:
            domain_name (str): domain name of the webapp
            python_version (str): python version for the webapp to use (ex: python37 which stands for python 3.7)

        Examples:
            >>> user = User(...)
            >>> await user.create_webapp('username.pythonanywhere.com', 'python39')

        Returns:
            WebApp
        """
        data = {"domain_name": domain_name, "python_version": python_version}

        await self.request(
            "POST",
            f"/api/v0/user/{self.username}/webapps/",
            return_json=True,
            data=data,
        )  # does not return all the necessary data for pyaww.WebApps init
        return await self.get_webapp_by_domain_name(domain_name=domain_name)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    def __str__(self):
        return str(self.headers)

    def __eq__(self, other):
        return self.headers == getattr(other, "headers", None)

    def __copy__(self) -> "User":
        return User(
            username=self.username,
            auth=self.headers["Authorization"].split("Token ")[1],
        )
