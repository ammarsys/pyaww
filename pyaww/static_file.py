"""Class for the static file(s) API endpoints"""

# Standard library imports

from typing import TYPE_CHECKING

# Local application/library specific imports

from .static_header import StaticHeader

if TYPE_CHECKING:
    from .webapp import WebApp


class StaticFile(StaticHeader):
    """A static file is a file that can be served much faster of disk. Accesed via URL."""

    id: int
    url: str
    path: str

    def __init__(self, resp: dict, webapp: "WebApp"):
        super().__init__(resp, webapp)
        self._webapp = webapp
        vars(self).update(resp)
        self._url = f"/api/v0/user/{self._webapp.user}/webapps/{self._webapp.domain_name}/static_files/{self.id}/"
