# simple-cli

Homework #2 for the course "Software Development". A simple CLI interpreter that supports several UNIX commands.

## Installation

To install the project, you need to have [Poetry](https://python-poetry.org/docs/#installation) installed on your machine.

### For Regular Users

1. Install the dependencies:
```bash
poetry install
```
2. Run interpretator:
```bash
$(poetry env activate)
python simple_cli/main.py
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

## Why `argparse`?

We chose `argparse` for parsing command-line arguments, and here are a few reasons why:

- **Built-in with Python**: `argparse` comes with Python, so you don't need to install anything extra. This reduces dependencies and simplifies the deployment of the application.

- **Comprehensive functionality**: This library handles arguments and options, generates automatic help messages —
 everything we need for our project without additional complexities.

- **Widely used and well-documented**: There is a lot of information and examples on `argparse`, making it a reliable choice if you encounter any questions.

### Considered Alternatives

We also considered `click` and `typer`, but decided they were not as suitable for our project. Here's why:

- **Click**: While it offers a convenient interface for creating commands, it requires installing an additional package. This adds another dependency to consider if we want to keep the project lightweight and easy to install.

- **Typer**: Built on `click`, it offers great features with type annotations, making the code more modern and structured. However, for our needs, this is excessive; we don't use type annotations extensively enough for it to be an advantage. Also, like `click`, it adds a dependency.

Ultimately, `argparse` became the best choice for us because it is simple, built-in, and has enough powerful features to meet all our needs.