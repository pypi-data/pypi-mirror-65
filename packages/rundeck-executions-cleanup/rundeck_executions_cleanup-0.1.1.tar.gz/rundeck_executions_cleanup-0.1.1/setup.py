# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rundeck_executions_cleanup']

package_data = \
{'': ['*']}

install_requires = \
['click-log>=0.3.2,<0.4.0', 'click>=7.1.1,<8.0.0', 'requests>=2.23.0,<3.0.0']

entry_points = \
{'console_scripts': ['rundeck-executions-cleanup = '
                     'rundeck_executions_cleanup:main']}

setup_kwargs = {
    'name': 'rundeck-executions-cleanup',
    'version': '0.1.1',
    'description': 'Python CLI to remove old Rundeck executions and log files',
    'long_description': '',
    'author': 'Lucas Souto',
    'author_email': 'lucassouto@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/instruct-br/rundeck-executions-cleanup',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
