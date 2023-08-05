# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dial_core',
 'dial_core.datasets',
 'dial_core.datasets.datatype',
 'dial_core.node_editor',
 'dial_core.plugin',
 'dial_core.project',
 'dial_core.utils',
 'dial_core.utils.log']

package_data = \
{'': ['*']}

install_requires = \
['dependency-injector>=3.15.6,<4.0.0',
 'tensorflow==2.0.0b1',
 'toml>=0.10.0,<0.11.0']

setup_kwargs = {
    'name': 'dial-core',
    'version': '0.13a0',
    'description': 'Deep Learning, node-based framework',
    'long_description': "# dial-core\nBase framework for the Dial application.\n\n| Build | Coverage | Quality | Version | Python | Docs | License |\n|-------|----------|---------|---------|--------|------|---------|\n| [![Build Status](https://travis-ci.com/dial-app/dial-core.svg?branch=master)](https://travis-ci.com/dial-app/dial-core) | [![codecov](https://codecov.io/gh/dial-app/dial-core/branch/master/graph/badge.svg)](https://codecov.io/gh/dial-app/dial-core) | [![Codacy Badge](https://api.codacy.com/project/badge/Grade/0efd35d1aeb042ba992b573324f52a82)](https://www.codacy.com/gh/dial-app/dial-core?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=dial-app/dial-core&amp;utm_campaign=Badge_Grade) | [![PyPI](https://img.shields.io/pypi/v/dial-core)](https://pypi.org/project/dial-core/) | [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/dial-core?color=green)](https://pypi.org/project/dial-core/) | [![ReadTheDocs](https://readthedocs.org/projects/dial-core/badge/?version=latest)](https://dial-core.readthedocs.io/en/latest/) | [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0) |\n\n## Documentation\n\nThis project's documentation lives at [readthedocs.io](https://dial-core.readthedocs.io).\n\n## License\n\nAll code is provided under the __GPL-3.0__ license. See [LICENSE](LICENSE) for more details.\n\n## Authors\n\n* **David Afonso (davafons)**: [Github](https://github.com/davafons) [Twitter](https://twitter.com/davafons)\n",
    'author': 'David Afonso',
    'author_email': 'davafons@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dial-app/dial-core',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<3.8',
}


setup(**setup_kwargs)
