# Standard library imports

from typing import TYPE_CHECKING

# Local application/library specific imports

from .sched_task import SchedTask

if TYPE_CHECKING:
    from .user import User


class AlwaysOnTask:
    """
    Implements AlwaysOnTask endpoints.

    See Also https://help.pythonanywhere.com/pages/AlwaysOnTasks/
    """

    url: str
    id: int
    ...

    def __init__(self, resp: dict, user: "User") -> None:
        vars(self).update(resp)
        self._user = user

    async def restart(self) -> None:
        """Restart an always_on task."""
        await self._user.request("POST", self.url + "restart/")

    async def delete(self) -> None:
        """Delete the task."""
        await self._user.request("DELETE", self.url)

    async def update(self, **kwargs) -> None:
        """
        Updates the task. All times are in UTC.

        Args:
            **kwargs: command str, minute str, hour str, interval str, description str,
            enabled bool

        Examples:
            >>> user = User(...)
            >>> task = await user.get_always_on_task_by_id(...)
            >>> await task.update(command='cd')
        """
        await self._user.request("PATCH", self.url, data=kwargs)
        vars(self).update(kwargs)

    def __str__(self):
        return self.url

    def __eq__(self, other):
        return self.url == other.url
