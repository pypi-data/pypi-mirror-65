# Norma 43 Parser
[![Build status](https://github.com/sergief/norma43parser/workflows/Python%20package/badge.svg)](https://github.com/sergief/norma43parser/actions?query=workflow%3A%22Python+package%22)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)

Parser for Norma43 bank account documents, commonly used in spanish banks to retrieve account movements.
It supports Python 3.6 onwards.

## How to install

```sh
$ pip install norma43parser
```

## How to use it
```python
from norma43parser import Norma43Parser, DateFormat                                                                                                                                                                                            

parser = Norma43Parser(DateFormat.SPANISH)
# it reads dates in DMY format, for YMD use DateFormat.ENGLISH

contents = open('./file.n43','r').read()                                                                                                                                                                           

n43 = parser.parse(contents)
```

## Norma43Document Model

Class `Norma43Document`:
* `accounts`: `List` of `Account` objects.
* `reported_entries`: number of reported n43 file entries.

Class `Account`:
* `header`: a `Header` object.
* `movement_lines`: `List` ofr `MovementLine` objects
* `footer`: a `Footer` object.

Class `Header`:
* `bank_code`: string.
* `branch_code`: string.
* `account_number`: string.
* `start_date`: date.
* `end_date`: date.
* `initial_balance`: Decimal.
* `currency`: string in ISO-4217 (number).
* `information_mode_code`: string.
* `account_name`: string.

Class `MovementLine`:
* `branch_code`: string.
* `transaction_date`: date.
* `value_date`: date.
* `amount`: Decimal.
* `balance`: Decimal.
* `description`: string.
* `extra_information`: List of strings.

Class `Footer`:
* `bank_code`: string.
* `branch_code`: string.
* `account_number`: string.
* `debit_entries`: integer.
* `debit_amount`: Decimal.
* `credit_entries`: integer.
* `credit_amount`: Decimal.
* `final_balance`: Decimal.
* `currency`: string in ISO-4217 (number).
