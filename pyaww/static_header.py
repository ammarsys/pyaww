from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .webapp import WebApp


class StaticHeader:
    """Contains all relevant methods to a static header."""
    id: int
    url: str
    name: str
    value: dict

    def __init__(self, resp: dict, webapp: 'WebApp') -> None:
        """
        Initialize the class variables.

        :param dict resp: json dictionary
        :param webapp: WebApp class (see pyaww.webapp)
        """
        self._webapp = webapp
        vars(self).update(resp)

    def delete(self) -> None:
        """Delete a static header."""
        self._webapp.userclass.request(
            'DELETE',
            f'/api/v0/user/{self._webapp.user}/webapps/{self._webapp.domain_name}/static_headers/{self.id}/',
        )

    def update(self, **kwargs) -> None:
        """
        Update a static header.

        Sample usage -> StaticHeader.update(...)

        :param kwargs: takes url, name, value
        """
        print(kwargs, 'hello')
        self._webapp.userclass.request(
            'PATCH',
            f'/api/v0/user/{self._webapp.user}/webapps/{self._webapp.domain_name}/static_headers/{self.id}/',
            data=kwargs
        )
        vars(self).update(kwargs)
