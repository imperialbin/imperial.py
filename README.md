# imperial-py

> [imperialbin](https://imperialb.in) is a code/text sharing site with the user experience in mind, it has feautures such as editing, encryption and integration with github gists and discord.

[![BUILT WITH SWAG](https://forthebadge.com/images/badges/built-with-swag.svg)](https://forthebadge.com)
[![MADE WITH PYTHON](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)
[![FIXED BUGS](https://forthebadge.com/images/badges/fixed-bugs.svg)](https://forthebadge.com)

## API Token

An API Token is not required, but you can't do most things without one. Add `IMPERIAL_TOKEN` to path to set it
automatically; this will get overwritten by setting one manually.

## Example Usage

Shorthand Functions are more optimal if you have your API token set as an environmental variable.

### Shorthand Functions

```python
import imperial_py

document = imperial_py.create_document("Hello, World!")
# document.content is "Hello, World!"
document.edit("Hello from Python!")
# document.content is "Hello from Python!"
document.delete()
# document is deleted off imperial servers,
# but information about the document still lives in the object
document.edit("This will raise an error!")
# imperial_py.exceptions.DocumentNotFound("We couldn't find that document!")
```

### Imperial Class

```python
from imperial_py import Imperial

imp = Imperial("IMPERIAL-00000000-0000-0000-0000-000000000000")
document = imp.create_document("Hello, World!")
# etc...
```

# Documentation

Refer to [imperial documentation](https://docs.imperialb.in) for full docs.<br/>To see what goes on with imperial-py,
view the full code. All important functions have docstrings and a description.

# Contributing

1. Fork the repo on GitHub
2. Clone the project to your own machine
3. Commit changes to your own branch
4. Push your work to your fork
5. Submit a Pull request so that I can review your changes
