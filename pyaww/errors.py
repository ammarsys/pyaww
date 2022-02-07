# Standard library imports

from datetime import datetime
from typing import NoReturn

from .utils.limiter import Route


class PythonAnywhereError(Exception):
    """A base exception, nothing special to it, used everywhere."""


class InvalidInfo(PythonAnywhereError):
    """Exception for handling invalid tokens."""

    def __init__(self, message: str, code: int) -> None:
        super().__init__(message)
        self.code = code


class NotFound(InvalidInfo):
    """Exception for handling 404's."""

class RouteLimit(InvalidInfo):
    """Exception for handling 429 rate limiter errors for when user has made too many requests to a route"""

class ConsoleLimit(InvalidInfo):
    """Exception for handling 429's raised by having more then 2 consoles on a free plan"""


ERRORS_DICT: dict[tuple[int, str], PythonAnywhereError] = {
    (401, "Invalid token."): InvalidInfo(
        "Bad token provided, please check it at https://www.pythonanywhere.com/account/#api_token",
        401,
    ),
    (404, "Not found."): NotFound("Not found.", 404),
    (429, "Console limit reached."): ConsoleLimit("Console limit reached.", 429),
}

def raise_limit_error_and_await(route: Route) -> NoReturn:
    """Raise the Route Limit error with its corresponding url message"""
    await_for = int(route.sleep_until().timestamp() - datetime.now().timestamp())
    raise RouteLimit("limit reached for route " + route.url + " please retry after " + str(await_for) + " seconds", 429)

def raise_error(data: tuple[int, str]) -> NoReturn:
    """
    Raise an appropriate error based on the response

    Args:
        data (tuple[Any]): data for the error
    """

    if data in ERRORS_DICT:
        raise ERRORS_DICT[data]

    raise PythonAnywhereError(data[1])
