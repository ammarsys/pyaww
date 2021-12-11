# Standard library imports

from typing import TYPE_CHECKING

# Local application/library specific imports

from .sched_task import SchedTask

if TYPE_CHECKING:
    from .user import User


class AlwaysOnTask(SchedTask):
    """
    Implements AlwaysOnTask endpoints.

    See Also https://help.pythonanywhere.com/pages/AlwaysOnTasks/
    """

    def __init__(self, resp: dict, user: "User") -> None:
        super().__init__(resp, user)

    async def restart(self) -> None:
        """Restart an always_on task."""
        await self._user.request("POST", self.url + "restart/")

    def __str__(self):
        return self.url

    def __eq__(self, other):
        return self.url == other.url
