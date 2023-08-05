# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['a_la_mode']

package_data = \
{'': ['*']}

install_requires = \
['bencode.py>=2.1.0,<3.0.0', 'toolz>=0.10.0,<0.11.0', 'toposort==1.5']

setup_kwargs = {
    'name': 'a-la-mode',
    'version': '0.1.2',
    'description': 'A tool for describing pure data pipelines that enables avoiding repeating work (incrementality) and keeping old data around (provenance)',
    'long_description': None,
    'author': 'thattommyhall',
    'author_email': 'thattommyhall@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
