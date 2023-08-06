# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['spelcheck']
install_requires = \
['fuzzywuzzy>=0.18.0,<0.19.0']

setup_kwargs = {
    'name': 'spelcheck',
    'version': '0.1.0',
    'description': 'Automagically spellcheck your classes',
    'long_description': None,
    'author': 'L3viathan',
    'author_email': 'git@l3vi.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
