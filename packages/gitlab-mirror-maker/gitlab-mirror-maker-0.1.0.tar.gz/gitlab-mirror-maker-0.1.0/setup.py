# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mirrormaker']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.1,<8.0.0', 'requests>=2.23.0,<3.0.0']

entry_points = \
{'console_scripts': ['gitlab-mirror-maker = '
                     'mirrormaker.mirrormaker:mirrormaker']}

setup_kwargs = {
    'name': 'gitlab-mirror-maker',
    'version': '0.1.0',
    'description': 'GitLab Mirror Maker - Automatically mirror your repositories from GitLab to GitHub',
    'long_description': None,
    'author': 'Grzegorz Dlugoszewski',
    'author_email': 'g.dlugoszewski@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
