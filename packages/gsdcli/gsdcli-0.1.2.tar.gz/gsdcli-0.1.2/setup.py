# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gsdcli']

package_data = \
{'': ['*']}

install_requires = \
['Click>=7.1.1,<8.0.0']

entry_points = \
{'console_scripts': ['gsd-cli = gsdcli.gsdcli:gsdcli']}

setup_kwargs = {
    'name': 'gsdcli',
    'version': '0.1.2',
    'description': 'A cli for installing game servers',
    'long_description': None,
    'author': 'egee-irl',
    'author_email': 'brian@egee.io',
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
