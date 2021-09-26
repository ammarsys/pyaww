"""Class for the always on tasks API endpoints"""

# Standard library imports
from typing import TYPE_CHECKING

# Local application/library specific imports
from .sched_task import SchedTask

if TYPE_CHECKING:
    from .user import User


class AlwaysOnTask(SchedTask):
    """Inherits sheduled task class because they're pretty similar. Only 1 method difference."""
    def __init__(self, resp: dict, user: 'User') -> None:
        super().__init__(resp, user)

    def restart(self) -> None:
        """Restart a always_on task."""
        self._user.request('POST', self.url + 'restart/')

    def __str__(self):
        return self.url
