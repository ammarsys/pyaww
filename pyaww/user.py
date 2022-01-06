# Standard library imports

import asyncio
import json
import datetime
from typing import AsyncIterator, Optional, TextIO, Union, Any

# Related third party imports

import aiohttp

# Local application/library specific imports

from .console import Console
from .file import File
from .sched_task import SchedTask
from .always_on_task import AlwaysOnTask
from .webapp import WebApp
from .types import cache_type
from .errors import raise_error
from .utils import CachedResponse, URLCache


async def _parse_json(
    resp: aiohttp.ClientResponse, return_json: bool
) -> Optional[dict]:
    """Parse the JSON and raise errors."""
    jsoned = await resp.json(content_type=None)

    if jsoned:
        for key in ("detail", "error", "error_message", "non_field_errors"):
            if key in jsoned:
                raise_error((resp.status, jsoned[key]))

    return jsoned if return_json else resp


async def _parse_data(data: Union[str, dict]) -> Union[str, dict]:
    """
    Parse the POST request data so it works with tha caching system.

    Args:
        data (Union[str, dict]): if it's a str, it means the data was probably retrieved from the cache and now must be
        converted to its original type and if it's a dictionary, it is most likely data argument in the request function
        that needs to be converted to a string so it's hashable and able to be stored inside the dictionary as a key.

    Returns:
        Union[str, dict]
    """
    if isinstance(data, str):
        return json.loads(data)

    elif isinstance(data, dict):
        return json.dumps(data)

    return data


