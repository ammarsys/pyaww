# Standard library imports

from typing import TYPE_CHECKING

# Local application/library specific imports

if TYPE_CHECKING:
    from .user import User


class SchedTask:
    """
    Implements ScheduledTask endpoints.

    See Also https://help.pythonanywhere.com/pages/ScheduledTasks/
    """

    id: int
    url: str
    user: str
    command: str
    expiry: str
    enabled: bool
    logfile: str
    extend_url: str
    interval: str
    hour: int
    minute: int
    printable_time: str
    can_enable: bool
    description: str

    def __init__(self, resp: dict, user: "User") -> None:
        vars(self).update(resp)
        self._user = user

    async def delete(self) -> None:
        """Delete the task."""
        await self._user.request("DELETE", self.url)
        await self._user.cache.pop('sched_task', id_=self.id)

    async def update(self, **kwargs) -> None:
        """
        Updates the task. All times are in UTC.

        Args:
            **kwargs: command str, minute str, hour str, interval str, description str,
            enabled bool

        Examples:
            >>> user = User(...)
            >>> task = await user.get_sched_task_by_id(...)
            >>> await task.update(command='cd')
        """
        await self._user.request("PATCH", self.url, data=kwargs)
        vars(self).update(kwargs)

    def __str__(self):
        return self.url

    def __eq__(self, other):
        return self.url == other.url
