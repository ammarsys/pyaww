# pyaww

An API wrapper around the pythonanywhere's API. The name stands for `py`thon`a`ny`w`here`w`rapper.

- 100% API coverage
- Most of the codebase is documented & typehinted
- Maintained

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
# Quick-start

```py
# import the module
from pyaww.user import User

# construct the user class
client = User(auth='...', username='...')

for console in client.consoles():
    print(console.name)
```

Please look at the documentations: https://ammarsys.github.io/pyaww-docs/

# Installation

```py
# Linux/MacOS
python3 -m pip install pyaww

# Windows
py -m pip install pyaww
```

For the dev version, do:
```
git clone https://github.com/ammarsys/pyaww
cd pyaww
```
# FAQ

### How do I get my accounts API token?
 - Head over to https://www.pythonanywhere.com/account/#api_token, and you should be able to find it.

### I have an issue, where can I recieve help?
 - Please open an issue over [here](https://github.com/ammarsys/pyaww/issues).

### Are there any examples?
 - Yes! See [this](https://github.com/ammarsys/pyaww/tree/main/recipes) directory.

### How do I contribute?
 - To make a code change, make a fork of this repository, edit it and make a pull request. Make sure to follow PEP8 and document your code.

### How to use this module in an async enviorment?
 - Look into [this](https://pypi.org/project/aioify/) library.

### Where are the documentations?
 - Over [here](https://ammarsys.github.io/pyaww-docs/).

### How to manually construct a class?
 - Import the class (such as pyaww.file) and pass following things File({...}, client). The dots inside the dictionary represent class variables.
