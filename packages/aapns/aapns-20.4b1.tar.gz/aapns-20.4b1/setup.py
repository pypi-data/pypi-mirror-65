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
    'version': '20.4b1',
    'description': 'Asynchronous Apple Push Notification Service Client',
    'long_description': '# AAPNS\n\n[![CircleCI](https://circleci.com/gh/HENNGE/aapns.svg?style=svg)](https://circleci.com/gh/HENNGE/aapns)\n[![Documentation Status](https://readthedocs.org/projects/aapns/badge/?version=latest)](http://aapns.readthedocs.io/en/latest/?badge=latest)\n\nAsynchronous Apple Push Notification Service client.\n\n* Requires TLS 1.2 or better\n* Requires Python 3.8 or better\n\n## Quickstart\n\n```python\nfrom aapns.api import create_client\nfrom aapns.config import Priority, Production\nfrom aapns.models import Notification, Alert, Localized\n\nasync def send_hello_world():\n    client = await create_client(\'/path/to/push/cert.pem\', Production)\n    apns_id = await client.send_notification(\n        \'my-device-token\',\n        Notification(\n            alert=Alert(\n                body=Localized(\n                    key=\'Hello World!\',\n                    args=[\'foo\', \'bar\']\n                ),\n            ),\n            badge=42\n        ),\n        priority=Priority.immediately\n    )\n    print(f\'Sent push notification with ID {apns_id}\')\n    await client.close()\n```\n\n### On idempotency\n\nOr how to ensure that a notification is displayed only once in the presence of network errors?\n\nIf the underlying TCP connection is broken or times out, there may be some notifications still in flight. In that case it\'s impossible to tell whether the notification was not yet delivered to the Apple server, or it was delivered but Apple server response was not yet delivered to back to your client.\n\nAdditionally, the server may try to shut down an HTTP/2 connection gracefully, for example for server maintenance or upgrade. In that case, due to https://github.com/python-hyper/hyper-h2/issues/1181, it is not possible to tell which of the in-flight requests will be completed by the server.\n\nThe Apple push notification protocol provides a header field `apns-collapse-id`. In the simple use-case, it\'s recommended to set this field, for example to a random value:\n\n```py\nawait client.send_notification(\n    ...,\n    collapse_id=str(random.random()),\n)\n```\n\nThen, should `aapns` need to retransmit the request, and retransmit "one time too many", the end user will only see a single notification.\n\nHowever, if you are rely on notification collapse mechanism, if `aapns` retransmits, the notifications may arrive out of order, and the end-user may ultimately see stale data.\n\n### Mid level API\n\nUse this API to maintain a fixed size connection pool and gain automatic retries with exponential back-off. A connection pool can handle up to `1000 * size` (current Apple server limit) concurrent requests and practically unlimited dumb queue of requests should concurrency limit be exceeded. It is thus suitable for bursty traffic.\n\nUse this API to send notification en masse or generic RPC-like communication over HTTP/2.\n\n```py\nfrom aapns.errors import APNSError, Closed, Timeout\nfrom aapns.pool import create_ssl_context, Pool, Request\n\n\nssl_context = create_ssl_context()\nssl_context.load_cert_chain(certfile=..., keyfile=...)\n\nreq = Request.new(\n    "/3/device/42...42",\n    {"apns-push-type": "alert", "apns-topic": "com.app.your"},\n    {"apns": {"alert": {"body": "Wakey-wakey, ham and bakey!"}}},\n    timeout=10,  # or the pool may retry forever\n)\n\nasync with Pool(\n        "https://api.development.push.apple.com",\n        size=10,  # default\n        ssl=ssl_context) as pool:\n    try:\n        resp = await pool.post(req)\n        assert resp.code == 200\n    except Timeout:\n        ...  # the notification has expired\n    except Closed:\n        ...  # the connection pool is done, e.g. if client certificate has expired\n    except APNSError:\n        ...  # rare\n```\n\n### Low level API\n\nUse this API if you want close control of a single connection to the server. A connection can handle up to `1000` concurrent requests (current Apple server limit) and up to `2**31` requests in total (HTTP/2 protocol limit).\n\nThis would be a good start for token authentication, https://github.com/HENNGE/aapns/issues/19.\n\n```py\nfrom aapns.errors import APNSError, Blocked, Closed, Timeout\nfrom aapns.connection import create_ssl_context, Connection, Request\n\n\nssl_context = create_ssl_context()\nssl_context.load_cert_chain(certfile=..., keyfile=...)\n\nreq = Request.new(\n    "/3/device/42...42",\n    {"apns-push-type": "alert", "apns-topic": "com.app.your"},\n    {"apns": {"alert": {"body": "Wakey-wakey, ham and bakey!"}}},\n    timeout=10)\n\nasync with Connection(\n        "https://api.development.push.apple.com",\n        ssl=ssl_context) as conn:\n    try:\n        resp = await conn.post(req)\n        assert resp.code == 200\n    except Blocked:\n        ...  # the connection is busy, try again later\n    except Closed:\n        ...  # the connection is no longer usable\n    except Timeout:\n        ...  # the notification has expired\n    except APNSError:\n        ...  # rare\n```\n\n### Technical notes\n\nRationale for using raw https://github.com/python-hyper/hyper-h2 rather than an existing library, like https://github.com/encode/httpx.\n\nContrast push notification use-case vs. generic, browser-like use-case:\n\n| feature                   | push-like | browser-like                        |\n|:--------------------------|:----------|:------------------------------------|\n| request size              | tiny      | small or large                      |\n| request method            | `POST`    | `OPTIONS,HEAD,GET,PUT,POST`,custom  |\n| response size             | tiny      | small, large, giant, streamed       |\n| server push               | no        | possible                            |\n| concurrent per connection | `1000`    | dozens                              |\n| total per connection      | millions  | dozens                              |\n| retryable                 | all       | idempotent verbs, graceful shutdown |\n| servers                   | `1`       | many                                |\n| authorisation             | client cert or token | none, token, other       |\n\n* Apple server sets max concurrent requests to `1000` and push requests are small (5KB max), thus TCP send buffer will be quite small, thus:\n  * we\'re not setting `TCP_NOTSENT_LOWAT`\n  * we\'re not checking `SO_NWRITE/SIOCOUTQ`\n* APN server is available on IPv4 only today, thus we don\'t worry about happy eyeballs\n',
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
