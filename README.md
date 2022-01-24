<div align="center">

![image](https://i.imgur.com/jXVDRs6.png)

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://badge.fury.io/py/pyaww.svg)](https://badge.fury.io/py/pyaww)
[![Code Size](https://img.shields.io/github/languages/code-size/ammarsys/pyaww)](https://img.shields.io/github/languages/code-size/ammarsys/pyaww)
</div>
<hr>

# Overview

An API wrapper around the PythonAnywhere's API. The name stands for `py`thon`a`ny`w`here`w`rapper. The key-features are,

- Modern API wrapper using the `async` / `await` syntax
- 100% API coverage, 100% tested
- Object-oriented
- Fully documented & Typehinted
- Caching handled

We strive to provide an easy-to-use, batteries included modern API wrapper. The documentation can be found [here](https://pyaww-docs.vercel.app/), 
for help please open an [issue](https://github.com/ammarsys/pyaww/issues).

# Installation

> The required Python version for the module is `3.9` or above.

```
# Linux/MacOS
python3 -m pip install pyaww==1.0.0

# Windows
py -m pip install pyaww==1.0.0
```

# Quick Example

To use this module, you first have to create an API key over [here](https://www.pythonanywhere.com/account/#api_token). 
After you've done that, copy the credentials and provide them to the `pyaww.User` class. It is advised that you do 
*not* make your token public within the code, instead, you should store it [securely](https://stackoverflow.com/questions/41546883/what-is-the-use-of-python-dotenv) 
using a package like `python-dotenv`.

This module is asynchronous meaning it utilises the `async` / `await` syntax.

```py
import pyaww
import asyncio

# construct the user class
client = pyaww.User("sexychad420", "my-python-anywhere-token")

async def cpu() -> dict:
    """Gets the CPU information."""
    return await client.get_cpu_info()

asyncio.run(cpu())
```

Using this module within PythonAnywhere webapps might be a little tricky as they only support WSGI at the moment.
However, you can run the function calls synchronously with `asyncio` module if your desired web framework doesn't 
support async syntax. Some back-end frameworks such as `flask` 
[support](https://flask.palletsprojects.com/en/2.0.x/async-await/) async syntax in the routes, example:
```py
from flask import Flask
import pyaww

app = Flask(__name__)
client = pyaww.User("sexychad420", "my-python-anywhere-token")

@app.route("/")
async def cpu_usage():
    return await client.get_cpu_info()

if __name__ == '__main__':
    app.run()
```

If there is no way that you can use the `async/await` syntax within your webapp, you can downgrade to `>3.0.0` versions
of this module.
