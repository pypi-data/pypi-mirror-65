# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['liquidata']
setup_kwargs = {
    'name': 'liquidata',
    'version': '0.1.1',
    'description': 'EDSL for data pipelines in Python',
    'long_description': None,
    'author': 'Jacek Generowicz',
    'author_email': 'github@my-post-office.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jacg/liquidata',
    'py_modules': modules,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
