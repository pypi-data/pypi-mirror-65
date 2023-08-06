# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['snow',
 'snow.request',
 'snow.request.core',
 'snow.request.helpers',
 'snow.resource',
 'snow.resource.fields',
 'snow.resource.query']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.6.2,<4.0.0', 'marshmallow>=3.2.2,<4.0.0', 'ujson>=1.35,<2.0']

setup_kwargs = {
    'name': 'snow',
    'version': '0.2.2',
    'description': 'Python library for ServiceNow',
    'long_description': '<p align="center">\n  <img width="256" height="256" src="extras/images/logo-gh.png">\n  <br><br>\n  <b>Python library for ServiceNow</b><br>\n</p>\n\n[![image](https://badgen.net/pypi/v/snow)](https://pypi.org/project/snow)\n[![image](https://badgen.net/badge/python/3.7+?color=purple)](https://pypi.org/project/snow)\n[![image](https://badgen.net/travis/rbw/snow)](https://travis-ci.org/rbw/snow)\n[![image](https://badgen.net/pypi/license/snow)](https://raw.githubusercontent.com/rbw/snow/master/LICENSE)\n[![image](https://pepy.tech/badge/snow/month)](https://pepy.tech/project/snow)\n\n\nSnow is a simple and lightweight yet powerful and extensible library for interacting with ServiceNow. It works\nwith modern versions of Python and utilizes [asyncio](https://docs.python.org/3/library/asyncio.html).\n\nDocumentation\n---\n\nThe Snow API reference, examples and more is available in the [documentation](https://python-snow.readthedocs.io/en/latest).\n\nDevelopment status\n---\n\nPre-alpha\n\nContributing\n---\n\nCheck out the [contributing guidelines](CONTRIBUTING.md) if you want to help out with code or documentation.\n\n\nFunding\n-------\n\nThe Snow code is permissively licensed, and can be incorporated into any type of application–commercial or otherwise–without costs or limitations.\nIts author believes it\'s in the commercial best-interest for users of the project to invest in its ongoing development.\n\nConsider leaving a [donation](https://paypal.vault13.org) if you like this software, it will:\n\n- Directly contribute to faster releases, more features, and higher quality software.\n- Allow more time to be invested in documentation, issue triage, and community support.\n- Safeguard the future development of Snow.\n\nAuthor\n------\n\nRobert Wikman \\<rbw@vault13.org\\>\n\n\n',
    'author': 'Robert Wikman',
    'author_email': 'rbw@vault13.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rbw/snow',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
