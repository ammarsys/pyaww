import pytest

from pyaww.user import User
from pyaww.errors import RouteLimit
from time import sleep

@pytest.mark.asyncio
async def test_limiter(client: User) -> None:
    for _ in range(40):
        client.limiter("/test")
    #check that it raises an error now that we went over the limit
    with pytest.raises(RouteLimit, match='limit reached for route /test please retry after 60 seconds'):
        client.limiter("/test")
    #wait until limiter resets
    sleep(60)
    client.limiter("/test")