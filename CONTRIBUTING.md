# Contributing to pyaww

First, thanks for taking the time to contribute! ❤️ All contributions are welcomed and encouraged.

## Contributing

1. [Create an issue and assign it to yourself](https://github.com/ammarsys/pyaww/issues).
2. Fork the repository.
3. Locally clone your fork,

```
git clone https://github.com/yourname/pyaww
cd pyaww
```

4. Commit your changes, 

```
git add pyaww/user.py
git commit -m "[feat] add support for x in method y"
```

Please look at the [following](https://gist.github.com/qoomon/5dfcdf8eec66a051ecd85625518cfd13) git guide for commits.

5. Push your changes `git push -u origin branch`.
6. [Create a PR](https://github.com/ammarsys/pyaww/issues/pulls),
with a good description on the changes you've made.

## General Guidelines

- Follow the `PEP8` rules.
- Use [Google-style](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html) docstrings.
- You must format your code using [black](https://pypi.org/project/black/).
- You must sort imports using [isort](https://pypi.org/project/isort/).
- You must run tests using [pytest](https://pypi.org/project/pytest/) before creating a pull request.
- Your code must be typehinted. Look into `pyright` or `pylance` type checkers if you do not have one.
- Write clean and efficient code.

## How to run the tests?

1. Install the `pytest` and the `python-dotenv` library.
2. Navigate to `pyaww/tests/assets` and create `.env`. It should contain:
```dotenv
USERNAME=USERNAME
AUTH=TOKEN
STARTED_CONSOLE=ID
```

To properly test the module, use a "fresh account". Just create an alternative account, make & start a console and 
you're good to go!

3. Ensure your CWD is `pyaww` and not `pyaww/tests` or similar.
4. Run `py -m pytest -v -s`.
5. Fix if anything is wrong, if not, your tests are fine.

## What is currently our TODO for 0.0.4 version?

#### Making the documentations good.
- ~~The automatically ...~~


### Better caching
- ~~TTL cache ...~~ 
- Thread safe caching with `threading.RLock`
- Caching methods outside `pyaww.User`, specifically the submodules
- an `update_cache` function that updates the cache. A MVP would probably accept string-like options, 
`WIPE`, `ADD_TO_CACHE`, etc. The `WIPE` option for example would be a value for a parameter in a decorator, 
sample use-case is, 
```py
@cache_func
def consoles() -> list:
    ...

@update_cache(func='User.get_console_by_id', mode='ADD_TO_CACHE', identifier="RETURN")
def create_console(...) -> Console:
    """Once a console is created, it'll be added to the cache of User.consoles."""
    ...
```
or if you can propose a better idea.

### Ratelimiting
- 40/minute for everything except console inputs where it is 120/min
- decorator style