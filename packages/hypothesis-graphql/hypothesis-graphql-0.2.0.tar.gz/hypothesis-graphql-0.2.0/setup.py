# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['hypothesis_graphql', 'hypothesis_graphql._strategies']

package_data = \
{'': ['*']}

install_requires = \
['graphql-core>=3.1.0,<4.0.0', 'hypothesis>=5.8.0,<6.0.0']

setup_kwargs = {
    'name': 'hypothesis-graphql',
    'version': '0.2.0',
    'description': 'Hypothesis strategies for GraphQL schemas and queries',
    'long_description': None,
    'author': 'Dmitry Dygalo',
    'author_email': 'dadygalo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
