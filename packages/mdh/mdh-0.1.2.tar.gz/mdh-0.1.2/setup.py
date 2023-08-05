# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mdh']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=19.0', 'numpy>=1.9', 'scipy>=1.0']

setup_kwargs = {
    'name': 'mdh',
    'version': '0.1.2',
    'description': 'modified dh',
    'long_description': '# Modified Denavit–Hartenberg (mdh)\n\n[![Actions Status](https://github.com/MultipedRobotics/dh/workflows/CheckPackage/badge.svg)](https://github.com/MultipedRobotics/dh/actions)\n![GitHub](https://img.shields.io/github/license/multipedrobotics/dh)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mdh)\n![PyPI](https://img.shields.io/pypi/v/mdh)\n\n\n<img src="https://upload.wikimedia.org/wikipedia/commons/d/d8/DHParameter.png" width="600px">\n\n[Modified Denavit-Hartenberg parameters](https://en.wikipedia.org/wiki/Denavit%E2%80%93Hartenberg_parameters#Modified_DH_parameters)\n\n## Inspiration\n\nYou should probably use one of these, they inspired me to write a simpler\nmodule for my needs:\n\n- [pybotics](https://github.com/nnadeau/pybotics)\n- [pytransform3d](https://github.com/rock-learning/pytransform3d)\n',
    'author': 'walchko',
    'author_email': 'walchko@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/mdh/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
