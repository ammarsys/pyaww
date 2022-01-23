# Standard library imports

from typing import TYPE_CHECKING, Optional

# Local application/library specific imports

if TYPE_CHECKING:
    from .user import User


class AlwaysOnTask:
    """
    Implements AlwaysOnTask endpoints.

    See Also https://help.pythonanywhere.com/pages/AlwaysOnTasks/
    """

    url: str
    id: int
    description: str
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

    async def update(
            self,
            command: Optional[str] = None,
            minute: Optional[str] = None,
            hour: Optional[str] = None,
            interval: Optional[str] = None,
            description: Optional[str] = None,
            enabled: Optional[bool] = None,
    ) -> None:
        """
        Updates the task. All times are in UTC.

        Examples:
            >>> user = User(...)
            >>> task = await user.get_always_on_task_by_id(...)
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
        if enabled is not None:
            data["enabled"] = description

        await self._user.request("PATCH", self.url, data=data)
        vars(self).update(data)

    def __str__(self):
        return self.url

    def __eq__(self, other):
        return self.url == getattr(other, "url", None)
