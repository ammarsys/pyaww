# Standard library imports

from typing import TYPE_CHECKING, Optional, Any

# Local library/library specific imports

if TYPE_CHECKING:
    from .webapp import WebApp


class StaticHeader:
    """Implements StaticHeader endpoints."""

    id: int
    url: str
    name: str
    value: dict

    def __init__(self, resp: dict, webapp: "WebApp") -> None:
        self._webapp = webapp
        vars(self).update(resp)
        self._url = f"/api/v0/user/{self._webapp.user}/webapps/{self._webapp.domain_name}/static_headers/{self.id}/"

    async def delete(self) -> None:
        """Delete the static header. Webapp restart required."""
        await self._webapp.userclass.request("DELETE", self._url)

    async def update(
        self,
        url: Optional[str] = None,
        name: Optional[str] = None,
        value: Optional[Any] = None,
    ) -> None:
        """Update the static header. Webapp restart required."""
        data = {}

        if url is not None:
            data["url"] = url
        if name is not None:
            data["name"] = name
        if value is not None:
            data["value"] = value

        await self._webapp.userclass.request("PATCH", self._url, data=data)
        vars(self).update(data)

    def __str__(self):
        return self.url

    def __eq__(self, other):
        return self.id == getattr(other, "id", None)
