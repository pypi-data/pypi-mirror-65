# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jiradumper']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.1,<8.0.0', 'jira>=2.0.0,<3.0.0', 'jsonschema>=3.2.0,<4.0.0']

entry_points = \
{'console_scripts': ['jiradumper = jiradumper.jiradumper:cli']}

setup_kwargs = {
    'name': 'jiradumper',
    'version': '0.2.2',
    'description': '',
    'long_description': None,
    'author': 'Khalid',
    'author_email': 'khalidck@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
