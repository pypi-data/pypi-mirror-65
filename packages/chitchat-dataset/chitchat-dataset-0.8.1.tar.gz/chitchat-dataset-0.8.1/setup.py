# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chitchat_dataset']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'chitchat-dataset',
    'version': '0.8.1',
    'description': 'Open-domain conversational dataset from the BYU PCC lab',
    'long_description': '# chitchat-dataset\n\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/chitchat_dataset)](https://pypi.org/project/chitchat-dataset/)\n[![PyPI](https://img.shields.io/pypi/v/chitchat_dataset)](https://pypi.org/project/chitchat-dataset/)\n[![PyPI - Wheel](https://img.shields.io/pypi/wheel/chitchat_dataset)](https://pypi.org/project/chitchat-dataset/)\n\n[![CI](https://github.com/BYU-PCCL/chitchat-dataset/workflows/CI/badge.svg)](https://github.com/BYU-PCCL/chitchat-dataset/actions?query=workflow%3ACI)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\nOpen-domain conversational dataset from the BYU\n[Perception, Control & Cognition] lab\'s [Chit-Chat Challenge].\n\n## install\n\n```bash\npip3 install chitchat_dataset\n```\n\n_or_ simply download the raw dataset:\n\n```bash\ncurl -LO https://raw.githubusercontent.com/BYU-PCCL/chitchat-dataset/master/chitchat_dataset/dataset.json\n```\n\n## usage\n\n```python\nimport chitchat_dataset as ccc\n\ndataset = ccc.Dataset()\n\n# Dataset is a subclass of dict()\nfor convo_id, convo in dataset.items():\n    print(convo_id, convo)\n```\n\nSee [`examples/`] for other languages.\n\n## stats\n\n- 7,168 conversations\n- 258,145 utterances\n- 1,315 unique participants\n\n## format\n\nThe [dataset] is a mapping from conversation [UUID] to a conversation:\n\n```json\n{\n  "prompt": "What\'s the most interesting thing you\'ve learned recently?",\n  "ratings": { "witty": "1", "int": 5, "upbeat": 5 },\n  "start": "2018-04-20T01:57:41",\n  "messages": [\n    [\n      {\n        "text": "Hello",\n        "timestamp": "2018-04-19T19:57:51",\n        "sender": "22578ac2-6317-44d5-8052-0a59076e0b96"\n      }\n    ],\n    [\n      {\n        "text": "I learned that the Queen of England\'s last corgi died",\n        "timestamp": "2018-04-19T19:58:14",\n        "sender": "bebad07e-15df-48c3-a04f-67db828503e3"\n      }\n    ],\n    [\n      {\n        "text": "Wow that sounds so sad",\n        "timestamp": "2018-04-19T19:58:18",\n        "sender": "22578ac2-6317-44d5-8052-0a59076e0b96"\n      },\n      {\n        "text": "was it a cardigan welsh corgi",\n        "timestamp": "2018-04-19T19:58:22",\n        "sender": "22578ac2-6317-44d5-8052-0a59076e0b96"\n      },\n      {\n        "text": "?",\n        "timestamp": "2018-04-19T19:58:24",\n        "sender": "22578ac2-6317-44d5-8052-0a59076e0b96"\n      }\n    ]\n  ]\n}\n```\n\n# how to cite\n\nIf you extend or use this work, please cite the paper where it was introduced:\n\n```\n@article{myers2020conversational,\n  title={Conversational Scaffolding: An Analogy-Based Approach to Response Prioritization in Open-Domain Dialogs},\n  author={Myers, Will and Etchart, Tyler and Fulda, Nancy},\n  year={2020}\n}\n```\n\n[perception, control & cognition]: https://pcc.cs.byu.edu\n[chit-chat challenge]: https://pcc.cs.byu.edu/2018/04/18/the-chit-chat-challenge/\n[dataset]: chitchat_dataset/dataset.py\n[dataset.json]: chitchat_dataset/dataset.py\n[`dataset.json`]: chitchat_dataset/dataset.py\n[uuid]: https://en.wikipedia.org/wiki/Universally_unique_identifier#Version_4_(random)\n[requests]: https://2.python-requests.org/en/master/\n[examples]: examples/\n[`examples/`]: examples/\n',
    'author': 'William Myers',
    'author_email': 'mwilliammyers@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/BYU-PCCL/chitchat-dataset',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
