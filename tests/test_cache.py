# Standard library imports

import time

# Related third party imports

import pytest

# Local application/library specific imports

from pyaww import User, cache_func


@cache_func(seconds=1, max_len=5)
async def hello(client: User, name: str = "Maria") -> str:
    client.helloed = name
    return "Hello " + name


@pytest.mark.asyncio
async def test_caches(client: User) -> None:
    await hello(client, "John")
    await hello(client, name="Bob")
    await hello(client)

    cache = client.cache["hello"].cache
    params = [(client, "John"), (client, "Bob"), (client, "Maria")]

    assert all(k in params for k, v in cache.items())

    # Just checking the dunder methods... gotta be sure
    client.cache["hello"].__getitem__(params[0]),
    client.cache["hello"].__contains__(params[0])

    client.cache = {}


@pytest.mark.asyncio
async def test_TTL_getitem(client: User) -> None:
    await hello(client, "Martin")
    params = (client, "Martin")

    assert params in client.cache["hello"].cache
    time.sleep(1)

    with pytest.raises(KeyError):
        client.cache["hello"].__getitem__(params)

    client.cache = {}


@pytest.mark.asyncio
async def test_TTL_contains(client: User) -> None:
    await hello(client, "Martin")
    params = (client, "Martin")

    assert params in client.cache["hello"].cache
    time.sleep(1)

    assert not (params in client.cache["hello"])

    client.cache = {}


@pytest.mark.asyncio
async def test_returns_cached_output(client: User) -> None:
    await hello(client, "David")
    assert client.helloed == "David"

    client.helloed = ""

    await hello(client, "David")
    assert client.helloed == ""

    client.cache = {}


@pytest.mark.asyncio
async def test_max_len(client: User) -> None:
    await hello(client, "Mark")
    await hello(client, "Sebastian")
    await hello(client, "John")
    await hello(client, "Jake")
    await hello(client, "Emma")

    assert len(client.cache["hello"]) == 5

    await hello(client, "Jenny")

    assert (
        not ((client, "Mark") in client.cache["hello"])
        and len(client.cache["hello"]) == 5
    )
