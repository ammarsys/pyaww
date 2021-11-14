# Standard library imports

import json
from typing import Iterator, Optional, TextIO

# Related third party imports

import requests

# Local application/library specific imports

from .console import Console
from .file import File
from .sched_task import SchedTask
from .always_on_task import AlwaysOnTask
from .webapp import WebApp
from .errors import raise_error
from utils import cache_func


class User:
    """The brain of the operation. All modules are connected to this class in one way or another."""

    def __init__(self, username: str, auth: str, from_eu: bool = False) -> None:
        """
        Args:
            username (str): Username of the account
            auth (str): API token of the account
            from_eu (bool): Whether you are from europe or not, because European accounts API URL is different
        """
        self.use_cache = True
        self.cache = {}

        self.from_eu = from_eu
        self.username = username
        self.token = auth

        self.session = requests.Session()
        self.headers = {"Authorization": f"Token {self.token}"}
        self.request_url = (
            "https://www.pythonanywhere.com"
            if not self.from_eu
            else "https://eu.pythonanywhere.com"
        )

        if len(self.token) != 40:
            raise_error((401, "Invalid token."))

    def request(self, method: str, url: str, **kwargs) -> requests.models.Response:
        """
        Custom function to send http requests which handles errors as well.

        Args:
            method (str): method for the http request
            url (str): URL for the http request
            **kwargs: any additional kwargs such as "data" for post requests

        Returns:
            requests.models.Response
        """
        resp = self.session.request(
            method, self.request_url + url, headers=self.headers, **kwargs
        )

        try:
            jsoned = resp.json()
        except json.decoder.JSONDecodeError:
            pass
        else:
            for key in ("detail", "error", "error_message", "non_field_errors"):
                if key in jsoned:
                    raise_error((resp.status_code, jsoned[key]))

        return resp

    @cache_func(seconds=300)
    def get_cpu_info(self) -> dict:
        """
        Gets CPU information.

        Returns:
            dict: dictionary that contains relevant information (next_reset_time, time_left, time_left_untiL_reset)
        """
        return self.request("GET", f"/api/v0/user/{self.username}/cpu/").json()

    def consoles(self) -> dict[str, list[Console]]:
        """
        Return a list of consoles for the user.

        Returns:
            Dict[str, List[Console]]:
            dictionary with keys (personal, shared) and values of shared and personal consoles.
        """
        personal = self.request("GET", f"/api/v0/user/{self.username}/consoles/").json()
        shared = self.request(
            "GET", f"/api/v0/user/{self.username}/consoles/shared_with_you/"
        ).json()

        return {
            "personal": [Console(console, self) for console in personal],
            "shared": [Console(console, self) for console in shared],
        }

    def get_console_by_id(self, id_: int) -> Console:
        """Get a console by its id."""
        resp = self.request(
            "GET", f"/api/v0/user/{self.username}/consoles/{id_}"
        ).json()

        return Console(resp, self)

    def create_console(
        self, executable: str, workingdir: str = None, arguments: str = ""
    ) -> Optional[Console]:
        """
        Creates a console. Console must be started upon creation to send input to it.

        Args:
            executable (str): executable for the console to use (example python3.8)
            workingdir (str): console arguments
            arguments (str): working directory for console

        Examples:
            >>> User(...).create_console('python3.8')

        Returns:
            Optional[Console]: console object, console sucessfully created or None if console limit was hit
        """
        try:
            resp = self.request(
                "POST",
                f"/api/v0/user/{self.username}/consoles/",
                data={
                    "executable": executable,
                    "arguments": arguments,
                    "working_directory": workingdir,
                },
            ).json()

            return Console(resp, self)

        except json.decoder.JSONDecodeError:
            raise_error((403, "You've reached the maximum number of consoles."))

    def listdir(
        self, path: str, recursive: bool = False, only_subdirectories: bool = True
    ) -> Iterator[str]:
        """
        List dir that crawls into dirs (if recursive is set to true), if not, list files and sub-dirs in a directory.

        Args:
            path (str): path to be "searched" for files / subdirs
            recursive (bool): option whether subdirs and subdirs inside should be searched and so-on
            only_subdirectories (bool): self explanatory

        Examples:
            >>> User(...).listdir('/home/yourname/my_site/', recursive=True)

        Returns:
            Iterator[str]: generator with paths
        """
        resp = self.request(
            "GET", f"/api/v0/user/{self.username}/files/tree/?path={path}"
        ).json()

        if not recursive:
            yield resp
            return

        for path in resp:
            if path.endswith("/"):
                yield from self.listdir(path, True, not only_subdirectories)
            elif only_subdirectories:
                yield path

    def get_file_by_path(self, path: str) -> File:
        """
        Function to get a file. Does not error if not found.

        Args:
            path (str): path to the file

        Returns:
            File: File class (see pyaww.file)
        """

        return File(path, self)

    def create_file(self, path: str, file: TextIO) -> File:
        """
        Create or update a file at a path.

        Args:
            path (str): path as to where the file shall be created (must include name + file extension in path)
            file (TextIO): file to be created / updated

        Examples:
            >>> with open('./grocery_list.txt') as f:
            >>>    User(...).create_file('/home/yourname/grocery_list.txt', f)
        """
        self.request(
            "POST",
            f"/api/v0/user/{self.username}/files/path/{path}",
            files={"content": file},
        )

        return File(path, self)

    @cache_func(300)
    def students(self) -> dict:
        """List students of the user."""
        return self.request("GET", f"/api/v0/user/{self.username}/students/").json()

    def remove_student(self, student: str) -> None:
        """Remove a student from the students list."""
        self.request("DELETE", f"/api/v0/user/{self.username}/students/{student}")

    def tasks(self) -> dict[str, list]:
        """
        Get tasks for the user.

        Returns:
            dictionary containing both scheduled and always_on tasks
        """
        schedules = self.request(
            "GET", f"/api/v0/user/{self.username}/schedule/"
        ).json()
        always_on = self.request(
            "GET", f"/api/v0/user/{self.username}/always_on"
        ).json()
        return {
            "scheduled_tasks": [SchedTask(i, self) for i in schedules],
            "always_on_tasks": [AlwaysOnTask(i, self) for i in always_on],
        }

    def get_sched_task_by_id(self, id_: int) -> SchedTask:
        """Get a scheduled task via it's id."""
        resp = self.request(
            "GET", f"/api/v0/user/{self.username}/schedule/{id_}/"
        ).json()
        return SchedTask(resp, self)

    def create_sched_task(
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
            >>> User(...).create_sched_task('cmd', '5', '5', 'daily', False, 'do "cmd"')

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

        resp = self.request(
            "POST", f"/api/v0/user/{self.username}/schedule/", data=data
        ).json()
        return SchedTask(resp, self)

    def create_always_on_task(
        self, command: str, description: str = "", enabled: bool = True
    ) -> AlwaysOnTask:
        """
        Creates a always_on task, do not confuse it with a scheduled task.

        Args:
            command (str): command to be executed
            description (str): description of the task
            enabled (bool): whether the task should be enabled upon creation

        Examples:
            >>> User(...).create_always_on_task('/home/yourname/myscript.py', 'Scrape a website', True)

        Returns:
            AlwaysOnTask
        """
        data = {"command": command, "description": description, "enabled": enabled}

        resp = self.request(
            "POST", f"/api/v0/user/{self.username}/always_on/", data=data
        ).json()
        return AlwaysOnTask(resp, self)

    def get_always_on_task_by_id(self, id_: int) -> AlwaysOnTask:
        """Gets an always_on task."""
        resp = self.request(
            "GET", f"/api/v0/user/{self.username}/always_on/{id_}/"
        ).json()
        return AlwaysOnTask(resp, self)

    @cache_func(seconds=180)
    def python_versions(self) -> list:
        """Get all 3 ("python3", "python" and "run button") versions."""
        return [
            self.request(
                "GET", f"/api/v0/user/{self.username}/default_python3_version/"
            ).json(),
            self.request(
                "GET", f"/api/v0/user/{self.username}/default_python_version/"
            ).json(),
            self.request(
                "GET",
                f"/api/v0/user/{self.username}/default_save_and_run_python_version/",
            ).json(),
        ]

    def set_python_version(self, version: float, command: str) -> None:
        """
        Set default python version.

        Args:
            version (float): version to be set
            command (str): takes "python3", "python" and/or "save_and_run_python"

        Examples:
            >>> User(...).set_python_version(3.8, 'python3')
        """
        self.request(
            "PATCH",
            f"/api/v0/user/{self.username}/default_{command}_version/",
            data={f"default_{command}_version": version},
        )

    @cache_func(seconds=300)
    def get_system_image(self) -> dict:
        """
        Get the current system image.

        The system image for your account determines the versions of Python that you can use and the packages that
        are pre-installed.
        """
        return self.request("GET", f"/api/v0/user/{self.username}/system_image/").json()

    def set_system_image(self, system_image: str) -> None:
        """
        Set the system image. Please see https://help.pythonanywhere.com/pages/ChangingSystemImage for the table.

        Args:
            system_image (str): system image to be set
        """
        self.request(
            "PATCH",
            f"/api/v0/user/{self.username}/system_image/",
            data={"system_image": system_image},
        )

    def get_webapp_by_domain_name(self, domain_name: str) -> WebApp:
        """Get a webapp via its domain."""
        resp = self.request(
            "GET", f"/api/v0/user/{self.username}/webapps/{domain_name}/"
        ).json()
        return WebApp(resp, self)

    @cache_func(300)
    def webapps(self) -> list[WebApp]:
        """Get webapps for the user."""
        resp = self.request("GET", f"/api/v0/user/{self.username}/webapps/").json()
        return [WebApp(i, self) for i in resp]

    def create_webapp(self, domain_name: str, python_version: str) -> WebApp:
        """
        Creata a webapp.

        Args:
            domain_name (str): domain name of the webapp
            python_version (str): python version for the webapp to use (ex: python37 which stands for python 3.7)

        Examples:
            >>> User(...).create_webapp('username.pythonanywhere.com', 'python39')

        Returns:
            WebApp
        """
        data = {"domain_name": domain_name, "python_version": python_version}

        self.request(
            "POST", f"/api/v0/user/{self.username}/webapps/", data=data
        ).json()  # does not return all the necessary data for pyaww.WebApps init
        return self.get_webapp_by_domain_name(domain_name=domain_name)

    def __enter__(self):
        return self

    def __del__(self):
        self.session.close()

    def __str__(self):
        return str(self.headers)
