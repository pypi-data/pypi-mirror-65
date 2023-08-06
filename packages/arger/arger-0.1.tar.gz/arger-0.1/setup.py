# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['arger', 'arger.parser']

package_data = \
{'': ['*']}

install_requires = \
['click>=6.0,<7.0', 'docstring-parser>=0.6.1,<0.7.0', 'minilog>=1.4,<2.0']

setup_kwargs = {
    'name': 'arger',
    'version': '0.1',
    'description': 'Create argparser automatically from functions',
    'long_description': "# Overview\n\nA wrapper around argparser to help build CLIs from functions. Uses typehints extensively.\n\n[![PyPi Version](https://img.shields.io/pypi/v/arger.svg?style=flat)](https://pypi.python.org/pypi/arger)\n[![Python Version](https://img.shields.io/pypi/pyversions/returns.svg)](https://pypi.org/project/arger/)\n\n[![Unix Build Status](https://img.shields.io/travis/jnoortheen/arger/master.svg?label=unix)](https://travis-ci.org/jnoortheen/arger)\n[![Windows Build Status](https://img.shields.io/appveyor/ci/jnoortheen/arger/master.svg?label=windows)](https://ci.appveyor.com/project/jnoortheen/arger)\n[![Coverage Status](https://img.shields.io/coveralls/jnoortheen/arger/master.svg)](https://coveralls.io/r/jnoortheen/arger)\n[![Scrutinizer Code Quality](https://img.shields.io/scrutinizer/g/jnoortheen/arger.svg)](https://scrutinizer-ci.com/g/jnoortheen/arger/?branch=master)\n[![PyPI Version](https://img.shields.io/pypi/v/arger.svg)](https://pypi.org/project/arger)\n[![PyPI License](https://img.shields.io/pypi/l/arger.svg)](https://pypi.org/project/arger)\n\n# Setup\n\n## Installation\n\nInstall it directly into an activated virtual environment:\n\n```text\n$ pip install arger\n```\n\nor add it to your [Poetry](https://poetry.eustace.io/) project:\n\n```text\n$ poetry add arger\n```\n\n# Usage\n\nAfter installation, the package can imported:\n\n```text\n$ python\n>>> import arger\n>>> arger.__version__\n```\n\n# Alternatives\n\n## [argh](https://argh.readthedocs.io/en/latest/tutorial.html) \n - has similar goals as to ease up using argparser. \n - doesn't support type hints. \n - No recent releases.\n\n## [typer](https://github.com/tiangolo/typer)\n - if you are using `click`, I highly recommend you to check this library.\n - it is neat and many features are inspired from this library.\n - doesn't support loading help text for arguments from docstrings.\n \n## [invoke](http://www.pyinvoke.org/) \n - doesn't support type hints.\n\n## [cliche](https://github.com/kootenpv/cliche)\n - has similar goals. \n - doesn't cover much use cases as `arger`.\n\nThis project was generated with [cookiecutter](https://github.com/audreyr/cookiecutter) using [jacebrowning/template-python](https://github.com/jacebrowning/template-python).",
    'author': 'Noortheen Raja',
    'author_email': 'jnoortheen@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/arger',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
