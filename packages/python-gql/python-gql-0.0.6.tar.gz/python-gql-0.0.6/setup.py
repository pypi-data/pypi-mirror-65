# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gql', 'gql.cli']

package_data = \
{'': ['*']}

install_requires = \
['click>=7,<8', 'graphql-core>=3,<4']

entry_points = \
{'console_scripts': ['gqlgen = gql.cli.main:main']}

setup_kwargs = {
    'name': 'python-gql',
    'version': '0.0.6',
    'description': 'Python schema-first and auto-generate class graphql server',
    'long_description': '# python-gql\n\nSchema-first python graphql library.\n\n## Install\n\n`pip install python-gql`\n\n## Use `gqlgen` command.\n\n### generate types\n\n`gqlgen ./schema.graphql types --kind=dataclass`\n\n### generator resolver\n\n`gqlgen ./schema.graphql resolver Query hello`\n\n### help info\n\nFor more info about `gqlgen`, please use `gqlgen -h`\n',
    'author': 'ysun',
    'author_email': 'sunyu418@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
