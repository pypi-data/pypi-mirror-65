# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mousebender']

package_data = \
{'': ['*']}

install_requires = \
['packaging>=20.3,<21.0']

setup_kwargs = {
    'name': 'mousebender',
    'version': '1.0.0',
    'description': 'A package for implementing various Python packaging standards',
    'long_description': 'mousebender\n###########\nA package for installing fully-specified Python packages.\n\nPackage contents\n================\n\n- ``mousbender.simple`` -- Parsers for the `simple repository API`_\n\nGoals for this project\n======================\n\nThe goal is to provide a package which could install all dependencies as frozen by a tool like `pip-tools`_ via an API (or put another way, what is required to install ``pip`` w/o using pip itself?). This avoids relying on pip\'s CLI to do installations but instead provide a programmatic API. It also helps discover any holes in specifications and/or packages for providing full support for Python package installation based on standards.\n\nThe steps to installing a package\n---------------------------------\n\n`PyPA specifications`_\n\n1. Check if package is already installed (`spec <https://packaging.python.org/specifications/recording-installed-packages/>`__ / `importlib-metadata`_)\n2. Check local wheel cache (? / ?; `how pip does it <https://pip.pypa.io/en/stable/reference/pip_install/#caching>`__)\n3. Choose appropriate file from PyPI/index\n\n   1. Process the list of files (`simple repository API`_ / `mousebender.simple`)\n   2. Calculate best-fitting wheel (`spec <https://packaging.python.org/specifications/platform-compatibility-tags/>`__ / `packaging.tags`_)\n\n4. *Download the wheel*\n5. Cache the wheel locally (? / ?)\n6. Install the wheel\n\n   1. Install the files (`spec <https://packaging.python.org/specifications/distribution-formats/>`__ / `distlib.wheel`_)\n   2. Record the installation (`spec <https://packaging.python.org/specifications/recording-installed-packages/>`__ / ?)\n\n\nThings pip does that the above outline doesn\'t\n----------------------------------------------\n\n* Parse a frozen ``requirements.txt`` file\n* Install from an sdist\n* Install dependencies (i.e. read dependencies from wheel, solve dependency graph)\n* Networking (everything is sans-I/O to allow the user to use whatever networking approach they want)\n\nWhere does the name come from?\n==============================\nThe customer from `Monty Python\'s cheese shop sketch`_ is named "Mr. Mousebender". And in case you don\'t know, the original name of PyPI_ was the Cheeseshop after the Monty Python sketch.\n\n\n---\n.. image::https://img.shields.io/badge/code%20style-black-000000.svg :target: https://github.com/psf/black\n\n\n.. _distlib.wheel: https://distlib.readthedocs.io/en/latest/tutorial.html#installing-from-wheels\n.. _importlib-metadata: https://pypi.org/project/importlib-metadata/\n.. _Monty Python\'s cheese shop sketch: https://en.wikipedia.org/wiki/Cheese_Shop_sketch\n.. _packaging.tags: https://packaging.pypa.io/en/latest/tags/\n.. _pip-tools: https://pypi.org/project/pip-tools/\n.. _PyPI: https://pypi.org\n.. _PyPA specifications: https://packaging.python.org/specifications/\n.. _simple repository API: https://packaging.python.org/specifications/simple-repository-api/\n',
    'author': 'Brett Cannon',
    'author_email': 'brett@snarky.ca',
    'maintainer': 'Derek Keeler',
    'maintainer_email': 'derek@suchcool.ca',
    'url': 'https://github.com/brettcannon/mousebender',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4',
}


setup(**setup_kwargs)
