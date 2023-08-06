# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['toml_validator']

package_data = \
{'': ['*'], 'toml_validator': ['.vscode/*']}

install_requires = \
['click>=7.0,<8.0', 'tomlkit>=0.5.9,<0.6.0']

extras_require = \
{':python_version < "3.8"': ['importlib_metadata>=1.6.0,<2.0.0']}

entry_points = \
{'console_scripts': ['toml-validator = toml_validator.console:main']}

setup_kwargs = {
    'name': 'toml-validator',
    'version': '1.0.0',
    'description': 'Simple TOML file validator using Python.',
    'long_description': '# toml-validator\n\n[![Tests](https://github.com/staticdev/toml-validator/workflows/Tests/badge.svg)](https://github.com/staticdev/toml-validator/actions?workflow=Tests)\n[![Codecov](https://codecov.io/gh/staticdev/toml-validator/badge.svg?branch=master&service=github)](https://codecov.io/gh/staticdev/toml-validator)\n![PyPi](https://badge.fury.io/py/toml-validator.svg)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\nSimple TOML file validator using Python.\n\n## Quickstart\n\n```sh\npip install toml-validator\ntoml-validator FILANAME\n```\n\nIt gives a green message for correct files and red message with errors.\n',
    'author': "Thiago Carvalho D'Ávila",
    'author_email': 'thiagocavila@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/staticdev/toml-validator',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
