import pytest

from pyaww.user import User
from pyaww.errors import RouteLimit
from time import sleep

@pytest.mark.asyncio
async def test_limiter(client: User) -> None:
    normal_route = "/test"
    console_route = "/api/v0/user/user/consoles/1/send_input/"
    for _ in range(40):
        client.limiter(normal_route)
    for _ in range(120):
        client.limiter(console_route)
    #check that it raises an error now that we went over the limit
    with pytest.raises(RouteLimit):
        client.limiter(normal_route)
    with pytest.raises(RouteLimit):
        client.limiter(console_route)
    #wait until limiter resets
    sleep(60)
    client.limiter(normal_route)
    client.limiter(console_route)