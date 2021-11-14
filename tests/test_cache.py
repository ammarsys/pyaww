# Standard library imports

import time

# Local application/library specific imports

from pyaww.user import User, cache_func


@cache_func(seconds=1)
def foo(client: User, name: str) -> str:  # client must be here
    return "Hello" + name + "!"


def test_caches(client: User) -> None:
    foo(client, "John")
    foo(client, name="Bob")

    assert (
        (foo.__qualname__, ((client, "John"), ())) in client.cache
        or not (foo.__qualname__, ((client,), (("name", "Bob"),))) in client.cache
    ), "Function was not cached."

    time.sleep(1)

    foo(client, "John")
    foo(client, name="Bob")

    assert not client.cache, "Cache is not empty."


def test_correct_output(client: User) -> None:
    original = foo(client, "Martin")

    assert (foo.__qualname__, ((client, "Martin"), ())) in client.cache, "Function was not cached."

    cached = foo(client, "Martin")

    assert original == cached
