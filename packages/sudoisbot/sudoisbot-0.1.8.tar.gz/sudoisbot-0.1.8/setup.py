# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sudoisbot']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML', 'python-daemon', 'python-telegram-bot']

entry_points = \
{'console_scripts': ['listener = sudoisbot.tglistener:main',
                     'sendtelegram = sudoisbot.sendtelegram:main']}

setup_kwargs = {
    'name': 'sudoisbot',
    'version': '0.1.8',
    'description': '',
    'long_description': None,
    'author': 'Benedikt Kristinsson',
    'author_email': 'benedikt@lokun.is',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
