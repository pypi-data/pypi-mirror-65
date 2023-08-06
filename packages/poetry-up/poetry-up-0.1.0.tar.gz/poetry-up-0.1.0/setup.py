# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['poetry_up']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=1.5.0,<2.0.0']}

entry_points = \
{'console_scripts': ['poetry-up = poetry_up.console:main']}

setup_kwargs = {
    'name': 'poetry-up',
    'version': '0.1.0',
    'description': 'Poetry Up',
    'long_description': '[![Tests](https://github.com/cjolowicz/poetry-up/workflows/Tests/badge.svg)](https://github.com/cjolowicz/poetry-up/actions?workflow=Tests)\n[![Codecov](https://codecov.io/gh/cjolowicz/poetry-up/branch/master/graph/badge.svg)](https://codecov.io/gh/cjolowicz/poetry-up)\n[![PyPI](https://img.shields.io/pypi/v/poetry-up.svg)](https://pypi.org/project/poetry-up/)\n[![Python Version](https://img.shields.io/pypi/pyversions/poetry-up)](https://pypi.org/project/poetry-up)\n[![Read the Docs](https://readthedocs.org/projects/poetry-up/badge/)](https://poetry-up.readthedocs.io/)\n[![License](https://img.shields.io/pypi/l/poetry-up)](https://opensource.org/licenses/MIT)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n# poetry-up\n',
    'author': 'Claudio Jolowicz',
    'author_email': 'mail@claudiojolowicz.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/cjolowicz/poetry-up',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
