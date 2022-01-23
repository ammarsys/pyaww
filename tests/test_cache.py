# Standard library imports

import copy
from typing import NoReturn

# Related third party imports

import pytest

# Local application/library specific imports

from pyaww import User


async def mock_request_func(*args, **kwargs) -> NoReturn:
    raise NotImplementedError("request function not implemented")


class MockUser(User):
    pass


@pytest.mark.asyncio
async def test_disable_cache_methods(client: "User") -> None:
    client_seperate = copy.copy(client)
    original = client_seperate.request

    client_seperate.cache.use_cache = False
    client_seperate.cache._console_cache.cache = {}

    client_seperate.request = mock_request_func  # type: ignore

    with pytest.raises(NotImplementedError):
        await client_seperate.consoles()

    client_seperate.request = original  # type: ignore
    consoles = await client_seperate.consoles()  # populate the cache
    client_seperate.request = mock_request_func  # type: ignore

    client_seperate.cache.disable_cache_for_identifier.add(consoles[0].id)

    with pytest.raises(NotImplementedError):
        await client_seperate.get_console_by_id(consoles[0].id)

    client_seperate.cache.disable_cache_for_identifier = set()
    client_seperate.cache.disable_cache_for_module.add("console")

    with pytest.raises(NotImplementedError):
        await client_seperate.consoles()
