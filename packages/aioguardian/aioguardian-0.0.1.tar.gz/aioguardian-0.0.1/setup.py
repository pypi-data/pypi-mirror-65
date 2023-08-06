# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aioguardian']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.6.2,<4.0.0']

setup_kwargs = {
    'name': 'aioguardian',
    'version': '0.0.1',
    'description': 'A Python3 library for Elexa Guardian water valves and sensors',
    'long_description': '# 🚰 aioguardian: A Python3 library for Elexa Guardian devices\n',
    'author': 'Aaron Bach',
    'author_email': 'bachya1208@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bachya/aioguardian',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
