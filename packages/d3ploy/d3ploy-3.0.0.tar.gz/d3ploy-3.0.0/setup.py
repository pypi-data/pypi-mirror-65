# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['d3ploy']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.12.38,<2.0.0',
 'pathspec>=0.7.0,<0.8.0',
 'progressbar2>=3.50.1,<4.0.0',
 'pync>=2.0.3,<3.0.0']

setup_kwargs = {
    'name': 'd3ploy',
    'version': '3.0.0',
    'description': 'Easily deploy to S3 with multiple environment support.',
    'long_description': None,
    'author': 'dryan',
    'author_email': 'dryan@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
