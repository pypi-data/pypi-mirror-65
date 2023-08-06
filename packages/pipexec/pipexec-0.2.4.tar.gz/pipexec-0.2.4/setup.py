# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pipexec']

package_data = \
{'': ['*']}

install_requires = \
['cleo>=0.8.0,<0.9.0']

entry_points = \
{'console_scripts': ['pipexec = pipexec:main']}

setup_kwargs = {
    'name': 'pipexec',
    'version': '0.2.4',
    'description': 'Test pip packages quickly',
    'long_description': '## Pipexec\n\nTry out pip packages quickly\n\n## Install\n\n```shell\npip install pipexec\n```\n\n### Usage\n\nRun `pipexec <package-name>` to start the interactive shell, where `<package-name>` is any valid pip package. Example:\n\n```shell\npipexec pendulum\n```\n',
    'author': 'Amos Omondi',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/amos-o/pipexec',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.9',
}


setup(**setup_kwargs)
