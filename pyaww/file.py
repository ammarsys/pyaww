# Standard library imports

from typing import TYPE_CHECKING, TextIO

# Local application/library specific imports

from .errors import PythonAnywhereError

if TYPE_CHECKING:
    from .user import User


class File:
    """
    Implements File endpoints.

    See Also https://www.pythonanywhere.com/files/
    """

    def __init__(self, path: str, user: "User") -> None:
        self.path = path
        self._user = user

    def share(self) -> str:
        """
        Share a file.

        Returns:
            str: shared URL
        """
        return self._user.request(
            "POST",
            f"/api/v0/user/{self._user.username}/files/sharing/",
            data={"path": self.path},
        ).json()["url"]

    def unshare(self) -> None:
        """Function to stop sharing the file."""
        self._user.request(
            "DELETE",
            f"/api/v0/user/{self._user.username}/files/sharing/?path={self.path}",
        )

    def is_shared(self) -> bool:
        """Function to check sharing status of the file."""
        try:
            self._user.request(
                "GET",
                f"/api/v0/user/{self._user.username}/files/sharing/?path={self.path}",
            )
            return True
        except PythonAnywhereError:
            return False

    def delete(self) -> None:
        """Delete the file."""
        self._user.request(
            "DELETE", f"/api/v0/user/{self._user.username}/files/path/{self.path}"
        )

    def read(self) -> bytes:
        """Read files contents. The contents are in bytes, call decode() on it."""
        return self._user.request(
            "GET", f"/api/v0/user/{self._user.username}/files/path/{self.path}"
        ).content

    def update(self, content: TextIO) -> None:
        """
        Update the file.

        Args:
            content (TextIOWrapper): content the file shall be updated with

        Examples:
            >>> file = User(...).get_file_by_path('...')
            >>> with open('newcontent.txt', 'r') as f:
            >>>    file.update(f)
        """
        self._user.create_file(self.path, content)

    def __str__(self):
        return self.path
