# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dff_calc']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.18.2,<2.0.0', 'pandas>=1.0.3,<2.0.0', 'scipy>=1.4.1,<2.0.0']

setup_kwargs = {
    'name': 'dff-calc',
    'version': '0.2.0',
    'description': 'Calculate dF/F for neural calcium traces',
    'long_description': None,
    'author': 'HagaiHargil',
    'author_email': 'hagaihargil@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
