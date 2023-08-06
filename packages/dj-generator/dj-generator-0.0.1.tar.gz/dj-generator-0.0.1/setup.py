# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dj_generator',
 'dj_generator.management.commands',
 'dj_generator.migrations',
 'dj_generator.templates.dj_generator.curd.default.code',
 'dj_generator.templates.dj_generator.curd.power.code',
 'dj_generator.templatetags']

package_data = \
{'': ['*'],
 'dj_generator': ['templates/dj_generator/curd/default/templates/*',
                  'templates/dj_generator/curd/power/templates/*']}

install_requires = \
['django>=3.0.5,<4.0.0']

setup_kwargs = {
    'name': 'dj-generator',
    'version': '0.0.1',
    'description': 'Boilerplate generator for django',
    'long_description': '# dj-generator\nA lot of our time we spend on creating CURD in django. This project aims to generate boilerplate code to reduce our valuable time.\n\nThe django templating system is pretty powerful. We can make use of the power of templating tool to generate basic CURD given a model.\n\n## Assumptions\nThis project assumes that you follow certain folder structure. That makes this project to stay as simple as possible.\n\n\n## Usage\nPattern -\n```sybase\npython manage.py generate app.Model --template power\n```\n\nFor example if you run following command -\n```sybase\npython manage.py generate testapp.Task --template power\n```\n\nIt will create -\n- CRUD python files under ``testapp/task`` folder.\n- CRUD template files under ``testapp/templates/testapp/task`` folder.\n\n',
    'author': 'Shimul Chowdhury',
    'author_email': 'shimul@divine-it.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/shimulch/dj-generator',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
