# Contributing to pyaww

First, thanks for taking the time to contribute! ❤️ All contributions are welcomed and encouraged.

## Contributing

1. [Create issue and assign it to yourself](https://github.com/ammarsys/pyaww/issues)
2. Fork the repository or make a new branch
3. Make your changes.
4. [Create a PR](https://github.com/ammarsys/pyaww/issues/pulls)
   with a good description on the changes you've made.

## General Guidelines

- Follow `PEP8` rules
- Use [Google-style](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html) docstrings
- You should format your code using [black](https://pypi.org/project/black/) 
- You should sort imports using [isort](https://pypi.org/project/isort/) 
- You should run tests using [pytest](https://pypi.org/project/pytest/) before creating a pull request
- Your code must be typehinted. Look into `pyright` or `pylance` type checkers if you do not have one
- Write efficient and clean code

## How to run the tests?

- Install `pytest` library if you don't have it via `py -m pip install pytest`
- Navigate to `pyaww/tests/assets` and create `settings.json`. It should contain:
```json
{
  "USERNAME": "YOUR_NAME",
  "AUTH": "YOUR_TOKEN",
  "STARTED_CONSOLE": 123
}
```
- Ensure your CWD is `pyaww` and not `pyaww/tests` or similar
- Run `py -m pytest/tests`
- Fix if anything is wrong, if not, your tests are fine

## What is currently our TODO?
- Better caching, specifically, caching inside instances that `pyaww.user.User` returns.
- Ratelimit handling, 40/minute for everything exception being console inputs where it is 120/min.
