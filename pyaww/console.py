# Standard library imports

from typing import TYPE_CHECKING
import inspect

# Local application/library specific imports

if TYPE_CHECKING:
    from .user import User


class Console:
    """
    Implements Console endpoints.

    See Also https://help.pythonanywhere.com/pages/TypesOfConsoles/
    """

    id: int
    user: "User"
    executable: str
    arguments: str
    working_directory: str
    name: str
    console_url: str
    console_frame_url: str

    def __init__(self, resp: dict, user: "User") -> None:
        vars(self).update(resp)
        self._user = user

    async def send_input(self, inp: str, end: str = "\n") -> str:
        """
        Function to send inputs to the console. Console must be started manually before hand.

        Args:
            inp (str): string to be inputted in the console
            end (str): pass '' to not "click enter" in console

        Examples:
            >>> user = User(...)
            >>> console = await user.get_console_by_id(...)
            >>> await console.send_input("print('hello!')", end='')

        Returns:
            str: latest writting in the console
        """
        await self._user.request("POST", "/api/v0" + self.console_url + f"send_input/", data={"input": inp + end})
        outs = await self.outputs()

        return outs.split("\r")[-2].strip()

    async def delete(self) -> None:
        """Delete the console."""
        await self._user.request("DELETE", "/api/v0" + self.console_url)

    async def outputs(self) -> str:
        """Return all outputs in the console."""
        resp = await self._user.request("GET", "/api/v0" + self.console_url + "get_latest_output/", return_json=True)

        return resp["output"]

    def __str__(self):
        return self.console_url
