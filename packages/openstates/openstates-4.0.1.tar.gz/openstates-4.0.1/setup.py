# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['openstates',
 'openstates.cli',
 'openstates.cli.tests',
 'openstates.data',
 'openstates.data.admin',
 'openstates.data.management',
 'openstates.data.management.commands',
 'openstates.data.migrations',
 'openstates.data.models',
 'openstates.data.tests',
 'openstates.importers',
 'openstates.importers.tests',
 'openstates.reports',
 'openstates.reports.migrations',
 'openstates.scrape',
 'openstates.scrape.schemas',
 'openstates.scrape.tests',
 'openstates.utils',
 'openstates.utils.tests']

package_data = \
{'': ['*']}

install_requires = \
['Django>=2.2',
 'dj_database_url>=0.5.0,<0.6.0',
 'jsonschema>=3.2.0,<4.0.0',
 'psycopg2-binary>=2.8.4,<3.0.0',
 'pytz>=2019.3,<2020.0',
 'scrapelib>=1.2.0,<2.0.0']

entry_points = \
{'console_scripts': ['os-update = openstates.cli.update:main']}

setup_kwargs = {
    'name': 'openstates',
    'version': '4.0.1',
    'description': 'core infrastructure for the openstates project',
    'long_description': None,
    'author': 'James Turk',
    'author_email': 'james@openstates.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
