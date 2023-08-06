# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['willing_zg', 'willing_zg.resources']

package_data = \
{'': ['*']}

install_requires = \
['zygoat>=0.5.0,<0.6.0']

setup_kwargs = {
    'name': 'willing-zg',
    'version': '0.1.0',
    'description': '',
    'long_description': '# willing_zg\n\nWilling specific plugins for Zygoat\n',
    'author': 'Bequest, Inc.',
    'author_email': 'oss@willing.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
