# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['piteau', 'piteau.base']

package_data = \
{'': ['*']}

install_requires = \
['aioconsole>=0.1.16,<0.2.0']

setup_kwargs = {
    'name': 'piteau',
    'version': '0.1.1',
    'description': 'Python asynchronous chat',
    'long_description': 'Piteau is an asynchronous chat application written in python for education purposes.\n',
    'author': 'Gabriel Oger',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/piteau/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
