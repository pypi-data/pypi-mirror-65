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
    'version': '1.0.1',
    'description': 'A package for implementing various Python packaging standards',
    'long_description': 'mousebender\n###########\nA package for installing fully-specified Python packages.\n\nPackage contents\n================\n\n- ``mousbender.simple`` -- Parsers for the `simple repository API`_\n\nGoals for this project\n======================\n\nThe goal is to provide a package which could install all dependencies as frozen by a tool like `pip-tools`_ via an API (or put another way, what is required to install ``pip`` w/o using pip itself?). This avoids relying on pip\'s CLI to do installations but instead provide a programmatic API. It also helps discover any holes in specifications and/or packages for providing full support for Python package installation based on standards.\n\nThe steps to installing a package\n---------------------------------\n\n`PyPA specifications`_\n\n#. Figure out what packages are necessary\n\n    #. For an app, read lock file (?)\n    #. For a package:\n\n        #. Read list of dependencies (?)\n        #. *Solve dependency constraints* (ResolveLib_)\n\n#. Get the wheel to install\n\n    #. Check if package is already installed (`spec <https://packaging.python.org/specifications/recording-installed-packages/>`__ / `importlib-metadata`_)\n    #. Check local wheel cache (?; `how pip does it <https://pip.pypa.io/en/stable/reference/pip_install/#caching>`__)\n    #. Choose appropriate file from PyPI/index\n\n        #. Process the list of files (`simple repository API`_ / `mousebender.simple`)\n        #. Calculate best-fitting wheel (`spec <https://packaging.python.org/specifications/platform-compatibility-tags/>`__ / `packaging.tags`_)\n        #. If no wheel found ...\n\n            #. Select and download the sdist (?)\n            #. Build the wheel (`PEP 517`_, `PEP 518`_ / pep517_)\n\n    #. *Download the wheel*\n    #. Cache the wheel locally (?)\n\n#. Install the wheel\n\n   #. Install the files (`spec <https://packaging.python.org/specifications/distribution-formats/>`__ / `distlib.wheel`_)\n   #. Record the installation (`spec <https://packaging.python.org/specifications/recording-installed-packages/>`__ / ?)\n\n\nWhere does the name come from?\n==============================\nThe customer from `Monty Python\'s cheese shop sketch`_ is named "Mr. Mousebender". And in case you don\'t know, the original name of PyPI_ was the Cheeseshop after the Monty Python sketch.\n\n\n-----\n\n.. image:: https://github.com/brettcannon/mousebender/workflows/CI/badge.svg\n    :target: https://github.com/brettcannon/mousebender/actions?query=workflow%3ACI+branch%3Amaster+event%3Apush\n    :alt: CI status\n\n.. image:: https://img.shields.io/badge/coverage-100%25-brightgreen\n    :target: https://github.com/brettcannon/mousebender/blob/master/pyproject.toml\n    :alt: 100% branch coverage\n\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/psf/black\n    :alt: Formatted with Black\n\n.. image:: http://www.mypy-lang.org/static/mypy_badge.svg\n    :target: https://mypy.readthedocs.io/\n    :alt: Checked by mypy\n\n.. image:: https://img.shields.io/pypi/pyversions/mousebender\n    :target: https://pypi.org/project/mousebender\n    :alt: PyPI - Python Version\n\n.. image:: https://img.shields.io/pypi/l/mousebender\n    :target: https://github.com/brettcannon/mousebender/blob/master/LICENSE\n    :alt: PyPI - License\n\n.. image:: https://img.shields.io/pypi/wheel/mousebender\n    :target: https://pypi.org/project/mousebender/#files\n    :alt: PyPI - Wheel\n\n\n.. _distlib.wheel: https://distlib.readthedocs.io/en/latest/tutorial.html#installing-from-wheels\n.. _importlib-metadata: https://pypi.org/project/importlib-metadata/\n.. _Monty Python\'s cheese shop sketch: https://en.wikipedia.org/wiki/Cheese_Shop_sketch\n.. _packaging.tags: https://packaging.pypa.io/en/latest/tags/\n.. _PEP 517: https://www.python.org/dev/peps/pep-0517/\n.. _PEP 518: https://www.python.org/dev/peps/pep-0518/\n.. _pep517: https://pypi.org/project/pep517/\n.. _pip-tools: https://pypi.org/project/pip-tools/\n.. _PyPI: https://pypi.org\n.. _PyPA specifications: https://packaging.python.org/specifications/\n.. _ResolveLib: https://pypi.org/project/resolvelib/\n.. _simple repository API: https://packaging.python.org/specifications/simple-repository-api/\n',
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
