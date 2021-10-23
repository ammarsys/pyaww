"""Class for the static file(s) API endpoints"""

# Standard library imports

from typing import TYPE_CHECKING

# Local application/library specific imports

if TYPE_CHECKING:
    from .webapp import WebApp


class StaticFile:
    """A static file is a file that can be served much faster of disk. Accesed via URL."""

    id: int
    url: str
    path: str

    def __init__(self, resp: dict, webapp: "WebApp"):
        self._webapp = webapp
        vars(self).update(resp)
        self._url = f"/api/v0/user/{self._webapp.user}/webapps/{self._webapp.domain_name}/static_files/{self.id}/"

    def delete(self) -> None:
        """Delete the static file."""
        self._webapp.userclass.request("DELETE", self._url)

    def update(self, **kwargs) -> None:
        """
        Update the static file.

        Args:
            **kwargs: can take url, path
        """
        self._webapp.userclass.request("PATCH", self._url, data=kwargs)
        vars(self).update(kwargs)

    def __str__(self):
        return self.url
