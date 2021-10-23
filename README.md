# pyaww

![image](https://i.imgur.com/tWIb4cW.png)

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://badge.fury.io/py/pyaww.svg)](https://badge.fury.io/py/pyaww)

A lightweight API wrapper around PythonAnywhere's API. The name stands for `py`thon`a`ny`w`here`w`rapper.

- 100% API coverage
- Object-oriented
- Fully documented & Typehinted
- Caching & Ratelimiting handled

# Quick-start

```py
# import the module
from pyaww.user import User

# construct the user class
client = User(auth='...', username='...')

for console in client.consoles():
    print(console.name)
```

Documentations: https://ammarsys.github.io/pyaww-docs/

PyPi: https://pypi.org/project/pyaww
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
 - Please check out `CONTRIBUTING.MD`

### How to use this module in an async enviorment?
 - Look into [this](https://pypi.org/project/aioify/) library.

### Where are the documentations?
 - Over [here](https://ammarsys.github.io/pyaww-docs/).

### How to manually construct a class?

We know that the class variables for a console (taken from docs) are:

- id
- user
- executable
- arguments
- working_directory
- name
- console_url
- console_frame_url

So we can do:

```python
from pyaww.user import Console, User

console = Console(resp={
    'id': ..., 
    'user': ..., 
    'executable': ...
}, user=User(...))  # goes on
```
