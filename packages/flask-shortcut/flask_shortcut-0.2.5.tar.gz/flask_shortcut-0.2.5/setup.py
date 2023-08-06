# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flask_shortcut', 'tests']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.1,<8.0.0',
 'flask>=1.1.2,<2.0.0',
 'importlib-metadata>=1.6.0,<2.0.0',
 'xmltodict>=0.12.0,<0.13.0']

setup_kwargs = {
    'name': 'flask-shortcut',
    'version': '0.2.5',
    'description': 'Extension that provides an easy way to add dev-only shortcuts to your routes.',
    'long_description': 'Flask-Shortcut\n==============\n\n.. image:: https://img.icons8.com/color/144/000000/cabbage.png\n   :alt: Cabbage\n   :align: center\n\n\n.. image:: https://github.com/a-recknagel/Flask-Shortcut/workflows/CI-CD/badge.svg\n   :alt: Main workflow status\n   :target: https://github.com/a-recknagel/Flask-Shortcut/actions\n\n.. image:: https://img.shields.io/pypi/v/flask-shortcut\n   :alt: Current pyPI version\n   :target: https://pypi.org/project/flask-shortcut/\n\n.. image:: https://img.shields.io/badge/docs-github--pages-blue\n   :alt: Documentation home\n   :target: https://a-recknagel.github.io/flask-shortcut/\n\n.. image:: https://img.shields.io/pypi/l/flask-shortcut\n   :alt: Package license\n   :target: https://pypi.org/project/flask-shortcut/\n\n.. image:: https://img.shields.io/pypi/pyversions/flask-shortcut\n   :alt: Supported on python versions\n   :target: https://pypi.org/project/flask-shortcut/\n\n.. image:: https://img.shields.io/badge/codestyle-black-black\n   :alt: Any color you want\n   :target: https://black.readthedocs.io/en/stable/\n\n.. header-end\n\nProject Description\n-------------------\n\nExtension that provides an easy way to add dev-only shortcuts to routes in your\nflask application.\n',
    'author': 'Arne',
    'author_email': 'arecknag@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/a-recknagel/Flask-Shortcut',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
