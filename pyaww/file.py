# Standard library imports

from typing import TYPE_CHECKING, TextIO, Any

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

    async def share(self) -> str:
        """
        Share the file.

        Returns:
            str: shared URL
        """
        resp = await self._user.request(
            "POST",
            f"/api/v0/user/{self._user.username}/files/sharing/",
            return_json=True,
            data={"path": self.path},
        )
        return resp["url"]

    async def unshare(self) -> None:
        """Function to stop sharing the file."""
        await self._user.request(
            "DELETE",
            f"/api/v0/user/{self._user.username}/files/sharing/?path={self.path}",
            return_json=True,
        )

    async def is_shared(self) -> bool:
        """Function to check sharing status of the file."""
        try:
            await self._user.request(
                "GET",
                f"/api/v0/user/{self._user.username}/files/sharing/?path={self.path}",
                return_json=True,
            )
            return True
        except PythonAnywhereError:
            return False

    async def delete(self) -> None:
        """Delete the file."""
        await self._user.request(
            "DELETE", f"/api/v0/user/{self._user.username}/files/path/{self.path}"
        )

    async def read(self) -> str:
        """Read the files content."""
        resp = await self._user.request(
            "GET", f"/api/v0/user/{self._user.username}/files/path{self.path}"
        )

        return await resp.text()

    async def update(self, content: TextIO) -> None:
        """
        Update the file.

        Args:
            content (TextIOWrapper): content the file shall be updated with

        Examples:
            >>> user = User(...)
            >>> file = await user.get_file_by_path('...')
            >>> with open('newcontent.txt', 'r') as f:
            >>>    await file.update(f)
        """
        await self._user.create_file(self.path, content)

    def __str__(self):
        return self.path
