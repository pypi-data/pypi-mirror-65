# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['django_command_overrides',
 'django_command_overrides.conf',
 'django_command_overrides.management',
 'django_command_overrides.management.commands',
 'django_command_overrides.migrations']

package_data = \
{'': ['*'],
 'django_command_overrides.conf': ['app_template/*',
                                   'app_template/migrations/*',
                                   'app_template/models/*',
                                   'app_template/tests/*',
                                   'app_template/views/*']}

install_requires = \
['django>=2.2']

setup_kwargs = {
    'name': 'django-command-overrides',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Jonathan Meier',
    'author_email': 'jonathanwmeier@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
