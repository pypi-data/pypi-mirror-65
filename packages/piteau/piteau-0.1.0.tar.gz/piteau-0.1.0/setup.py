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
    'version': '0.1.0',
    'description': 'Python asynchronous chat',
    'long_description': '********************************************\nPiteau: Asynchronous Chat\n********************************************\n.. image:: https://badgen.net/badge/python%20version/3.6|3.7|3.8/blue\n\n.. image:: https://travis-ci.com/cimourdain/piteau.svg?branch=master\n    :target: https://travis-ci.com/cimourdain/piteau\n\n.. image:: https://readthedocs.org/projects/piteau/badge/?version=latest\n    :target: https://piteau.readthedocs.io/en/latest/?badge=latest\n    :alt: Documentation Status\n\n.. image:: https://badgen.net/badge/code%20style/black/000\n    :target: https://github.com/ambv/black\n    :alt: code style: black\n\n.. image:: https://badgen.net/badge/static%20typing/mypy/\n    :target: https://github.com/python/mypy\n    :alt: static-typing : mypy\n\n.. image:: https://badgen.net/github/license/cimourdain/piteau\n\n\n**Piteau** is an asynchronous chat application written in python for education purposes.\n\nFeatures\n========\n\n- Chat server to route message between clients\n- Chat client to send user input messages to server and receive server messages\n- Easy way to implement a chat bot\n\nDocumentation\n=============\n\nFull documentation is available at https://piteau.readthedocs.io/ .\n \nRoadmap\n=======\n\n- Unit testing\n- Implement chatrooms, private messages and IRC-like commands\n- Implement UI\n\n',
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
