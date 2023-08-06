# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['versionup']
install_requires = \
['fire>=0.2.1,<0.3.0', 'toml', 'typing-extensions>=3.7.4,<4.0.0']

extras_require = \
{':python_version < "3.7"': ['dataclasses']}

entry_points = \
{'console_scripts': ['versionup = versionup:cli']}

setup_kwargs = {
    'name': 'pyversionup',
    'version': '0.1.5',
    'description': '',
    'long_description': None,
    'author': 'Yohei Tamura',
    'author_email': 'tamuhey@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
