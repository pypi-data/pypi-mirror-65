# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rpaframework_screenshot']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'rpaframework-screenshot',
    'version': '0.0.1',
    'description': '',
    'long_description': '',
    'author': 'Mika Hänninen',
    'author_email': 'mika@robocorp.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
