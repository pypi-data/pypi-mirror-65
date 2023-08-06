# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['google_music', 'google_music.clients']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.0,<2.0',
 'audio-metadata>=0.10',
 'google-music-proto>=2.8.0,<3.0.0',
 'httpx>=0.11,<1.0',
 'oauthlib>=3.0,<4.0',
 'protobuf>=3.5,<4.0',
 'tbm-utils>=2.4,<3.0',
 'tenacity>=5.0,<7.0',
 'wrapt>=1.0,<2.0']

extras_require = \
{'dev': ['flake8>=3.5,<4.0',
         'flake8-builtins>=1.0,<2.0',
         'flake8-comprehensions>=2.0,<=4.0',
         'flake8-import-order>=0.18,<0.19',
         'flake8-import-order-tbm>=1.0,<2.0',
         'nox>=2019,<2020',
         'sphinx>=2.0,<3.0',
         'sphinx-material<1.0.0'],
 'doc': ['sphinx>=2.0,<3.0', 'sphinx-material<1.0.0'],
 'lint': ['flake8>=3.5,<4.0',
          'flake8-builtins>=1.0,<2.0',
          'flake8-comprehensions>=2.0,<=4.0',
          'flake8-import-order>=0.18,<0.19',
          'flake8-import-order-tbm>=1.0,<2.0']}

setup_kwargs = {
    'name': 'google-music',
    'version': '3.6.0',
    'description': 'A Google Music API wrapper.',
    'long_description': '# google-music\n\n[![PyPI](https://img.shields.io/pypi/v/google-music.svg?label=PyPI)](https://pypi.org/project/google-music/)\n![](https://img.shields.io/badge/Python-3.6%2B-blue.svg)  \n[![GitHub CI](https://img.shields.io/github/workflow/status/thebigmunch/google-music/CI?label=GitHub%20CI)](https://github.com/thebigmunch/google-music/actions?query=workflow%3ACI)  \n[![Docs - Stable](https://img.shields.io/readthedocs/google-music/stable.svg?label=Docs%20%28Stable%29)](https://google-music.readthedocs.io/en/stable/)\n[![Docs - Latest](https://img.shields.io/readthedocs/google-music/latest.svg?label=Docs%20%28Latest%29)](https://google-music.readthedocs.io/en/latest/)\n\n[google-music](https://github.com/thebigmunch/google-music) is an API wrapper library for Google Music using my sans-I/O library,\n[google-music-proto](https://github.com/thebigmunch/google-music-proto).\n\n\n## Installation\n\n``pip install -U google-music``\n\n\n## Usage\n\nFor the release version, see the [stable docs](https://google-music.readthedocs.io/en/stable/).  \nFor the development version, see the [latest docs](https://google-music.readthedocs.io/en/latest/).\n\n\n## Appreciation\n\nShowing appreciation is always welcome.\n\n#### Thank\n\n[![Say Thanks](https://img.shields.io/badge/thank-thebigmunch-blue.svg?style=flat-square)](https://saythanks.io/to/thebigmunch)\n\nGet your own thanks inbox at [SayThanks.io](https://saythanks.io/).\n\n#### Contribute\n\n[Contribute](https://github.com/thebigmunch/google-music/blob/master/.github/CONTRIBUTING.md) by submitting bug reports, feature requests, or code.\n\n#### Help Others/Stay Informed\n\n[Discourse forum](https://forum.thebigmunch.me/)\n\n#### Referrals/Donations\n\n[![Digital Ocean](https://img.shields.io/badge/Digital_Ocean-referral-orange.svg?style=flat-square)](https://bit.ly/DigitalOcean-tbm-referral) [![Namecheap](https://img.shields.io/badge/Namecheap-referral-orange.svg?style=flat-square)](http://bit.ly/Namecheap-tbm-referral) [![PayPal](https://img.shields.io/badge/PayPal-donate-brightgreen.svg?style=flat-square)](https://bit.ly/PayPal-thebigmunch)\n',
    'author': 'thebigmunch',
    'author_email': 'mail@thebigmunch.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/thebigmunch/google-music',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
