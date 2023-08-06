# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['kbase_workspace_client']

package_data = \
{'': ['*']}

install_requires = \
['biopython>=1.76,<2.0', 'requests>=2']

setup_kwargs = {
    'name': 'kbase-workspace-client',
    'version': '0.0.2',
    'description': 'KBase Workspace Client and Utilities',
    'long_description': None,
    'author': 'KBase Team',
    'author_email': 'info@kbase.us',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.7,<4.0.0',
}


setup(**setup_kwargs)
