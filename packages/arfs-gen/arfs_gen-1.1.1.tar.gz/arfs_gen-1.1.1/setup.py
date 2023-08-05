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
    'version': '1.1.1',
    'description': 'Library to generate toy data for machine learning experiments in the context of all-relevant feature selection.',
    'long_description': '# All Relevant Feature Selection Generator Library (ARFS-Gen)\n![PyPI](https://img.shields.io/pypi/v/arfs_gen)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/arfs_gen)\n![PyPI - License](https://img.shields.io/pypi/l/arfs_gen)\n\nThis repository contains a python library to generate synthetic (toy) data for use in research papers when evaluating all relevant feature selection e.g.  used in [fri](https://github.com/lpfann/fri).\n\nIt allows creating datasets with a specified number of strongly and weakly relevant features as well as random noise features.\n\nIn the newest revision it also includes methods which generate data with privileged information.\n\nIt works by utilizing existing methods from `numpy` and `scikit-learn`.\n# Install\nThe library is available on [PyPi](https://pypi.org/project/arfs-gen/).\nInstall via `pip`:\n```shell\npip install arfs_gen\n```\nor clone this repository and use:\n```shell\npip install .\n```\n\n# Usage\nIn the following we generate a simple regression data set with a mix of strongly and weakly relevant features:\n\n```python\n    # Import relevant method\n    from arfs_gen import genRegressionData\n    # Import model\n    from sklearn.svm import LinearSVR\n\n    # Specify parameters\n    n = 100\n    # Features\n    strRel = 2\n    strWeak = 2\n    # Overall number of features (Rest will be filled by random features)\n    d = 10\n\n    # Generate the data\n    X, y = genRegressionData(\n        n_samples=n,\n        n_features=d,\n        n_redundant=strWeak,\n        n_strel=strRel,\n        n_repeated=0,\n        noise=0,\n    )\n    # Fit a model\n    linsvr = LinearSVR()\n    linsvr.fit(X, y)\n```\n\n# Development\nFor dependency management we use the newly released [poetry](https://python-poetry.org/) tool.\n\nIf you have `poetry` installed, use\n```shell\n$ poetry install\n```  \ninside the project folder to create a new `venv` and to install all dependencies.\nTo enter the newly created `venv` use \n```shell \n$ poetry env\n```\nto open a new shell inside.\nOr alternatively run commands inside the `venv` with `poetry run ...`.\n\n## Test\nTest it by running `poetry run pytest`.\n',
    'author': 'Lukas Pfannschmidt',
    'author_email': 'lukas@lpfann.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/lpfann/arfs_gen',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
