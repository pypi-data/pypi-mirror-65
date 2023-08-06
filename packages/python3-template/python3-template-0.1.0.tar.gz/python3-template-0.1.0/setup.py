# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['python3_template']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.1,<8.0.0',
 'desert>=2020.1.6,<2021.0.0',
 'marshmallow>=3.5.1,<4.0.0',
 'requests>=2.23.0,<3.0.0']

entry_points = \
{'console_scripts': ['python3-template = python3_template.console:main']}

setup_kwargs = {
    'name': 'python3-template',
    'version': '0.1.0',
    'description': 'python3-template project',
    'long_description': '[![Tests](https://github.com/zgallagher08/python3-template/workflows/Tests/badge.svg)](https://github.com/zgallagher08/python3-template/actions?workflow=Tests)\n[![Codecov](https://codecov.io/gh/zgallagher08/python3-template/branch/master/graph/badge.svg)](https://codecov.io/gh/zgallagher08/python3-template)\n[![PyPI](https://img.shields.io/pypi/v/python3-template.svg)](https://pypi.org/project/python3-template/)\n\n# python3-template\nImplementation of Hypermodern Python repo (https://cjolowicz.github.io/posts/hypermodern-python-01-setup/)\n',
    'author': 'Zach Gallagher',
    'author_email': 'zachagallagher@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
