# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['caboodle']

package_data = \
{'': ['*']}

install_requires = \
['google-cloud-storage>=1.25,<2.0', 'tqdm>=4.41.1,<5.0.0']

setup_kwargs = {
    'name': 'the-whole-caboodle',
    'version': '0.2.6',
    'description': 'Utilities for artifact management for data science in the cloud.',
    'long_description': None,
    'author': 'Saad Khan',
    'author_email': 'skhan8@mail.einstein.yu.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
