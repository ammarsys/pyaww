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
(the tests/ directory)
- Your code must be typehinted. Look into `pyright` or `pylance` type checkers if you do not have one
- Write efficient and clean code

## What is currently our TODO?
- Better caching, specifically, caching inside instances that `pyaww.user.User` returns.
- Ratelimit handling, 40/minute for everything exception being console inputs where it is 120/min.
