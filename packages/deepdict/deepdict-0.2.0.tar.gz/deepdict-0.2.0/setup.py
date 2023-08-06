# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['deepdict']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'deepdict',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'Yampolskiy Dmitriy',
    'author_email': 'yampolskiydv@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0.0',
}


setup(**setup_kwargs)
