# Standard library imports

from typing import TYPE_CHECKING, Optional

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
        await self._user.cache.pop("sched_task", id_=self.id)

    async def update(
        self,
        command: Optional[str] = None,
        minute: Optional[str] = None,
        hour: Optional[str] = None,
        interval: Optional[str] = None,
        description: Optional[str] = None,
    ) -> None:
        """
        Updates the task. All times are in UTC.

        Examples:
            >>> user = User(...)
            >>> task = await user.get_sched_task_by_id(...)
            >>> await task.update(command='cd')
        """
        data = {}

        if command is not None:
            data["command"] = command
        if minute is not None:
            data["minute"] = minute
        if hour is not None:
            data["hour"] = hour
        if interval is not None:
            data["interval"] = interval
        if description is not None:
            data["description"] = description

        await self._user.request("PATCH", self.url, data=data)
        vars(self).update(data)

        await self._user.cache.set("sched_task", object_=self)

    def __str__(self):
        return self.url

    def __eq__(self, other):
        return self.id == getattr(other, "id", None)
