# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['csvblend']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'csvblend',
    'version': '0.1.0',
    'description': 'Join or merge multiple CSVs.',
    'long_description': '# csvblend: Python CSV Merge Library\n\n[![Travis (.org)](https://img.shields.io/travis/rwanyoike/csvblend.svg)](https://travis-ci.org/rwanyoike/csvblend)\n[![Codecov](https://img.shields.io/codecov/c/gh/rwanyoike/csvblend.svg)](https://codecov.io/gh/rwanyoike/csvblend)\n[![GitHub](https://img.shields.io/github/license/rwanyoike/csvblend)](LICENSE)\n[![PyPI](https://img.shields.io/pypi/v/csvblend.svg)](https://pypi.python.org/pypi/csvblend)\n[![Code Style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n> Join or merge multiple CSVs.\n\ncsvblend is a _memory constant_ Python library to merge multiple CSVs based on a list of columns.\n\nNOTE: csvblend requires SQLite version 3.24.0 (2018-06-04) or better: `python -c \'import sqlite3; print(sqlite3.sqlite_version)\'`\n\nBasic merge usage:\n\n```python\n>>> from csvblend import MergeFiles\n>>> columns = ["a", "b", "c"]\n>>> indexes = ["a"]\n>>> with MergeFiles(columns, indexes) as mf:\n...     mf.merge(open(csvfile1))\n...     mf.merge(open(csvfile2))\n...     mf.merge(open(csvfile3))\n...     for row in mf.rows():\n...         print(row)\n```\n\n[Features](#features) | [Installation](#installation) | [Usage](#usage) | [Contributing](#contributing) | [License](#license)\n\n## Features\n\n- [SQLite](https://www.sqlite.org) (RDBMS) under the hood.\n- Affected row count (created or updated) - useful to show changes between CSVs.\n- No external dependencies.\n\ncsvblend officially supports Python 3.6+.\n\n## Installation\n\nTo install csvblend, simply run:\n\n```shell\n$ pip install -U csvblend\n✨🖇✨\n```\n\n## Usage\n\nFor documentation, see [`./docs/README.md`](./docs/README.md).\n\n## Contributing\n\nPull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.\n\n## License\n\nThis project is licensed under the [MIT License](./LICENSE).\n',
    'author': 'Raymond Wanyoike',
    'author_email': 'raymond.wanyoike@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rwanyoike/csvblend',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
