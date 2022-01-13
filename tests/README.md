This module uses the `pytest` library for its tests. Alongside the bare library, the following plugins for it are used:

- `pytest-asyncio`

as well as `python-dovenv` for API credentials. 

### Structure explained

For the configuration, rendering credentials and creating fixtures `conftest.py` is used.

The structure is divided into three parts,

- `.py` files in the tests directory are usually configuration
and/or tests of the main class (`pyaww.User`)
- `assets/` directory is used for anything that the tests need in order to run (e.g. credentials, data...)
- `submodules/` tests for any instances that constructors return (usually in `conftest.py`)

Submodules directory exists for the ease of cleanup.

### Sample test

```python
@pytest.mark.asyncio
async def test_x(y_fixture: Y) -> None:
    assert isinstance(await y_fixture.do_stuff(), Y)
```

### Testing caching & ratelimiting

Caching and ratelimit tests are both given a seperate test file for their main functionaly 
(e.g. testing TTL cache class) but the actual testing of whether a method caches or not, is done in either said so
method or in their corresponding fixture.