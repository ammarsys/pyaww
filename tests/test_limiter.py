from pyaww.utils import limiter
from pyaww import errors

import pytest

@pytest.mark.asyncio
async def test_limiter() -> None:
    for i in range(49):
        limiter.limiter("/test")
    with pytest.raises(errors.ConsoleLimit):
        await limiter.limiter("/test")