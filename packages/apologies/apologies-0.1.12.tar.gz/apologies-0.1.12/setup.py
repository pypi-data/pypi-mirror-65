# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['apologies']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=19.3.0,<20.0.0',
 'cattrs>=1.0.0,<2.0.0',
 'orjson>=2.6.1,<3.0.0',
 'pendulum>=2.1.0,<3.0.0']

setup_kwargs = {
    'name': 'apologies',
    'version': '0.1.12',
    'description': 'Python code to play a game similar to Sorry',
    'long_description': '# Apologies Python Library\n\n![](https://img.shields.io/pypi/l/apologies.svg)\n![](https://img.shields.io/pypi/wheel/apologies.svg)\n![](https://img.shields.io/pypi/pyversions/apologies.svg)\n![](https://github.com/pronovic/apologies/workflows/Test%20Suite/badge.svg)\n\n[Apologies](https://gitub.com/pronovic/apologies) is a Python library that\nimplements a game similar to the [Sorry](https://en.wikipedia.org/wiki/Sorry!_(game)) board \ngame.  It includes a console demo that plays the game with automated players,\nintended for use by developers and not by end users.\n\nIt also serves as a complete example of how to manage a modern (circa 2020)\nPython project, including style checks, code formatting, integration with\nIntelliJ, CI builds at GitHub, and integration with PyPI and Read the Docs.\n',
    'author': 'Kenneth J. Pronovici',
    'author_email': 'pronovic@ieee.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://apologies.readthedocs.io',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
