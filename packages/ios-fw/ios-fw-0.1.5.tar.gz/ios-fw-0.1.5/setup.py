# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['packers']

package_data = \
{'': ['*']}

modules = \
['cli']
install_requires = \
['click>=7.1.1,<8.0.0',
 'coloredlogs>=14.0,<15.0',
 'construct>=2.10.56,<3.0.0',
 'simpleelf>=0.1.3,<0.2.0']

entry_points = \
{'console_scripts': ['ios-fw = cli:main']}

setup_kwargs = {
    'name': 'ios-fw',
    'version': '0.1.5',
    'description': 'IOS firmware utilities',
    'long_description': None,
    'author': 'Charlie Brown',
    'author_email': 'whysoyum@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
