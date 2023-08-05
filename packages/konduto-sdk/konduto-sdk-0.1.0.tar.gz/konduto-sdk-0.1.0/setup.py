# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['konduto',
 'konduto.api',
 'konduto.api.clients',
 'konduto.api.clients.v1',
 'konduto.api.resources',
 'konduto.api.resources.requests',
 'konduto.api.resources.response',
 'konduto.infrastructure']

package_data = \
{'': ['*']}

install_requires = \
['dacite>=1.3.0,<2.0.0', 'requests>=2.16.0,<3.0.0']

setup_kwargs = {
    'name': 'konduto-sdk',
    'version': '0.1.0',
    'description': 'SDK to let the process easier to integrate your application with konduto rest API',
    'long_description': '<img src="https://user-images.githubusercontent.com/9020828/78465897-9a77b400-76d1-11ea-9551-1a4db4b1a910.png" align="left" width="192px" height="192px"/>\n<img align="left" width="0" height="192px" hspace="10"/>\n\n[![codecov](https://codecov.io/gh/alefhsousa/konduto-sdk/branch/master/graph/badge.svg)](https://codecov.io/gh/alefhsousa/konduto-sdk)\n![ci](https://github.com/alefhsousa/konduto-sdk/workflows/ci/badge.svg)\n<a href="https://github.com/alefhsousa/konduto-sdk/blob/master/LICENSE"><img alt="License: MIT" src="https://img.shields.io/github/license/alefhsousa/konduto-sdk"></a>\n[![Codacy Badge](https://api.codacy.com/project/badge/Grade/57e4534797c7416b86c20c4ec5d53067)](https://www.codacy.com/manual/alefhsousa/konduto-sdk?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=alefhsousa/konduto-sdk&amp;utm_campaign=Badge_Grade)\nA Python SDK for integrating with the [Konduto rest api][1]. Compatible with python 3.6+, this repo not is a official repository from Konduto.\nFeel free to contribute with the project.\n\n### Getting Started\n\nSetup a local environment:\n\nI expected that you already python3 installed in your machine\n\n```bash\n$ make setup\n```\n\n### Running tests\nThe CI command that setups all requirements and runs tests to assure everything is configured accordingly.\n\n```bash\n$ make test\n```\n\n### License\n\nCopyright Alefh Sousa 2020.\n\nDistributed under the terms of the [MIT][2] license, konduto-sdk is free and open source software.\n\n[1]: http://docs.konduto.com/en/\n[2]: https://github.com/alefhsousa/konduto-sdk/blob/master/LICENSE\n',
    'author': 'Alefh Sousa',
    'author_email': 'alefh.sousa@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/alefhsousa/konduto-sdk',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
