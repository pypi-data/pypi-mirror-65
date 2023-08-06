# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flask_shortcut', 'tests']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.1,<8.0.0', 'flask>=1.1.2,<2.0.0']

setup_kwargs = {
    'name': 'flask-shortcut',
    'version': '0.1.0',
    'description': 'Extension that provides an easy way to add dev-only shortcuts to your routes.',
    'long_description': 'Flask-Shortcut\n==============\n\nExtension that provides an easy way to add dev-only shortcuts to your routes.\n',
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
