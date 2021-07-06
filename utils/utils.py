from typing import Any, Iterator

def flatten(items: Any) -> Iterator:
    """
    A function to "completely" flatten a list. For example, itertools.chain() would flatten it once but with recursion
    this function flattens it completely til it's a list with no nested lists.

    :param Any items: items to be flattened
    :return: Iterator with flattened items (nothing nested)
    """
    try:
        if isinstance(items, str): raise TypeError

        for i in items:
            yield from flatten(i)
    except TypeError:
        yield items