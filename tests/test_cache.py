# Standard library imports

import time

# Local application/library specific imports

from pyaww.user import User, cache_func


@cache_func(seconds=1)
def hello(client: User, name: str = 'Maria') -> str:  # client must be here
    return "Hello " + name


def test_caches(client: User) -> None:
    hello(client, "John")
    hello(client, name="Bob")
    hello(client)

    assert (
        all(x in [(client, "John"), (client, "Bob"), (client, "Maria")] for x in client.cache[hello.__qualname__])
    ), "Function was not cached."

    time.sleep(1)

    hello(client, "John")
    hello(client, name="Bob")
    hello(client)

    assert not client.cache[hello.__qualname__], "Cache is empty."


def test_correct_output(client: User) -> None:
    original = hello(client, "Martin")

    assert (client, "Martin") in client.cache[hello.__qualname__]

    cached = hello(client, "Martin")

    assert original == cached


def test_global_settings(client: User) -> None:
    client.use_cache = False
    hello(client, "Jennifer")
    assert (client, "Jennifer") not in client.cache[hello.__qualname__]

    client.use_cache = True
    hello(client, "Jennifer")
    assert(client, "Jennifer") in client.cache[hello.__qualname__]
