# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dyncache', 'dyncache..ropeproject']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.1,<8.0.0', 'cloudpickle>=1.3.0,<2.0.0']

setup_kwargs = {
    'name': 'dyncache',
    'version': '0.1.0',
    'description': 'Dynamic input-output caching for deterministic functions',
    'long_description': '**Dynamic input-output caching for deterministic functions**\n\n|pypi| |docs| |license|\n\nFeatures\n========\n\n* Keep It Simple, Stupid: A single decorator that does everything for you\n* Automagically detects if the decorated function is changed and transparently\n  updates cache accordingly without ever returning cached results of the old\n  function.\n\nInstallation\n============\n\n:code:`pip3 install dyncache`\n\nExamples\n========\n\n.. code:: python3\n   \n   # Import the class\n   from dyncache import Cache\n\n\n   # Use with default options. It will create a file "circle_area.dyncache" into\n   # the current directory.\n   @Cache()\n   def circle_area(radius):\n       return 3.14159 * (radius ** 2)\n       \n\n   # Empty parentheses are not required for the decorator.\n   @Cache\n   def circle_area(radius):\n       return 3.14159 * (radius ** 2)\n\n\n   circle_area(2)  # Calculates and returns\n   circle_area(3)  # Calculates and returns\n   circle_area(2)  # Returns from cache\n\n\n   # Saves the cache to /tmp/hello.world.\n   @Cache(root="/tmp", filename="hello.world")\n   def circle_area(radius):\n       ...\n\n\n   # Use for function with large input/output -values.\n   @Cache(largeitems=True)\n   def load_all_api_data_for_a_day(day):\n       ...\n\n\n   # When items are small and cache would update too often, setting autowrite to\n   # False lets you control when the cached data is written to the file.\n   cache = Cache(autowrite=False)\n   @cache\n   def really_frequent_function(a, b):\n       ...\n   ...\n   cache.write()  # Write cache data to the file\n   sys.exit(0)\n\n\nContributing\n============\n\n* Send any issues to GitHub\'s issue tracker.\n* Before sending a pull request, format it with `Black`_ (-Sl79)\n* Any changes must be updated to the documentation\n* All pull requests must be tested with tox (if you are using pyenv, add the installed versions for py35-py38 and pypy3 to .python-version at the root of this repository before running tox)\n\n\n.. _`Black`: https://github.com/psf/black\n\n.. |pypi| image:: https://img.shields.io/pypi/v/dyncache.svg\n    :alt: PyPI\n    :target: https://pypi.org/project/dyncache/\n.. |docs| image:: https://readthedocs.org/projects/dyncache/badge/?version=latest\n    :alt: Read the Docs\n    :target: http://dyncache.readthedocs.io/en/latest/\n.. |license| image:: https://img.shields.io/github/license/b10011/dyncache.svg\n    :alt: License\n    :target: https://github.com/b10011/dyncache/blob/master/LICENSE\n',
    'author': 'Niko Järvinen',
    'author_email': 'nbjarvinen@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/b10011/dyncache',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
