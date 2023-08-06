# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['inpynamodb', 'inpynamodb.connection']

package_data = \
{'': ['*']}

install_requires = \
['aiobotocore>=0.10.3,<0.11.0',
 'async-property>=0.2.1,<0.3.0',
 'coveralls>=2.0.0,<3.0.0',
 'pynamodb==4.1.0']

setup_kwargs = {
    'name': 'inpynamodb',
    'version': '4.1.0',
    'description': 'asyncio wrapper of PynamoDB',
    'long_description': None,
    'author': 'sunghyun-lee',
    'author_email': 'sunghyunlee@mymusictaste.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
