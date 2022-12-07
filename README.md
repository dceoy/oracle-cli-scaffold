pdoracle
========

Pandas-based SQL Executor for Oracle DB

[![Test](https://github.com/dceoy/pdoracle/actions/workflows/test.yml/badge.svg)](https://github.com/dceoy/pdoracle/actions/workflows/test.yml)

Installation
------------

```sh
$ pip install -U https://github.com/dceoy/pdoracle/archive/main.tar.gz
```

Usage
-----

List user tables.

```sh
$ pdoracle --user-tables
```

Execute a SQL command.

```sh
$ pdoracle --sql-command 'SELECT * FROM USER_TABLES ORDER BY TABLE_NAME'
```

Run `pdoracle --help` for more detail.