async def _time(seconds: int) -> datetime.datetime:
    """Make a timedelta in the future"""
    return datetime.datetime.now() + datetime.timedelta(seconds=seconds)


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
        self.cache: cache_type = {}
        self.disable_cache = {}

        self.from_eu = from_eu
        self.username = username
        self.token = auth

        self.session = async_session
        self.sem = asyncio.Semaphore(10)
        self.lock = asyncio.Lock()

        self.headers = {"Authorization": f"Token {self.token}"}
        self.request_url = (
            "https://www.pythonanywhere.com"
            if not self.from_eu
            else "https://eu.pythonanywhere.com"
        )

        if len(self.token) != 40:
            raise_error((401, "Invalid token."))

    async def __make_request(
        self, method: str, url: str, **kwargs
    ) -> aiohttp.ClientResponse:
        """Make a request; private because it can mess with caching"""
        return await self.session.request(
            method=method,
            url=self.request_url + url,
            headers=self.headers,
            **kwargs,
        )

    async def request(
        self,
        method: str,
        url: str,
        return_json: bool = False,
        data: dict = None,
        cache: bool = True,
        cache_time: bool = 30,
    ) -> Union[aiohttp.ClientResponse, Any]:
        """
        Request function for the API.

        TTL caching is handled here using pyaww.URLCache and pyaww.CachedResponse. To prevent an URL from being cached,
        add it to the User.disable_cache instance variable. Sample use for this would be any sort of URLs that create
        things, such as creating consoles, you don't want that to be cached.

        Cached URLs are stored in a dictionary (instance variable "cache") which keys are the URLs and it's values an
        utils.cache.URLCache object. The time-to-live of values is handled inside the utils.cache.URLCache objects via
        the dunder methods, (__contains__ and __getitem__.)

        If the method is a POST request, the data dictionary will be converted to a string to be stored inside the
        dictionary and the POST request will be made with the actual dictionary. Upon sucessfully getting to the caching
        return stage, the string will be converted to a dictionary again.

        Cache is handled inside the functions that create submodules. The structure is usually like,

        create_x (e.g. create_console)
        get_x_by_y (e.g. get_console_by_id)
        xs (e.g. consoles)

        The "creator" for the examples in the parentheses is `create_console`. It edits the other functions cache to
        make them up to date, specifically the asyncio.Lock.__aenter__ inside User.create_console. It will append onto
        the pyaww.CachedRecord ret parameter for the /api/v0/user/name/consoles/ endpoint if the URL and parameters are
        present in the instance variable cache. It will not create a utils.cache.URLCache object incase the URL is not
        present in cache, because it may lead to inaccurate results (e.g. calling User.create_console then User.
        consoles.) For the get_console_by_id cache, it will simply create an URLCache object as the console URLs are
        always unique, meaning it is never present in the cache.

        The latter structure and caching logic is applied to the rest of the "creator" methods.

        Args:
            cache_time (bool): seconds param for _time
            cache (bool): takes a bool argument on whether to cache or not
            data (dict): data for the post request
            return_json (bool): return jsoned output
            method (str): method for the http request
            url (str): URL for the http request

        Returns:
            Union[aiohttp.ClientResponse, dict]
        """
        if not data:
            data = {}

        if not self.session:
            self.session = aiohttp.ClientSession()

        time = await _time(seconds=cache_time)

        async with self.sem:
            if url in self.disable_cache or not self.use_cache or not cache:
                resp = await _parse_json(
                    await self.__make_request(method, url, data=data), return_json
                )

            elif url in self.cache:
                params = (method, await _parse_data(data))

                try:
                    return self.cache[url][params].ret
                except KeyError:
                    resp = await _parse_json(
                        await self.__make_request(method, url, data=data), return_json
                    )

                    async with self.lock:
                        self.cache[url][params] = CachedResponse(params, time, resp)

            else:
                params = (method, await _parse_data(data))
                resp = await _parse_json(
                    await self.__make_request(method, url, data=data), return_json
                )

                async with self.lock:
                    self.cache[url] = URLCache(
                        url, to_cache=(params, CachedResponse(params, time, resp))
                    )

        return resp

    async def get_cpu_info(self) -> dict:
        """
        Gets CPU information.

        Returns:
            dict: dictionary that contains relevant information (next_reset_time, time_left, time_left_untiL_reset)
        """
        return await self.request(
            "GET", f"/api/v0/user/{self.username}/cpu/", return_json=True
        )

    async def consoles(self) -> dict[str, list[Console]]:
        """
        Return a list of consoles for the user.

        Returns:
            Dict[str, List[Console]]:
            dictionary with keys (personal, shared) and values of shared and personal consoles.
        """
        personal = await self.request(
            "GET", f"/api/v0/user/{self.username}/consoles/", return_json=True
        )
        shared = await self.request(
            "GET",
            f"/api/v0/user/{self.username}/consoles/shared_with_you/",
            return_json=True,
        )

        return {
            "personal": [Console(console, self) for console in personal],
            "shared": [Console(console, self) for console in shared],
        }

    async def get_console_by_id(self, id_: int) -> Console:
        """Get a console by its id."""
        resp = await self.request(
            "GET", f"/api/v0/user/{self.username}/consoles/{id_}", return_json=True
        )
        return Console(resp, self)

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
                data={
                    "executable": executable,
                    "arguments": arguments,
                    "working_directory": workingdir,
                },
                return_json=True,
                cache=False,
            )
        except json.decoder.JSONDecodeError:
            resp = None  # Just for linters (local var resp might be referenced before assigment)
            raise_error((429, "Console limit reached."))

        async with self.lock:
            params = ("GET", "{}")

            if url in self.cache:
                if params in self.cache[url].cache:
                    self.cache[url].cache[params].ret.append(resp)

            self.cache[f"{url}{resp['id']}/"] = URLCache(
                url, to_cache=(params, CachedResponse(params, await _time(30), resp))
            )

        return Console(resp, self)

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
            data={"content": file},
            return_json=True,
            cache=False,
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
                "DELETE",
                f"/api/v0/user/{self.username}/students/{student}",
                cache=False,
            )
        except json.decoder.JSONDecodeError:
            pass

    async def tasks(self) -> dict[str, list]:
        """
        Get tasks for the user.

        Returns:
            dictionary containing both scheduled and always_on tasks
        """
        schedules = await self.request(
            "GET", f"/api/v0/user/{self.username}/schedule/", return_json=True
        )
        always_on = await self.request(
            "GET", f"/api/v0/user/{self.username}/always_on", return_json=True
        )
        return {
            "scheduled_tasks": [SchedTask(i, self) for i in schedules],
            "always_on_tasks": [AlwaysOnTask(i, self) for i in always_on],
        }

    async def get_sched_task_by_id(self, id_: int) -> SchedTask:
        """Get a scheduled task via it's id."""
        resp = await self.request(
            "GET", f"/api/v0/user/{self.username}/schedule/{id_}/", return_json=True
        )
        return SchedTask(resp, self)

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
        data = {
            "command": command,
            "enabled": enabled,
            "interval": interval,
            "hour": hour,
            "minute": minute,
            "description": description,
        }

        resp = await self.request(
            "POST",
            f"/api/v0/user/{self.username}/schedule/",
            data=data,
            return_json=True,
        )
        return SchedTask(resp, self)

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
            data=data,
            return_json=True,
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
            data=data,
            return_json=True,
        )  # does not return all the necessary data for pyaww.WebApps init
        return await self.get_webapp_by_domain_name(domain_name=domain_name)

    def __aenter__(self):
        return self

    def __aexit__(self, exc_type, exc_val, exc_tb):
        self.session.close().__await__()

    def __str__(self):
        return str(self.headers)
