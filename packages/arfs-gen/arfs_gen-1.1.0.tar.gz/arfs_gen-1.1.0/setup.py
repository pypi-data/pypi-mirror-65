# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['arfs_gen', 'arfs_gen.tests']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1,<2', 'scikit-learn>=0,<1']

setup_kwargs = {
    'name': 'arfs-gen',
    'version': '1.1.0',
    'description': 'Library to generate toy data for machine learning experiments in the context of all-relevant feature selection.',
    'long_description': None,
    'author': 'Lukas Pfannschmidt',
    'author_email': 'lukas@lpfann.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
