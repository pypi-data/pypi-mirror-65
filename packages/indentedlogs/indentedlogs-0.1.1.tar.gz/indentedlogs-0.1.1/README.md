# indentedlogs

Adds indentation to the log messages according to their location in the call stack.

* Documentation: <https://gergelyk.github.io/python-indentedlogs>
* Repository: <https://github.com/gergelyk/python-indentedlogs>
* Package: <https://pypi.python.org/pypi/indentedlogs>
* Author: [grzegorz.krason@gmail.com](mailto:grzegorz.krason@gmail.com)
* License: [MIT](LICENSE)

## Requirements

This package requires CPython 3.8 or compatible. If you have other version already installed, you can switch using `pyenv`. It must be installed as described in the [manual](https://github.com/pyenv/pyenv).

```sh
pyenv install 3.8.2
pyenv local 3.8.2
```

## Installation

```sh
pip install indentedlogs
```

## Examples

```sh
python examples/demo0.py
python examples/demo1.py
python examples/demo2.py
```

## Development

```sh
# Preparing environment
pip install --user poetry  # unless already installed
poetry install

# Auto-formatting
poetry run docformatter -ri indentedlogs tests
poetry run isort -rc indentedlogs tests
poetry run yapf -r -i indentedlogs tests

# Checking coding style
poetry run flake8 indentedlogs tests

# Checking composition and quality
poetry run mypy indentedlogs tests
poetry run pylint indentedlogs tests
poetry run bandit indentedlogs tests
poetry run radon cc indentedlogs tests
poetry run radon mi indentedlogs tests

# Testing with coverage
poetry run pytest --cov indentedlogs --cov tests

# Rendering documentation
poetry run mkdocs serve

# Building package
poetry build

# Releasing
poetry version minor  # increment selected component
git tag ${$(poetry version)[2]}
git push --tags
poetry build
poetry publish
poetry run mkdocs build
poetry run mkdocs gh-deploy -b gh-pages
```

## Donations

If you find this software useful and you would like to repay author's efforts you are welcome to use following button:

[![Donate](https://www.paypalobjects.com/en_US/PL/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=D9KUJD9LTKJY8&source=url)
