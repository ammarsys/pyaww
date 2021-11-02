<div align="center">

![image](https://i.imgur.com/jXVDRs6.png)

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://badge.fury.io/py/pyaww.svg)](https://badge.fury.io/py/pyaww)
[![Code Size](https://img.shields.io/github/languages/code-size/ammarsys/pyaww)](https://img.shields.io/github/languages/code-size/ammarsys/pyaww)
</div>

<hr>

# Overview

A lightweight API wrapper around the PythonAnywhere's API. The name stands for `py`thon`a`ny`w`here`w`rapper.

- 100% API coverage
- Object-oriented
- Fully documented & Typehinted
- Caching & Ratelimiting handled
- 100% tested

The documentation can be found [here](https://pyaww-docs.vercel.app/).

# Quick-start

The required Python version for this module is `3.9` or above. This is as of `0.0.4`, versions below support `3.6+`.


```py
# Linux/MacOS
python3 -m pip install pyaww

# Windows
py -m pip install pyaww
```

For the development version do,
```
git clone https://github.com/ammarsys/pyaww/tree/dev
cd pyaww
```

Mini example,

```py
# import the module
from pyaww.user import User

# construct the user class
client = User(auth='...', username='...')

for console in client.consoles():
    print(console.name)
```

There are more examples in the `repices` directory.

<div align="center">

# Frequently Asked Questions

</div>

**Q: How do I get my accounts API token?**

**A:** Head over to https://www.pythonanywhere.com/account/#api_token, and you should be able to find it.

<hr>

**Q: I have an issue, where can I receive help?**

**A:** Please open an issue over [here](https://github.com/ammarsys/pyaww/issues).

<hr>

**Q: How do I contribute?**

**A:** We have a guide for that, please see `CONTRIBUTING.MD` in this repository.

<hr>

**Q: How to use this module in an async environment?**

**A:** Look into [this](https://pypi.org/project/aioify/) library.

<hr>


**Q: How to manually construct a class?**

We know that the class variables for a console (taken from the docs) are:

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
}, user=User(...)) # and the other stuff
```
