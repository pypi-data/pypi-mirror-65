# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chitchat_dataset']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'chitchat-dataset',
    'version': '0.3.0',
    'description': "Open-domain conversational dataset from the BYU Perception, Control & Cognition lab's Chit-Chat Challenge.",
    'long_description': None,
    'author': 'William Myers',
    'author_email': 'mwilliammyers@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
