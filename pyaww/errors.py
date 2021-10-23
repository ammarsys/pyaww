"""Errors for the module"""

# Standard library imports

from typing import Any, Dict, NoReturn, Tuple


class PythonAnywhereError(Exception):
    """A base exception, nothing special to it, used everywhere."""


class InvalidInfo(PythonAnywhereError):
    """Exception for handling invalid tokens."""

    def __init__(self, message: str, code: int) -> None:
        super().__init__(message)
        self.code = code


class NotFound(InvalidInfo):
    """Exception for handling 404's."""


ERRORS_DICT: Dict[Tuple[int, str], PythonAnywhereError] = {
    (401, "Invalid token."): InvalidInfo(
        "Bad token provided, please check it at https://www.pythonanywhere.com/account/#api_token",
        401,
    ),
    (404, "Not found."): NotFound("Not found.", 404),
}


def raise_error(data: Tuple[int, str]) -> NoReturn:
    """
    Raise an appropriate error based on the response

    Args:
        data (tuple[Any]): data for the error
    """

    if data in ERRORS_DICT:
        raise ERRORS_DICT[data]

    raise PythonAnywhereError(data[1])
