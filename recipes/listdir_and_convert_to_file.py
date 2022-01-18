from typing import AsyncIterator
import pyaww

client = pyaww.User('...', '...')


async def listpath(path: str) -> AsyncIterator:
    return client.listdir(path)
