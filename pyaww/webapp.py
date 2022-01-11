# Standard library imports

from typing import TYPE_CHECKING

# Local application/library specific imports

from .static_file import StaticFile
from .static_header import StaticHeader
from .errors import PythonAnywhereError

if TYPE_CHECKING:
    from .user import User


class WebApp:
    """
    Implements WebApp endpoints.

    See Also https://help.pythonanywhere.com/pages/WebAppBasics/

    Constructors:
        `WebApp.static_files`;`WebApp.create_static_file`;`WebApp.get_static_file_by_id` -> **StaticFile**

        `WebApp.static_headers`;`WebApp.create_static_header`;`WebApp.get_static_header_by_id` -> **StaicHeader**
    """

    id: int
    user: str
    domain_name: str
    python_version: str
    source_directory: str
    working_directory: str
    virualenv_path: str
    expiry: str
    force_https: bool

    def __init__(self, resp: dict, user: "User") -> None:
        self._user: "User" = user
        vars(self).update(resp)

    async def delete(self) -> None:
        """Deletes the webapp."""
        await self._user.request(
            "DELETE", f"/api/v0/user/{self.user}/webapps/{self.domain_name}/"
        )

    async def update(self, **kwargs) -> None:
        """
        Updates config of the webapp. Reload required.

        Args:
            **kwargs: can take: python_version, source_directory, virtualenv_path, force_https,
            password_protection_enabled, password_protection_username, password_protection_password
        """
        await self._user.request(
            "PATCH",
            f"/api/v0/user/{self.user}/webapps/{self.domain_name}/",
            data=kwargs,
        )
        vars(self).update(kwargs)

    async def restart(self) -> None:
        """Reloads the webapp."""
        await self._user.request(
            "POST", f"/api/v0/user/{self.user}/webapps/{self.domain_name}/reload/"
        )

    async def disable(self) -> None:
        """Disables the webapp."""
        await self._user.request(
            "POST", f"/api/v0/user/{self.user}/webapps/{self.domain_name}/disable/"
        )

    async def enable(self) -> None:
        """Enables the webapp."""
        try:
            await self._user.request(
                "POST", f"/api/v0/user/{self.user}/webapps/{self.domain_name}/enable/"
            )
        except PythonAnywhereError:
            pass

    async def get_ssl_info(self) -> dict:
        """Gets TLS/HTTP info of the webapp."""
        return await self._user.request(
            "GET",
            f"/api/v0/user/{self.user}/webapps/{self.domain_name}/ssl/",
            return_json=True,
        )

    async def set_ssl_info(self, cert: str, private_key: str) -> None:
        """
        Set the TLS/HTTP info. Webapp reload required.

        Args:
            cert (str): TLS/HTTP certificate
            private_key (str): TLS/HTTP private key
        """
        data = {"cert": cert, "private_key": private_key}
        await self._user.request(
            "POST",
            f"/api/v0/user/{self.user}/webapps/{self.domain_name}/ssl/",
            data=data,
        )

    async def static_files(self) -> list[StaticFile]:
        """Gets the webapps static files."""
        resp = await self._user.request(
            "GET",
            f"/api/v0/user/{self.user}/webapps/{self.domain_name}/static_files/",
            return_json=True,
        )
        return [StaticFile(i, self) for i in resp]

    async def create_static_file(self, file_path: str, url: str) -> StaticFile:
        """
        Create a static file. Webapp reload required.

        Args:
            file_path (str): path of the file
            url (str): URL that should lead to the static file.

        Returns:
            StaticFile
        """
        data = {"path": file_path, "url": url}
        resp = await self._user.request(
            "POST",
            f"/api/v0/user/{self.user}/webapps/{self.domain_name}/static_files/",
            return_json=True,
            data=data,
        )
        return StaticFile(resp, self)

    async def get_static_file_by_id(self, id_: int) -> StaticFile:
        """
        Get a static file via it's id.

        Args:
            id_ (int): ID of the static file

        Returns:
            StaticFile
        """
        resp = await self._user.request(
            "GET",
            f"/api/v0/user/{self.user}/webapps/{self.domain_name}/static_files/{id_}/",
            return_json=True,
        )
        return StaticFile(resp, self)

    async def static_headers(self) -> list[dict]:
        """Get webapps static headers."""
        return await self._user.request(
            "GET",
            f"/api/v0/user/{self.user}/webapps/{self.domain_name}/static_headers/",
            return_json=True,
        )

    async def get_static_header_by_id(self, id_: int) -> StaticHeader:
        """Get a static header by it's id."""
        resp = await self._user.request(
            "GET",
            f"/api/v0/user/{self.user}/webapps/{self.domain_name}/static_headers/{id_}/",
            return_json=True,
        )
        return StaticHeader(resp, self)

    async def create_static_header(
        self, url: str, name: str, value: dict
    ) -> StaticHeader:
        """
        Create a static header for the webapp. Webapp reload required.

        Args:
            url (str): url for the static header
            name (str): name of the static header
            value (dict): value(s) for the header

        Returns:
            StaticHeader
        """
        data = {"url": url, "name": name, "value": value}
        resp = await self._user.request(
            "POST",
            f"/api/v0/user/{self.user}/webapps/{self.domain_name}/static_headers/",
            return_json=True,
            data=data,
        )
        return StaticHeader(resp, self)

    @property
    def userclass(self):
        """Property for accessing pyaww.User"""
        return self._user

    def __str__(self):
        return self.domain_name

    def __eq__(self, other):
        return self.domain_name == other.domain_name
