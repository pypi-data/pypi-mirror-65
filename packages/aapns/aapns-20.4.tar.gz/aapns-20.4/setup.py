# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['aapns']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=19.3.0,<20.0.0', 'h2>=3.2.0,<4.0.0']

extras_require = \
{'cli': ['click>=7.0,<8.0']}

entry_points = \
{'console_scripts': ['aapns = aapns.cli:main']}

setup_kwargs = {
    'name': 'aapns',
    'version': '20.4',
    'description': 'Asynchronous Apple Push Notification Service Client',
    'long_description': "# AAPNS\n\n[![CircleCI](https://circleci.com/gh/HENNGE/aapns.svg?style=svg)](https://circleci.com/gh/HENNGE/aapns)\n[![Documentation Status](https://readthedocs.org/projects/aapns/badge/?version=latest)](http://aapns.readthedocs.io/en/latest/?badge=latest)\n\nAsynchronous Apple Push Notification Service client.\n\n* Requires TLS 1.2 or better\n* Requires Python 3.8 or better\n\n## Quickstart\n\n```python\nfrom aapns.api import create_client\nfrom aapns.config import Priority, Production\nfrom aapns.models import Notification, Alert, Localized\n\nasync def send_hello_world():\n    client = await create_client('/path/to/push/cert.pem', Production)\n    apns_id = await client.send_notification(\n        'my-device-token',\n        Notification(\n            alert=Alert(\n                body=Localized(\n                    key='Hello World!',\n                    args=['foo', 'bar']\n                ),\n            ),\n            badge=42\n        ),\n        priority=Priority.immediately\n    )\n    print(f'Sent push notification with ID {apns_id}')\n    await client.close()\n```\n",
    'author': 'Jonas Obrist',
    'author_email': 'jonas.obrist@hennge.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/HENNGE/aapns',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
