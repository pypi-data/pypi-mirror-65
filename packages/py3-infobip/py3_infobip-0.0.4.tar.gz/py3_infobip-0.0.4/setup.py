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
    'version': '0.0.4',
    'description': 'A python3 client for the infobip service',
    'long_description': "# Infobip Python3 client\n[![PyPI version](https://badge.fury.io/py/py3-infobip.svg)](https://pypi.org/project/py3-infobip/)\n[![PyPI pyversions](https://img.shields.io/pypi/pyversions/py3-infobip.svg)](https://pypi.org/project/py3-infobip/)\n[![PyPI license](https://img.shields.io/pypi/l/py3-infobip.svg)](https://pypi.org/project/py3-infobip/)\n\n## Description\n\nA simple python3 client for [infobip service](https://www.infobip.com/)\n\nInfobip is a client communication service with a [REST api](https://dev.infobip.com/), sadly they do not have an python3 client and my attemp to use the 2to3 library to transform the [infobip python2 client](https://github.com/infobip/infobip-api-python-client) failed.\n\nThis is why a simple python3 client that could consume the infobip API functionalities was needed\n\n## Dependencies\n\n- Python3.7+\n\n## Installation\n\n```\npip install py3-infobip\n```\n\n## Getting Started\n\nIf you want to send a text sms to your clients all you need is a list of phone numbers and the message you want to send.  \n\n```\nfrom py3_infobip import (\n    SmsClient,\n    SmsTextSimpleBody\n)\n\nmessage = SmsTextSimpleBody()\nmessage \\\n    .set_to([\n        '<phone_number>'\n    ]) \\\n    .set_text('some text')\n\ninfobip_client = SmsClient(\n    url='<infobip_url>',\n    api_key='<infobip_apikey>'\n)\nresponse = infobip_client.send_sms_text_simple(message)\nprint(response.json())\n```\n",
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
