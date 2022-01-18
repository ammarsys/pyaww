"""Helper functions for the API wrapper"""

# Standard library imports

from typing import Any, AsyncIterator


async def flatten(items: Any) -> AsyncIterator:
    """
    A function to "completely" flatten a list. For example, itertools.chain() would flatten it once but with recursion
    this function flattens it completely til it's a list with no nested lists.

    Args:
        items (Any): items to be flattened

    Returns:
        Iterator: Iterator with flattened items (nothing nested)
    """
    try:
        if isinstance(items, str):
            raise TypeError

        for i in items:
            async for x in flatten(i):
                yield x
    except TypeError:
        yield items
