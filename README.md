# pyanywhere-wrapper

An API wrapper around the pythonanywhere's API.

- 100% api coverage
- most of the codebase is documented & typehinted
- maintained

![Open Source? Yes!](https://badgen.net/badge/Open%20Source%20%3F/Yes%21/blue?icon=github)

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
# Quick-start

```py
# import the module
from pyanywhere import User

# construct the user class
client = User(auth='...', username='...')

# sample code
for console in client.consoles():
    print(console.name)
```

Please look at the documentations: https://ammarsys.github.io/pyanywhere-wrapper-docs/

# Installation

```py
# Linux/MacOS
python3 -m pip install pyanywhere-wrapper

# Windows
py -m pip install pyanywhere-wrapper
```

For the dev version, do:
```
git clone https://github.com/ammarsys/pyanywhere-wrapper
cd pyanywhere-wrapper
```
# How to get API a token?

Head over to https://www.pythonanywhere.com/account/#api_token, and you should be able to find it.
