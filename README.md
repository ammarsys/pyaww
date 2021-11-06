<div align="center">

![image](https://i.imgur.com/jXVDRs6.png)

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://badge.fury.io/py/pyaww.svg)](https://badge.fury.io/py/pyaww)
[![Code Size](https://img.shields.io/github/languages/code-size/ammarsys/pyaww)](https://img.shields.io/github/languages/code-size/ammarsys/pyaww)
</div>
<hr>

# Overview

An API wrapper around the PythonAnywhere's API. The name stands for `py`thon`a`ny`w`here`w`rapper. The key-feautures are,

- 100% API coverage, 100% tested
- Object-oriented
- Fully documented & Typehinted
- Caching & Ratelimiting handled

We strive to provide an easy to use, batteries included, modernic API wrapper. The documentation can be found [here](https://pyaww-docs.vercel.app/), 
for help please open an [issue](https://github.com/ammarsys/pyaww/issues).

# Installation

> The required Python version for the module is `3.9` or above.

```
# Linux/MacOS
python3 -m pip install pyaww

# Windows
py -m pip install pyaww
```

# Quick Example

To use this module, you first have to create an API key over [here](https://www.pythonanywhere.com/account/#api_token). 
After you've done that, copy the credentials and provide them to the `pyaww.user.User` class. It is advised that you do 
*not* make your token public within the code, instead, you should store it [securely](https://stackoverflow.com/questions/41546883/what-is-the-use-of-python-dotenv) 
using a package like `python-dotenv`.
```py
from pyaww.user import User

# construct the user class
client: User = User(auth='TOKEN_GOES_HERE', username='USERNAME_GOES_HERE')

def cpu() -> dict:
    """Gets the CPU information."""
    return client.get_cpu_info()

print(cpu())
```
