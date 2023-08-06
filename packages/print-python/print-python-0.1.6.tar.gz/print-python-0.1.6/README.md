# 🖨️ print-python

Python client for [`print`](https://github.com/gduverger/print) (simplest logging API)

## Introduction

Learn more about `print` at [github.com/gduverger/print](https://github.com/gduverger/print).

## Installation

```bash
$ pipenv install print-python
```

## Dependencies

```
requests (2.23.0)
```

## Usage

```python
>>> from print import print
>>> print(url='<PRINT_URL>', token='<PRINT_TOKEN>')
>>> print('As easy as rolling off a log')
```

## Test

```bash
python -m pytest
```
