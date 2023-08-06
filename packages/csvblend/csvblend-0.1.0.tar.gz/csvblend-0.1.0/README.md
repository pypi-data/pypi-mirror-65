# csvblend: Python CSV Merge Library

[![Travis (.org)](https://img.shields.io/travis/rwanyoike/csvblend.svg)](https://travis-ci.org/rwanyoike/csvblend)
[![Codecov](https://img.shields.io/codecov/c/gh/rwanyoike/csvblend.svg)](https://codecov.io/gh/rwanyoike/csvblend)
[![GitHub](https://img.shields.io/github/license/rwanyoike/csvblend)](LICENSE)
[![PyPI](https://img.shields.io/pypi/v/csvblend.svg)](https://pypi.python.org/pypi/csvblend)
[![Code Style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

> Join or merge multiple CSVs.

csvblend is a _memory constant_ Python library to merge multiple CSVs based on a list of columns.

NOTE: csvblend requires SQLite version 3.24.0 (2018-06-04) or better: `python -c 'import sqlite3; print(sqlite3.sqlite_version)'`

Basic merge usage:

```python
>>> from csvblend import MergeFiles
>>> columns = ["a", "b", "c"]
>>> indexes = ["a"]
>>> with MergeFiles(columns, indexes) as mf:
...     mf.merge(open(csvfile1))
...     mf.merge(open(csvfile2))
...     mf.merge(open(csvfile3))
...     for row in mf.rows():
...         print(row)
```

[Features](#features) | [Installation](#installation) | [Usage](#usage) | [Contributing](#contributing) | [License](#license)

## Features

- [SQLite](https://www.sqlite.org) (RDBMS) under the hood.
- Affected row count (created or updated) - useful to show changes between CSVs.
- No external dependencies.

csvblend officially supports Python 3.6+.

## Installation

To install csvblend, simply run:

```shell
$ pip install -U csvblend
✨🖇✨
```

## Usage

For documentation, see [`./docs/README.md`](./docs/README.md).

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the [MIT License](./LICENSE).
