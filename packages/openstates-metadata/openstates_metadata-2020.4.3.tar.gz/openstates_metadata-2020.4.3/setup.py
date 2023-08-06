# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['openstates_metadata',
 'openstates_metadata.data',
 'openstates_metadata.tests']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=19.3,<20.0']

setup_kwargs = {
    'name': 'openstates-metadata',
    'version': '2020.4.3',
    'description': 'metadata for the openstates project',
    'long_description': '# metadata\n\nThis repository contains state metadata that powers Open States.\n\n[![CircleCI](https://circleci.com/gh/openstates/metadata.svg?style=svg)](https://circleci.com/gh/openstates/metadata)\n\n## Links\n\n* [Open States Discourse](https://discourse.openstates.org)\n* [Code of Conduct](https://docs.openstates.org/en/latest/contributing/code-of-conduct.html)\n\n## Changelog\n\nReleases use YYYY.MM.patch versioning.\n\n### 2020.04.3\n\n* add executive_organization_id and executive_name to State\n\n### 2020.04.2 - Apr 8 2020\n\n* fix unicameral legislature ids\n\n### 2020.04.1 - Apr 8 2020\n\n* add State.legislature_organization_id\n\n### 2020.02.2 - Feb 6 2020\n\n* lower minimum Python version to 3.6\n\n### 2020.02.1 - Feb 5 2020\n\n* remove unnecessary dependencies\n* add lookup by name option\n\n### 2020.01.31 - Jan 31 2020\n\n* added organization_ids to chambers\n* added legacy_districts for states with district changes since 2010\n\n### 2020.01.16 - Jan 15 2020\n\n* Added helper methods.\n\n### 2020.01.15 - Jan 15 2020\n\n* First release, basic functionality.\n',
    'author': 'James Turk',
    'author_email': 'james@openstates.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/openstates/metadata',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
