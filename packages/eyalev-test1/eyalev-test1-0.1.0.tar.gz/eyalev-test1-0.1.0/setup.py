# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['eyalev_test1']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['test1-cli = test1.main:main']}

setup_kwargs = {
    'name': 'eyalev-test1',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Eyal Levin',
    'author_email': 'eyalev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
