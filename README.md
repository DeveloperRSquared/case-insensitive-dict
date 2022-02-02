# Case Insensitive Dict

Typed Python Case Insensitive Dictionary

[![Publish](https://github.com/DeveloperRSquared/case-insensitive-dict/actions/workflows/publish.yml/badge.svg)](https://github.com/DeveloperRSquared/case-insensitive-dict/actions/workflows/publish.yml)

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-brightgreen.svg)](#case-insensitive-dict)
[![PyPI - License](https://img.shields.io/pypi/l/case-insensitive-dictionary.svg)](LICENSE)
[![PyPI - Version](https://img.shields.io/pypi/v/case-insensitive-dictionary.svg)](https://pypi.org/project/case-insensitive-dictionary)

[![CodeQL](https://github.com/DeveloperRSquared/case-insensitive-dict/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/DeveloperRSquared/case-insensitive-dict/actions/workflows/codeql-analysis.yml)
[![codecov](https://codecov.io/gh/DeveloperRSquared/case-insensitive-dict/branch/main/graph/badge.svg?token=45JCHX8KT9)](https://codecov.io/gh/DeveloperRSquared/case-insensitive-dict)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/DeveloperRSquared/case-insensitive-dict/main.svg)](https://results.pre-commit.ci/latest/github/DeveloperRSquared/case-insensitive-dict/main)

[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)

## Install

Install and update using [pip](https://pypi.org/project/case-insensitive-dictionary/).

```sh
$ pip install -U case-insensitive-dictionary
```

## API Reference

| Method                    | Description                                                                                                                                         |
| :------------------------ | :-------------------------------------------------------------------------------------------------------------------------------------------------- |
| clear()                   | Removes all elements from the dictionary.                                                                                                           |
| copy()                    | Returns a copy of the dictionary.                                                                                                                   |
| get(key, default)         | Returns the value (case-insensitively), of the item specified with the key.<br>Falls back to the default value if the specified key does not exist. |
| fromkeys(iterable, value) | Returns a dictionary with the specified keys and the specified value.                                                                               |
| keys()                    | Returns the dictionary's keys.                                                                                                                      |
| values()                  | Returns the dictionary's values.                                                                                                                    |
| items()                   | Returns the key-value pairs.                                                                                                                        |
| pop(key)                  | Remove the specified item (case-insensitively).<br>The value of the removed item is the return value.                                               |
| popitem()                 | Remove the last item that was inserted into the dictionary.<br>For Python version <3.7, popitem() removes a random item.                            |

## Example

CaseInsensitiveDict:

```py
>>> from typing import Union

>>> from case_insensitive_dict import CaseInsensitiveDict

>>> case_insensitive_dict = CaseInsensitiveDict[Union[str, int], str](data={"Aa": "b", 1: "c"})
>>> case_insensitive_dict["aa"]
'b'
>>> case_insensitive_dict[1]
'c'

```

which also supports json encoding/decoding:

```py
>>> import json

>>> from case_insensitive_dict import CaseInsensitiveDict, CaseInsensitiveDictJSONEncoder, case_insensitive_dict_json_decoder

>>> case_insensitive_dict = CaseInsensitiveDict[str, str](data={"Aa": "b"})
>>> json_string = json.dumps(obj=case_insensitive_dict, cls=CaseInsensitiveDictJSONEncoder)
>>> json_string
'{"Aa": "b"}'

>>> case_insensitive_dict = json.loads(s=json_string, object_hook=case_insensitive_dict_json_decoder)
>>> case_insensitive_dict
CaseInsensitiveDict({'Aa': 'b'})
```

## Contributing

Contributions are welcome via pull requests.

### First time setup

```sh
$ git clone git@github.com:DeveloperRSquared/case-insensitive-dict.git
$ cd case-insensitive-dict
$ poetry install
$ poetry shell
```

Tools including black, mypy etc. will run automatically if you install [pre-commit](https://pre-commit.com) using the instructions below

```sh
$ pre-commit install
$ pre-commit run --all-files
```

### Running tests

```sh
$ poetry run pytest
```

## Links

- Source Code: <https://github.com/DeveloperRSquared/case-insensitive-dict/>
- PyPI Releases: <https://pypi.org/project/case-insensitive-dictionary/>
- Issue Tracker: <https://github.com/DeveloperRSquared/case-insensitive-dict/issues/>
