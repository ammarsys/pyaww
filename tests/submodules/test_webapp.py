# Local application/library specific imports

from pyaww import WebApp, User, StaticFile, StaticHeader


# No seperate files for static files and headers to simplify cleanup.


def test_get_static_file_by_id(static_file: StaticFile, webapp: WebApp) -> None:
    assert webapp.get_static_file_by_id(static_file.id) == static_file


def test_static_file_update(static_file: StaticFile, webapp: WebApp) -> None:
    static_file.update(url="PYAWW TESTING")
    webapp.restart()
    assert static_file.url == "PYAWW TESTING"


def test_static_file_delete(static_file: StaticFile) -> None:
    assert static_file.delete() is None


def test_get_static_header_by_id(static_header: StaticHeader, webapp: WebApp) -> None:
    assert webapp.get_static_header_by_id(static_header.id) == static_header


def test_static_header_update(static_header: StaticHeader, webapp: WebApp) -> None:
    static_header.update(url="PYAWW TESTING")
    webapp.restart()
    assert static_header.url == "PYAWW TESTING"


def test_static_header_delete(static_header: StaticHeader) -> None:
    assert static_header.delete() is None


def test_get_webapp_by_domain(client: User, webapp: WebApp) -> None:
    assert client.get_webapp_by_domain_name(webapp.domain_name) == webapp


def test_update(webapp: WebApp) -> None:
    webapp.update(python_version=3.8)
    assert webapp.python_version == 3.8


def test_disable(webapp: WebApp) -> None:
    assert webapp.disable() is None


def test_enable(webapp: WebApp) -> None:
    assert webapp.enable() is None


def test_get_ssl_info(webapp: WebApp) -> None:
    assert isinstance(webapp.get_ssl_info(), dict)


def test_set_ssl_info(webapp: WebApp) -> None:
    assert webapp.set_ssl_info(cert="PYAWWTEST", private_key="PYAWWTEST") is None


def test_reload(webapp: WebApp) -> None:
    assert webapp.restart() is None


def test_static_headers(webapp: WebApp) -> None:
    assert isinstance(webapp.static_headers(), list)


def test_static_files(webapp: WebApp) -> None:
    assert isinstance(webapp.static_files(), list)


def test_delete(webapp: WebApp) -> None:
    assert webapp.delete() is None
