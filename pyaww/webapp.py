from typing import TYPE_CHECKING, List

from .static_file import StaticFile
from .static_header import StaticHeader

if TYPE_CHECKING:
    from .user import User


class WebApp:
    """Contains all methods of a webapp."""
    id: int
    user: str
    domain_name: str
    python_version: str
    source_directory: str
    working_directory: str
    virualenv_path: str
    expiry: str
    force_https: bool

    def __init__(self, resp: dict, user: 'User') -> None:
        """
        Initialize the class variables.

        :param dict resp: json dictionary
        :param user: User class see (pyaww.user)
        """
        self._user = user
        vars(self).update(resp)

    def delete(self) -> None:
        """Deletes a webapp."""
        self._user.request('DELETE', f'/api/v0/user/{self.user}/webapps/{self.domain_name}/')

    def update(self, **kwargs) -> None:
        """
        Updates config of a webapp. Restart required.

        Sample usage -> Webapp.update(python_version='3.7', force_https=False)

        :param kwargs: can take: python_version, source_directory, virtualenv_path, force_https
        """
        self._user.request('PATCH', f'/api/v0/user/{self.user}/webapps/{self.domain_name}/', data=kwargs)
        vars(self).update(kwargs)

    def reload(self) -> None:
        """Reloads a webapp."""
        self._user.request('POST', f'/api/v0/user/{self.user}/webapps/{self.domain_name}/reload/')

    def disable(self) -> None:
        """Disables a webapp."""
        self._user.request('POST', f'/api/v0/user/{self.user}/webapps/{self.domain_name}/disable/')

    def enable(self) -> None:
        """Enables a webapp."""
        try:
            self._user.request('POST', f'/api/v0/user/{self.user}/webapps/{self.domain_name}/enable/')
        except:
            pass

    def get_ssl_info(self) -> dict:
        """
        Gets TLS/HTTP info of the webapp.

        :return: json dictionary
        """
        return self._user.request('GET', f'/api/v0/user/{self.user}/webapps/{self.domain_name}/ssl/').json()

    def set_ssl_info(self, cert: str, private_key: str) -> None:
        """
        Set the TLS/HTTP info. Webapp restart required.

        Sample usage -> Webapp.set_ssl_info(cert=..., private_key=...)

        :param str cert: TLS/HTTP certificate
        :param str private_key: TLS/HTTP private key
        """
        data = {'cert': cert, 'private_key': private_key}
        return self._user.request('POST', f'/api/v0/user/{self.user}/webapps/{self.domain_name}/ssl/', data=data).json()

    def static_files(self) -> List[StaticFile]:
        """
        Gets webapps static files.

        :return: list of static files (see pyanywhere.static_file)
        """

        resp = self._user.request('GET', f'/api/v0/user/{self.user}/webapps/{self.domain_name}/static_files/').json()
        return [StaticFile(i, self) for i in resp]

    def create_static_file(self, file_path: str, url: str = None) -> StaticFile:
        """
        Create a static file. Static files can be loaded much faster of disk. Webapp restart required.

        Sample usage -> Webapp.create_static_file('/home/yourname/mysite/verify.html', '/static/verify.html')

        :param str file_path: path of the file
        :param str url: URL that should lead to the static file.
        :return: a static file (see pyanywhere.static_file)
        """
        data = {'path': file_path, 'url': url}
        resp = self._user.request('POST', f'/api/v0/user/{self.user}/webapps/{self.domain_name}/static_files/',
                                  data=data).json()

        return StaticFile(resp, self)

    def get_static_file_by_id(self, id: int) -> StaticFile:
        """
        Get a static file via it's id.

        :param int id: ID of the static file
        :return: a static file (see pyanywhere.static_file)
        """
        resp = self._user.request('GET',
                                  f'/api/v0/user/{self.user}/webapps/{self.domain_name}/static_files/{id}/').json()
        return StaticFile(resp, self)

    def static_headers(self) -> List[dict]:
        """Get webapps static headers."""
        resp = self._user.request('GET', f'/api/v0/user/{self.user}/webapps/{self.domain_name}/static_headers/').json()
        return resp

    def get_static_header_by_id(self, id: int) -> StaticFile:
        """Get a static header by it's id."""
        resp = self._user.request('GET',
                                  f'/api/v0/user/{self.user}/webapps/{self.domain_name}/static_headers/{id}/').json()
        return StaticHeader(resp, self)

    def create_static_header(self, url: str, name: str, value: dict) -> StaticHeader:
        """
        Create a static header for the webapp. Webapp restart required.

        Sample usage -> Webapp.create_static_header(...)

        :param str url: url for the static header
        :param str name: name of the static header
        :param dict value: value(s) for the header
        :return: a static header (see pyanywhere.static_file)
        """
        data = {'url': url, 'name': name, 'value': value}
        resp = self._user.request(
            'POST', f'/api/v0/user/{self.user}/webapps/{self.domain_name}/static_headers/',
            data=data
        )
        return StaticHeader(resp.json(), self)

    @property
    def userclass(self):
        return self._user

    def __str__(self):
        return self.domain_name
