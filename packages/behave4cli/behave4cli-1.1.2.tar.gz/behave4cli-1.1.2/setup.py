# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['behave4cli', 'behave4cli.log']

package_data = \
{'': ['*']}

install_requires = \
['PyHamcrest>=2.0.2,<3.0.0', 'behave>=1.2.6,<2.0.0']

extras_require = \
{'bdd': ['mypy>=0.740.0,<0.741.0'],
 'docs': ['sphinx>=2.3.0,<3.0.0',
          'sphinx-autodoc-typehints>=1.10.3,<2.0.0',
          'sphinx-autobuild>=0.7.1,<0.8.0',
          'sphinx_rtd_theme>=0.4.3,<0.5.0'],
 'format': ['isort>=4.3,<5.0', 'seed-isort-config>=1.9.3,<2.0.0', 'black'],
 'lint': ['flake8>=3.7,<4.0',
          'flake8-bugbear>=19.8.0,<20.0.0',
          'pydocstyle>=3.0,<4.0',
          'pylint>=2.3,<3.0',
          'yapf>=0.27.0,<0.28.0'],
 'repl': ['bpython>=0.18,<0.19'],
 'test': ['pytest>=5.1,<6.0',
          'pytest-cov>=2.8.1,<3.0.0',
          'pytest-mock>=1.13.0,<2.0.0',
          'pytest-html>=2.0.1,<3.0.0',
          'pytest-asyncio>=0.10.0,<0.11.0',
          'mock>=4.0.2,<5.0.0'],
 'type': ['mypy>=0.740.0,<0.741.0']}

setup_kwargs = {
    'name': 'behave4cli',
    'version': '1.1.2',
    'description': 'This project provides an extension (testing domain) of behave to test commands and command-line interfaces (console apps).',
    'long_description': None,
    'author': 'Emmanuel Sciara',
    'author_email': 'emmanuel.sciara@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/esciara/behave4cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
