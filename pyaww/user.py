import requests
import json

from .console import Console
from .file import File
from .sched_task import SchedTask
from .always_on_task import AlwaysOnTask
from .webapp import WebApp

from typing import Iterator, Optional, List, Dict
from io import TextIOWrapper

class PythonAnywhereError(Exception):
    """A base exception, nothing special to it, used everywhere."""
    pass

class User:
    """The brain of the operation. All modules are connected to this class in one way or another."""
    def __init__(self, username: str, auth: str, from_eu: bool = False) -> None:
        """
        Initialize class variables.

        :param str username: username of the API token
        :param str auth: pythonanywhere token get it at https://www.pythonanywhere.com/account/#api_toke
        :param bool from_eu: the url is tiny different for EU users hence why this is a parameter
        """
        self.from_eu = from_eu
        self.username = username
        self.token = auth
        self.session = requests.Session()
        self.headers = {'Authorization': f'Token {self.token}'}
        self.request_url = 'https://www.pythonanywhere.com' if not self.from_eu else 'https://eu.pythonanywhere.com'

    def request(self, method: str, url: str, **kwargs) -> requests.models.Response:
        """
        Custom function to send http requests which handles errors as well.

        :param method: method for the http request
        :param url: URL for the http request
        :param kwargs: any additional kwargs such as "data" for post requests
        :return: requests.models.Response
        :raises: pythonanywhereerror
        """
        resp = None

        try:
            resp = self.session.request(method, self.request_url + url, headers=self.headers, **kwargs)
            jsoned = resp.json()

            if 'detail' in jsoned:
                raise PythonAnywhereError(jsoned['detail'])
            elif 'error' in jsoned:
                raise PythonAnywhereError(jsoned['error'])
            elif 'error_message' in jsoned:
                raise PythonAnywhereError(jsoned['error_message'])
            elif 'non_field_errors' in jsoned:
                raise PythonAnywhereError(jsoned['non_field_errors'])

            return resp
        except json.decoder.JSONDecodeError:
            return resp

    def get_cpu_info(self) -> dict:
        """
        Gets CPU information.

        :return: dictionary that contains relevant information (next_reset_time, time_left, time_left_untiL_reset)
        """
        return self.request('GET', f'/api/v0/user/{self.username}/cpu/').json()

    def consoles(self) -> Dict[str, List[Console]]:
        """
        Return a list of consoles for the user.

        :return: dictionary with keys (personal, shared) and values of shared and personal consoles.
        """
        personal = self.request('GET', f'/api/v0/user/{self.username}/consoles/').json()
        shared = self.request('GET', f'/api/v0/user/{self.username}/consoles/shared_with_you/').json()

        return {
            'personal': [Console(console, self) for console in personal],
            'shared': [Console(console, self) for console in shared]
        }

    def get_console_by_id(self, id: int) -> Console:
        """
        Get a console by it's id.

        :param int id: ID of the console
        :return: console class (see pyaww.console)
        """
        resp = self.request('GET', f'/api/v0/user/{self.username}/consoles/{id}').json()

        return Console(resp, self)

    def create_console(self, executable: str, workingdir: str, arguments: str = '') -> Optional[Console]:
        """
        Creates a console.

        Sample usage -> User.create_console('python3.8', None, None)

        :param executable: executable for the console to use (example python3.8)
        :param arguments: console arguments
        :param workingdir: working directory for console
        :return: console object, console sucessfully created or None if console limit was hit
        """
        try:
            resp = self.request('POST',
                                f'/api/v0/user/{self.username}/consoles/',
                                data={'executable': executable, 'arguments': arguments, 'working_directory': workingdir}
                                ).json()

            return Console(resp, self)

        except json.decoder.JSONDecodeError:
            raise ValueError('You\'ve reached the maximum number of consoles.')

    def listdir(self, path: str, recursive: bool = False, only_subdirectories: bool = True) -> Iterator[File]:
        """
        List dir that crawls into dirs (if recursive is set to true), if not, list files and sub-dirs in a directory.

        Sample usage -> User.listdir('/home/yourname/my_site/', recursive=True)

        :param only_subdirectories: self explanatory
        :param str path: path to be "searched" for files / subdirs
        :param bool recursive: option whether subdirs and subdirs inside should be searched and so-on
        :return: generator with paths
        """
        resp = self.request('GET', f'/api/v0/user/{self.username}/files/tree/?path={path}').json()

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

        :param str path: path to the file
        :return: File class (see pyaww.file)
        """
        if '.' not in path.split('/')[-1]:
            raise PythonAnywhereError('Bad path, are you sure the path you\'re providing is a file?')

        return File(path, self)

    def create_file(self, path: str, file: TextIOWrapper) -> None:
        """
        Create or update a file at a path.

        Sample usage -> with open('./grocery_list.txt') as f: User.create_file('/home/yourname/grocery_list.txt', f)

        :param str path: path as to where the file shall be created (must include name + file extension in path)
        :param TextIOWrapper file: file to be created / updated
        """
        self.request('POST',
                     f'/api/v0/user/{self.username}/files/path/{path}',
                     files={'content': file})

    def students(self) -> dict:
        """
        List students of the user.

        :return: json dictionary
        """
        return self.request('GET', f'/api/v0/user/{self.username}/students/').json()

    def remove_student(self, student: str) -> None:
        """
        Remove a student from the students list.

        :param str student: student name to be removed
        """
        self.request('DELETE', f'/api/v0/user/{self.username}/students/{student}')

    def tasks(self) -> dict:
        """
        Get tasks for the user.

        :return: json dictionary
        """
        schedules = self.request('GET', f'/api/v0/user/{self.username}/schedule/').json()
        always_on = self.request('GET', f'/api/v0/user/{self.username}/always_on').json()
        return {
            'scheduled_tasks': [SchedTask(i, self) for i in schedules],
            'always_on_tasks': [SchedTask(i, self) for i in always_on]
        }

    def get_sched_task_by_id(self, id: int) -> SchedTask:
        """
        Get a scheduled task via it's id.

        :param int id: ID of the scheduled task
        :return: Task class (see pyaww.sched_task)
        """
        resp = self.request('GET', f'/api/v0/user/{self.username}/schedule/{id}/').json()
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

        Sample usage -> User.create_sched_task('cmd', 5, 5, 'daily', True, 'perform "cmd"')

        :param str command: command to be executed every x time
        :param bool enabled: option as to whether the task should be enabled
        :param str interval: frequency the task should happen (example, daily)
        :param str hour: hour when the task should be executed
        :param str minute: minute when the task should be executed
        :param str description: description of the task
        :return: scheduled task class (see pyaww.sched_task)
        """

        data = {'command': command, 'enabled': enabled, 'interval': interval, 'hour': hour, 'minute': minute,
                'description': description}

        resp = self.request('POST', f'/api/v0/user/{self.username}/schedule/', data=data).json()
        return SchedTask(resp, self)

    def create_always_on_task(self, command: str, description: str = '', enabled: bool = True) -> AlwaysOnTask:
        """
        Creates a always_on task, do not confuse it with a scheduled task.

        Sample usage -> User.create_always_on_task('/home/yourname/myscript.py', 'Scrape a website', True)

        :param str command: command to be executed
        :param str description: description of the task
        :param bool enabled: whether the task should be enabled upon creation
        :return: AlwaysOnTask (see pyaww.always_on_task)
        """
        data = {'command': command, 'description': description, 'enabled': enabled}

        resp = self.request('POST', f'/api/v0/user/{self.username}/always_on/', data=data).json()
        return AlwaysOnTask(resp, self)

    def get_always_on_task_by_id(self, id: int) -> AlwaysOnTask:
        """
        Gets a always_on task.

        :param int id: ID of the task
        :return: AlwaysOnTask (see pyaww.always_on_task)
        """
        resp = self.request('GET', f'/api/v0/user/{self.username}/always_on/{id}/').json()
        return AlwaysOnTask(resp, self)

    def python_versions(self) -> list:
        """
        Get all 3 ("python3", "python" and "run button") versions.

        :return: list of json dictionaries
        """
        return [
            self.request('GET', f'/api/v0/user/{self.username}/default_python3_version/').json(),
            self.request('GET', f'/api/v0/user/{self.username}/default_python_version/').json(),
            self.request('GET', f'/api/v0/user/{self.username}/default_save_and_run_python_version/').json()
        ]

    def set_python_version(self, version: float, command: str) -> None:
        """
        Set default python version.

        Sample usage -> User.set_python_version('3.8', 'python3')

        :param float version: version to be set
        :param str command: takes "python3", "python" and/or "save_and_run_python"
        """
        self.request(
            'PATCH', f'/api/v0/user/{self.username}/default_{command}_version/',
            data={f'default_{command}_version': version}
        )

    def get_system_image(self) -> dict:
        """
        Get the current system image. The system image for your account determines the
        versions of Python that you can use and the packages that are pre-installed.

        :return: json dictionary
        """
        return self.request('GET', f'/api/v0/user/{self.username}/system_image/').json()

    def set_system_image(self, system_image: str) -> None:
        """
        Set the system image. Please see https://help.pythonanywhere.com/pages/ChangingSystemImage for the table.

        Sample usage -> User.set_system_image('fishnchips') # see ^^^ to understand what's fishnchips

        :param str system_image: system image to be set
        """
        self.request('PATCH', f'/api/v0/user/{self.username}/system_image/', data={"system_image": system_image})

    def get_webapp_by_domain_name(self, domain_name: str) -> WebApp:
        """
        Get a webapp via it's name.

        Sample usage -> User.get_webbapp_by_domain_name('yourname.pythonanywhere.com')

        :param str domain_name: webapps domain
        :return: WebApp (see pyaww.webapp)
        """
        resp = self.request('GET', f'/api/v0/user/{self.username}/webapps/{domain_name}/').json()

        return WebApp(resp, self)

    def webapps(self) -> List[WebApp]:
        """
        Get webapps for the user.

        :return: a list of webapps (see pyaww.webapp)
        """
        resp = self.request('GET', f'/api/v0/user/{self.username}/webapps/').json()
        return [WebApp(i, self) for i in resp]

    def create_webapp(self, domain_name: str, python_version: str) -> WebApp:
        """
        Create a webapp.

        Sample usage -> User.create_webapp('test.com', 'python3.8')

        :param str domain_name: domain name of the webapp
        :param python_version: python version for the webapp to use (ex: python3.7)
        :return: WebApp (see pyaww.webapp)
        """
        data = {'domain_name': domain_name, 'python_version': python_version}

        resp = self.request('POST', f'/api/v0/user/{self.username}/webapps/', data=data).json()
        return WebApp(resp, self)

    def __enter__(self):
        return self

    def __del__(self):
        self.session.close()

    def __str__(self):
        return str(self.headers)
