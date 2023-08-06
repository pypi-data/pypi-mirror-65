# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['flake8_pytestrail']
install_requires = \
['attrs>=19.2.0', 'flake8>=3.0.0']

entry_points = \
{'flake8.extension': ['TR = flake8_pytestrail:PyTestRailChecker']}

setup_kwargs = {
    'name': 'flake8-pytestrail',
    'version': '0.2.0',
    'description': 'Flake8 plugin to check for missing or wrong TestRail test identifiers',
    'long_description': '# flake8-pytestrail\n\nA companion Flake8 plugin for [pytest-testrail](https://github.com/allankp/pytest-testrail) package.\n\n## Installation\n\n```\npip install flake8-pytestrail\n```\n\nor if you use [poetry](https://python-poetry.org/):\n\n```\npoetry add --dev flake8-pytestrail\n```\n\n## Usage\n\n> ⚠️ At the moment plugin assumes that you use\n> default `pytest` configuration (test files\n> are all can be matched by `**/test_*.py` glob).\n> It also assumes that you want all test cases to have\n> been registered inside of TestRail and have ID.\n\n```\nflake8 .\n```\n\n## Error list\n\n* TR001 Missing `@pytestrail.case()` decorator\n* TR002 Multiple `@pytestrail.case()` decorators\n* TR003 Test case ID should match `"^C\\d+$"` pattern\n\n## Configuration\n\nThere is no way to configure the plugin at the moment.\n',
    'author': 'Andrey Semakin',
    'author_email': 'and-semakin@ya.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/and-semakin/flake8-pytestrail',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
