import pytest

from pyaww.user import User
from pyaww.errors import RouteLimit
from time import sleep

@pytest.mark.asyncio
async def test_limiter(client: User) -> None:
    for i in range(49):
        client.limiter("/test")
    with pytest.raises(RouteLimit, match='limit reached for route /test please retry after 60 seconds'):
        client.limiter("/test")
    sleep(60)
    assert isinstance(await client.limiter(), None)