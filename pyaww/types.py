# Standard library imports

import datetime

from typing import Any, TYPE_CHECKING

# Local application/library specific imports

if TYPE_CHECKING:
    from .user import User

cache_type = dict[str, dict[tuple["User", Any], tuple[datetime.datetime, Any]]]
