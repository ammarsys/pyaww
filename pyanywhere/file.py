from io import TextIOWrapper

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User

class File:
    def __init__(self, path: str, user: 'User') -> None:
        """
        Initialize class variables.

        :param path: path of the file
        :param user: user class (see pyanywhere.user)
        """
        self.path = path
        self._user = user

    def share(self) -> str:
        """
        Function to start sharing a file.

        Sample usage -> File.share()

        :return: share url of the file
        """
        return self._user.request('POST',
                                  f'/api/v0/user/{self._user.username}/files/sharing/',
                                  data={'path': self.path}).json()['url']

    def unshare(self) -> None:
        """Function to stop sharing a file."""
        self._user.request('DELETE', f'/api/v0/user/{self._user.username}/files/sharing/?path={self.path}')

    def is_shared(self) -> bool:
        """Function to check sharing status of a file."""
        try:
            self._user.request('GET', f'/api/v0/user/{self._user.username}/files/sharing/?path={self.path}')
            return True
        except:
            return False

    def delete(self) -> None:
        """Delete the file."""
        self._user.request('DELETE', f'/api/v0/user/{self._user.username}/files/path/{self.path}')

    def read(self) -> bytes:
        """Read files contents. The contents are in bytes, call decode() on it. Sample usage -> File.read()"""
        return self._user.request('GET', f'/api/v0/user/{self._user.username}/files/path/{self.path}').content

    def update(self, content: TextIOWrapper) -> None:
        """
        Update a file.

        Sample usage
        --------------
        with open('newcontent.txt', 'r') as f:
            File.update(f)
        --------------

        :param TextIOWrapper content: content the file should be updated with, will create if doesn't exist.
        """
        self._user.create_file(self.path, content)

    def __str__(self):
        return self.path
