# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['arger', 'arger.parser']

package_data = \
{'': ['*']}

install_requires = \
['docstring-parser>=0.6.1,<0.7.0']

setup_kwargs = {
    'name': 'arger',
    'version': '0.2.4',
    'description': 'Create argparser automatically from functions',
    'long_description': '# Overview\n\nA wrapper around argparser to help build CLIs from functions. Uses typehints extensively.\n\n[![PyPi Version](https://img.shields.io/pypi/v/arger.svg?style=flat)](https://pypi.python.org/pypi/arger)\n[![Python Version](https://img.shields.io/pypi/pyversions/returns.svg)](https://pypi.org/project/arger/)\n![](https://github.com/jnoortheen/arger/workflows/test-and-publish/badge.svg)\n[![PyPI License](https://img.shields.io/pypi/l/arger.svg)](https://pypi.org/project/arger)\n\n# Setup\n\n## Installation\n\nInstall it directly into an activated virtual environment:\n\n```text\n$ pip install arger\n```\n\nor add it to your [Poetry](https://poetry.eustace.io/) project:\n\n```text\n$ poetry add arger\n```\n\n# Usage\n- create a python file called test.py\n```python\nfrom arger import Arger\n\ndef main(param1: int, param2: str, kw1=None, kw2=False):\n    """Example function with types documented in the docstring.\n\n    :param param1: The first parameter.\n    :param param2: The second parameter.\n    """\n    print(locals())\n\n\nif __name__ == \'__main__\':\n    Arger(main).run()\n```\n\n- run this normally with \n\n```shell script\n$ python test.py 100 param2\n```\n\n- Checkout [examples](./tests/examples) folder and documentation to see more of `arger` in action.\n\n# Alternatives\n\n## [argh](https://argh.readthedocs.io/en/latest/tutorial.html) \n - has similar goals as to ease up using argparser. \n - doesn\'t support type hints. \n - No recent releases.\n\n## [typer](https://github.com/tiangolo/typer)\n - if you are using `click`, I highly recommend you to check this library.\n - it is neat and many features are inspired from this library.\n - doesn\'t support loading help text for arguments from docstrings.\n \n## [invoke](http://www.pyinvoke.org/) \n - doesn\'t support type hints.\n\n## [cliche](https://github.com/kootenpv/cliche)\n - has similar goals. \n - doesn\'t cover much use cases as `arger`.\n\nThis project was generated with [cookiecutter](https://github.com/audreyr/cookiecutter) using [jacebrowning/template-python](https://github.com/jacebrowning/template-python).\n',
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
