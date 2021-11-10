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
git commit -m "[adds] Something!"
```

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

1. Install `pytest` library if you don't have it via `py -m pip install pytest`.
2. Navigate to `pyaww/tests/assets` and create `settings.json`. It should contain:
```json
{
  "USERNAME": "YOUR_NAME",
  "AUTH": "YOUR_TOKEN",
  "STARTED_CONSOLE": 123
}
```

To properly test the module, use a "fresh account". Just create an alternative account, make & start a console and 
you're good to go!

3. Ensure your CWD is `pyaww` and not `pyaww/tests` or similar.
4. Run `py -m pytest -v -s`.
5. Fix if anything is wrong, if not, your tests are fine.

## What is currently our TODO?

- Better caching, cache submodules, Thread safe caching...
- Ratelimit handling, 40/minute for everything except console inputs where it is 120/min.
- Making the `README.md` pretty.
- Making the documentations good.
