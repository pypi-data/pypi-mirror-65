# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['py3_infobip', 'py3_infobip.utils']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.23.0,<3.0.0']

setup_kwargs = {
    'name': 'py3-infobip',
    'version': '0.0.3',
    'description': '',
    'long_description': None,
    'author': 'Nicolas Cardenas',
    'author_email': 'nicolas.cardenas722@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nico722/infobip-python3-client',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
