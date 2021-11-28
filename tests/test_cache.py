# Standard library imports

import time

# Related third party imports

import pytest

# Local application/library specific imports

from pyaww import User, cache_func


@cache_func(seconds=1, max_len=5)
def hello(client: User, name: str = "Maria") -> str:
    client.helloed = name
    return "Hello " + name


def test_caches(client: User) -> None:
    hello(client, "John")
    hello(client, name="Bob")
    hello(client)

    cache = client.cache["hello"].cache
    params = [(client, "John"), (client, "Bob"), (client, "Maria")]

    assert all(k in params for k, v in cache.items())

    # Just checking the dunder methods... gotta be sure
    client.cache["hello"].__getitem__(params[0]),
    client.cache["hello"].__contains__(params[0])

    client.cache = {}


def test_TTL_getitem(client: User) -> None:
    hello(client, "Martin")
    params = (client, "Martin")

    assert params in client.cache["hello"].cache
    time.sleep(1)

    with pytest.raises(KeyError):
        client.cache["hello"].__getitem__(params)

    client.cache = {}


def test_TTL_contains(client: User) -> None:
    hello(client, "Martin")
    params = (client, "Martin")

    assert params in client.cache["hello"].cache
    time.sleep(1)

    assert not (params in client.cache["hello"])

    client.cache = {}


def test_returns_cached_output(client: User) -> None:
    hello(client, "David")
    assert client.helloed == "David"

    client.helloed = ""

    hello(client, "David")
    assert client.helloed == ""

    client.cache = {}


def test_max_len(client: User) -> None:
    hello(client, "Mark")
    hello(client, "Sebastian")
    hello(client, "John")
    hello(client, "Jake")
    hello(client, "Emma")

    assert len(client.cache["hello"]) == 5

    hello(client, "Jenny")

    assert (
        not ((client, "Mark") in client.cache["hello"])
        and len(client.cache["hello"]) == 5
    )
