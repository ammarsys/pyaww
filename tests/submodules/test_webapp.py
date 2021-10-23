# Local application/library specific imports

from pyaww.user import WebApp, User


def test_get_webapp_by_domain(client: User, webapp: WebApp) -> None:
    assert client.get_webapp_by_domain_name(webapp.domain_name) == webapp


def test_delete(webapp: WebApp) -> None:
    assert webapp.delete() is None
