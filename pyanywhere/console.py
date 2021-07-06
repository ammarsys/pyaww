from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User


class Console:
    """All methods of a console/."""
    id: int
    user: 'User'
    executable: str
    arguments: str
    working_directory: str
    name: str
    console_url: str
    console_frame_url: str

    def __init__(self, resp: dict, user: 'User') -> None:
        """
        Initialize class variables.

        :param dict resp: json dictionary returned by the API
        :param user: User class (see pyanywhere.user)
        """
        vars(self).update(resp)
        self._user = user

    def send_input(self, inp: str, end: str = '\n') -> str:
        """
        Function to send inputs to a console.

        Sample usage -> Console.send_input("print('hello!')", end='')

        :param str inp: string to be inputted in the console
        :param bool end: pass '' to not "click enter" in console
        :return: latest output (output of that code)
        """
        self._user.request(
            'POST',
            '/api/v0' + self.console_url + f'send_input/',
            data={'input': inp + end}
        )
        return self.outputs().split('\r')[-2].strip()

    def delete(self) -> None:
        """Function to delete a console. Sample usage -> Console.delete()"""
        self._user.request('DELETE', '/api/v0' + self.console_url)

    def outputs(self) -> str:
        """Functions to return all outputs in a console. Sample usage -> Console.outputs()"""
        return self._user.request('GET', '/api/v0' + self.console_url + 'get_latest_output/').json()['output']

    def __str__(self):
        return self.console_url