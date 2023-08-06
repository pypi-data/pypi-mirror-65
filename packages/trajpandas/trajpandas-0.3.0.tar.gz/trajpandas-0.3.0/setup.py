# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['trajpandas', 'trajpandas.io', 'trajpandas.utils']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1,<2', 'pandas>=1,<2', 'scipy>=1,<2']

setup_kwargs = {
    'name': 'trajpandas',
    'version': '0.3.0',
    'description': '',
    'long_description': None,
    'author': 'Bror Jonsson',
    'author_email': 'brorfred@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
