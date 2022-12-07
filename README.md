pdrdb
=====

Pandas-based SQL Executor for RDBMS

[![Test](https://github.com/dceoy/pdrdb/actions/workflows/test.yml/badge.svg)](https://github.com/dceoy/pdrdb/actions/workflows/test.yml)
[![CI to Docker Hub](https://github.com/dceoy/pdrdb/actions/workflows/docker-publish.yml/badge.svg)](https://github.com/dceoy/pdrdb/actions/workflows/docker-publish.yml)

Installation
------------

```sh
$ pip install -U https://github.com/dceoy/pdrdb/archive/main.tar.gz
```

Set the following environment variables for connection to the RDBMS:

- `PDRDB_RDBMS`: RDBMS (`postgresql`, `sqlite`, `mysql`, and `oracle` are available.)
- `PDRDB_DB_USER`: DB user
- `PDRDB_DB_PASSWORD`: DB password
- `PDRDB_DB_DSN`: DB data source name

Usage
-----

Execute a SQL command.

```sh
$ pdrdb --sql-command 'SELECT * FROM USER_TABLES'
```

Run `pdrdb --help` for more detail.
