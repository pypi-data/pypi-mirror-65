# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fourutils',
 'fourutils.asynchronous',
 'fourutils.flask',
 'fourutils.flask.testing',
 'fourutils.ldap',
 'fourutils.sqla',
 'fourutils.sqla.mixins',
 'fourutils.sqla.types',
 'fourutils.webnotifications']

package_data = \
{'': ['*']}

install_requires = \
['sentry-sdk>=0,<1']

setup_kwargs = {
    'name': 'fourutils',
    'version': '0.2.1',
    'description': '',
    'long_description': None,
    'author': 'Oscar Rainford',
    'author_email': 'oscar@fourbs.com.au',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
