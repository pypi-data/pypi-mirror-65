# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tamr_client',
 'tamr_client.attributes',
 'tamr_client.datasets',
 'tamr_unify_client',
 'tamr_unify_client.attribute',
 'tamr_unify_client.auth',
 'tamr_unify_client.categorization',
 'tamr_unify_client.categorization.category',
 'tamr_unify_client.dataset',
 'tamr_unify_client.mastering',
 'tamr_unify_client.mastering.published_cluster',
 'tamr_unify_client.project',
 'tamr_unify_client.project.attribute_configuration',
 'tamr_unify_client.project.attribute_mapping']

package_data = \
{'': ['*']}

install_requires = \
['dataclasses>=0.6.0,<0.7.0',
 'pandas>=1.0.3,<2.0.0',
 'requests>=2.22,<3.0',
 'simplejson>=3.16,<4.0']

setup_kwargs = {
    'name': 'tamr-unify-client',
    'version': '0.11.1',
    'description': 'Python Client for the Tamr API',
    'long_description': "# Python Client\nProgrammatically 💻 interact with Tamr using Python 🐍\n\n[![Version](https://img.shields.io/pypi/v/tamr-unify-client.svg?style=flat-square)](https://pypi.org/project/tamr-unify-client/)\n[![Documentation Status](https://readthedocs.org/projects/tamr-client/badge/?version=stable&style=flat-square)](https://tamr-client.readthedocs.io/en/stable/?badge=stable)\n[![Build Status](https://img.shields.io/github/workflow/status/Datatamer/tamr-client/CI?&style=flat-square)](https://github.com/Datatamer/tamr-client/actions?query=workflow%3ACI)\n![Supported Python Versions](https://img.shields.io/pypi/pyversions/tamr-unify-client.svg?style=flat-square)\n[![License](https://img.shields.io/pypi/l/tamr-unify-client.svg?style=flat-square)](LICENSE)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/ambv/black)\n\n---\n\n*Quick links:*\n**[Docs](https://tamr-client.readthedocs.io/en/stable/)** |\n**[Contributing](https://tamr-client.readthedocs.io/en/stable/contributor-guide.html)** |\n**[Change Log](https://github.com/Datatamer/tamr-client/blob/master/CHANGELOG.md)** |\n**[License](https://github.com/Datatamer/tamr-client/blob/master/LICENSE)**\n\n---\n\n## Install\n\n```sh\npip install tamr-unify-client\n```\n\n## Features\n- 🐍 Python objects/methods/functions instead of raw HTTP requests\n- 🤖 Automate operational workflows\n  - Continuous Mastering\n  - Continuous Categorization\n- 🚀 Kick-off synchronous/asynchronous operations\n  - Refresh datasets in your pipeline\n  - Train Tamr's machine learning models\n  - Generate predictions from trained models\n- 🔒 Authenticate with Tamr\n\nFor more see the [official docs](https://tamr-client.readthedocs.io/en/stable/).\n\n## Maintainers\n\n- [Pedro Cattori](https://github.com/pcattori)\n",
    'author': 'Pedro Cattori',
    'author_email': 'pedro.cattori@tamr.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://tamr-client.readthedocs.io/en/stable/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
