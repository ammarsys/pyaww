# Related third party imports

import pytest

# Local application/library specific imports

from pyaww import WebApp, User, StaticFile, StaticHeader


@pytest.mark.asyncio
async def test_get_static_file_by_id(static_file: StaticFile, webapp: WebApp) -> None:
    assert await webapp.get_static_file_by_id(static_file.id) == static_file


@pytest.mark.asyncio
async def test_static_file_update(static_file: StaticFile, webapp: WebApp) -> None:
    await static_file.update(url="PYAWW TESTING")
    await webapp.restart()
    assert static_file.url == "PYAWW TESTING"


@pytest.mark.asyncio
async def test_static_file_delete(static_file: StaticFile) -> None:
    assert await static_file.delete() is None


@pytest.mark.asyncio
async def test_get_static_header_by_id(static_header: StaticHeader, webapp: WebApp) -> None:
    assert await webapp.get_static_header_by_id(static_header.id) == static_header


@pytest.mark.asyncio
async def test_static_header_update(static_header: StaticHeader, webapp: WebApp) -> None:
    await static_header.update(url="PYAWW TESTING")
    await webapp.restart()
    assert static_header.url == "PYAWW TESTING"


@pytest.mark.asyncio
async def test_static_header_delete(static_header: StaticHeader) -> None:
    assert await static_header.delete() is None


@pytest.mark.asyncio
async def test_get_webapp_by_domain(client: User, webapp: WebApp) -> None:
    assert await client.get_webapp_by_domain_name(webapp.domain_name) == webapp


@pytest.mark.asyncio
async def test_update(webapp: WebApp) -> None:
    await webapp.update(python_version=3.8)
    assert webapp.python_version == 3.8


@pytest.mark.asyncio
async def test_disable(webapp: WebApp) -> None:
    assert await webapp.disable() is None


@pytest.mark.asyncio
async def test_enable(webapp: WebApp) -> None:
    assert await webapp.enable() is None


@pytest.mark.asyncio
async def test_get_ssl_info(webapp: WebApp) -> None:
    assert isinstance(await webapp.get_ssl_info(), dict)


@pytest.mark.asyncio
async def test_set_ssl_info(webapp: WebApp) -> None:
    assert await webapp.set_ssl_info(cert="PYAWWTEST", private_key="PYAWWTEST") is None


@pytest.mark.asyncio
async def test_reload(webapp: WebApp) -> None:
    assert await webapp.restart() is None


@pytest.mark.asyncio
async def test_static_headers(webapp: WebApp) -> None:
    assert isinstance(await webapp.static_headers(), list)


@pytest.mark.asyncio
async def test_static_files(webapp: WebApp) -> None:
    assert isinstance(await webapp.static_files(), list)


@pytest.mark.asyncio
async def test_delete(webapp: WebApp) -> None:
    assert await webapp.delete() is None
