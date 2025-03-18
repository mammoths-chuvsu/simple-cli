# simple-cli

Homework #2 for the course "Software Development". A simple CLI interpreter that supports several UNIX commands.

## Installation

To install the project, you need to have [Poetry](https://python-poetry.org/docs/#installation) installed on your machine.

### For Regular Users

1. Install the dependencies:
```bash
poetry install
```

### For Developers
If you are planning to develop or contribute to this project, install the development dependencies as well:

Install all dependencies including those needed for development:

```bash
poetry install --with=dev
```

Set up pre-commit hooks:

```bash
poetry run pre-commit install
```


## Features
- Supports `cat` to display file contents.
- `echo` to print arguments to the screen.
- `wc` to count lines, words, and bytes in a file.
- `pwd` to print the current directory.
- `exit` to terminate the interpreter.
Anything unknown is passed to an external program.
