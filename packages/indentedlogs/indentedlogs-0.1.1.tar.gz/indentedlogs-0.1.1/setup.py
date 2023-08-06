# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['indentedlogs']

package_data = \
{'': ['*']}

install_requires = \
['bandit>=1.6.2,<2.0.0', 'pylint>=2.4.4,<3.0.0', 'radon>=4.1.0,<5.0.0']

setup_kwargs = {
    'name': 'indentedlogs',
    'version': '0.1.1',
    'description': 'Adds indentation to the log messages according to their location in the call stack.',
    'long_description': "# indentedlogs\n\nAdds indentation to the log messages according to their location in the call stack.\n\n* Documentation: <https://gergelyk.github.io/python-indentedlogs>\n* Repository: <https://github.com/gergelyk/python-indentedlogs>\n* Package: <https://pypi.python.org/pypi/indentedlogs>\n* Author: [grzegorz.krason@gmail.com](mailto:grzegorz.krason@gmail.com)\n* License: [MIT](LICENSE)\n\n## Requirements\n\nThis package requires CPython 3.8 or compatible. If you have other version already installed, you can switch using `pyenv`. It must be installed as described in the [manual](https://github.com/pyenv/pyenv).\n\n```sh\npyenv install 3.8.2\npyenv local 3.8.2\n```\n\n## Installation\n\n```sh\npip install indentedlogs\n```\n\n## Examples\n\n```sh\npython examples/demo0.py\npython examples/demo1.py\npython examples/demo2.py\n```\n\n## Development\n\n```sh\n# Preparing environment\npip install --user poetry  # unless already installed\npoetry install\n\n# Auto-formatting\npoetry run docformatter -ri indentedlogs tests\npoetry run isort -rc indentedlogs tests\npoetry run yapf -r -i indentedlogs tests\n\n# Checking coding style\npoetry run flake8 indentedlogs tests\n\n# Checking composition and quality\npoetry run mypy indentedlogs tests\npoetry run pylint indentedlogs tests\npoetry run bandit indentedlogs tests\npoetry run radon cc indentedlogs tests\npoetry run radon mi indentedlogs tests\n\n# Testing with coverage\npoetry run pytest --cov indentedlogs --cov tests\n\n# Rendering documentation\npoetry run mkdocs serve\n\n# Building package\npoetry build\n\n# Releasing\npoetry version minor  # increment selected component\ngit tag ${$(poetry version)[2]}\ngit push --tags\npoetry build\npoetry publish\npoetry run mkdocs build\npoetry run mkdocs gh-deploy -b gh-pages\n```\n\n## Donations\n\nIf you find this software useful and you would like to repay author's efforts you are welcome to use following button:\n\n[![Donate](https://www.paypalobjects.com/en_US/PL/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=D9KUJD9LTKJY8&source=url)\n",
    'author': 'Grzegorz Krasoń',
    'author_email': 'grzegorz.krason@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gergelyk.github.io/python-indentedlogs',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
