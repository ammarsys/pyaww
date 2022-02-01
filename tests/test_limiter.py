from pyaww.utils import limiter
from pyaww import errors

import pytest

@pytest.mark.asyncio
async def test_limiter(client: "User") -> None:
    for i in range(49):
        limiter.limiter("/test")
    with pytest.raises(errors.ConsoleLimit):
        limiter.limiter("/test")