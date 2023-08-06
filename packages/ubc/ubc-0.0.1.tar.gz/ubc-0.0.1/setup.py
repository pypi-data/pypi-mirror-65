# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ubc', 'ubc.rates', 'ubc.rates.openei']

package_data = \
{'': ['*']}

install_requires = \
['altair>=4.1.0,<5.0.0',
 'dynaconf>=2.2.3,<3.0.0',
 'jmespath>=0.2.1,<0.3.0',
 'pandas>=1.0.3,<2.0.0',
 'requests>=2.23.0,<3.0.0']

setup_kwargs = {
    'name': 'ubc',
    'version': '0.0.1',
    'description': 'Utility Bill Calculator',
    'long_description': None,
    'author': 'Thomas Tu',
    'author_email': 'thomasthetu@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
