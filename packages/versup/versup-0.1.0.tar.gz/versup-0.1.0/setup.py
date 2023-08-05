# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['versup']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0',
 'colorama>=0.4.3,<0.5.0',
 'gitpython>=3.0,<4.0',
 'pytest-cov>=2.8,<3.0',
 'semver>=2.8,<3.0']

entry_points = \
{'console_scripts': ['versup = versup.__main__:main']}

setup_kwargs = {
    'name': 'versup',
    'version': '0.1.0',
    'description': '',
    'long_description': 'versup\n======\n\nMIT license\n\n** Still in early stages, so use with caution **\n\nBump your project version, update version numbers in your files, create a changelog,\nmake a commit, and tag it, all in one easy step. versup is also quite configurable.\n\nInstall\n=======\n\nInstall with either poetry\n\n`poetry install`\n\nor pip\n\n`pip install .`\n\nQuick start\n===========\n\nTo get started all versup needs to know is the new version increment or number.\nYou can provide it with a valid semantic version increase such as `patch`, `minor`,\n`major` etc, or an entirely new semantic version like `1.2.5`.\n\nIf you specifiy a version number, then versup will take that version and apply\nit to the current project as is. If you provide an increment, it will get the\nlast version number from either the latest git tag that has a valid version,\nor from the default version in the config file.\n\n',
    'author': 'Sven Steinbauer',
    'author_email': 'sven@unlogic.co.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/unlogic/versup',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
