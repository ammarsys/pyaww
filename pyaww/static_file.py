from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .webapp import WebApp


class StaticFile:
    """A static file is a file that can be served much faster of disk. Accesed via URL."""
    id: int
    url: str
    path: str

    def __init__(self, resp: dict, webapp: 'WebApp'):
        """
        Initialize class variables.

        :param dict resp: json dictionary
        :param webapp: webapp class (see pyaww.webapp)
        """
        self._webapp = webapp
        vars(self).update(resp)

    def delete(self) -> None:
        """Delete a static file."""
        self._webapp.userclass.request(
            'DELETE',
            f'/api/v0/user/{self._webapp.user}/webapps/{self._webapp.domain_name}/static_files/{self.id}/'
        )

    def update(self, **kwargs) -> None:
        """
        Update a static file.

        Sample usage -> StaticFile.update(url='/static/myfile.html')

        :param kwargs: can take url, path
        """
        self._webapp.userclass.request(
            'PATCH',
            f'/api/v0/user/{self._webapp.user}/webapps/{self._webapp.domain_name}/static_files/{self.id}/',
            data=kwargs
        )
        vars(self).update(kwargs)

    def __str__(self):
        return self.url
