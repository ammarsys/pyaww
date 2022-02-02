import pytest

from pyaww.user import User
from pyaww.errors import ConsoleLimit

@pytest.mark.asyncio
async def test_limiter(client: User) -> None:
    for i in range(49):
        client.limiter("/test")
    with pytest.raises(ConsoleLimit):
        client.limiter("/test")