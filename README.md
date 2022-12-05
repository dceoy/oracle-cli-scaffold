oracle-cli-scaffold
===================

Scaffold for cx_Oracle-based CLI tools

[![Test](https://github.com/dceoy/oracle-cli-scaffold/actions/workflows/test.yml/badge.svg)](https://github.com/dceoy/oracle-cli-scaffold/actions/workflows/test.yml)

Example
-------

##### Installation

```sh
$ pip install -r requirements.txt
```

##### Usage

Execute SQL.

```sh
$ echo 'SELECT * FROM USER_TABLES ORDER BY TABLE_NAME' \
    | ./oraclesql.py -
```

Run `./oraclesql.py --help`.
