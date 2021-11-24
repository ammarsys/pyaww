"""Helper functions for the API wrapper"""

# Standard library imports

from typing import Any, Iterator


def flatten(items: Any) -> Iterator:
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
            yield from flatten(i)
    except TypeError:
        yield items
