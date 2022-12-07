#!/usr/bin/env python

import argparse
import fileinput
import logging
import os
import sys
from pprint import pformat

import cx_Oracle
import pandas as pd

__version__ = 'v0.0.1'


def main():
    args = _parse_arguments()
    _set_log_config(args=args)
    logger = logging.getLogger(__name__)
    logger.debug('args:' + os.linesep + pformat(vars(args)))
    connection = cx_Oracle.connect(
        user=args.db_user, password=args.db_password,
        dsn=args.db_dsn, encoding='UTF-8'
    )
    logger.debug(f'connection: {connection}')
    if args.user_tables:
        sqls = ['SELECT * FROM USER_TABLES ORDER BY TABLE_NAME']
    elif args.user_views:
        sqls = ['SELECT * FROM USER_VIEWS ORDER BY VIEW_NAME']
    elif args.sql_command:
        sqls = [args.sql_command]
    else:
        sqls = list(_read_sql_input(path=args.sql_path))
    for i, sql in enumerate(sqls):
        logger.info(f'sql: {sql}')
        df = pd.read_sql_query(sql, connection)
        if i > 0:
            print('---')
        if args.csv:
            print(df.to_csv(sys.stdout, sep=',', index=False))
        elif args.tsv:
            print(df.to_csv(sys.stdout, sep='\t', index=False))
        else:
            print(df)


def _read_sql_input(path='-'):
    sql_lines = list()
    for s in fileinput.input(files=path, encoding='utf-8'):
        r = s.strip()
        if r.endswith(';'):
            sql_lines.append(r[:-1])
            sql = ''.join(sql_lines)
            sql_lines = list()
            yield sql
        else:
            sql_lines.append(r)
    if sql_lines:
        yield ''.join(sql_lines)


def _set_log_config(args):
    if args.debug:
        level = logging.DEBUG
    elif args.info:
        level = logging.INFO
    else:
        level = logging.WARNING
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S', level=level
    )


def _parse_arguments():
    parser = argparse.ArgumentParser(
        prog='pdoracle', description='Pandas-based SQL Executor for Oracle DB'
    )
    parser.add_argument(
        '--version', action='version', version=f'%(prog)s {__version__}'
    )
    parser.add_argument(
        '--db-user', action='store',
        default=os.getenv('ORACLE_DB_USER'),
        help='Set an Oracle DB user [$ORACLE_DB_USER]'
    )
    parser.add_argument(
        '--db-password', action='store',
        default=os.getenv('ORACLE_DB_PASSWORD'),
        help='Set an Oracle DB password [$ORACLE_DB_PASSWORD]'
    )
    parser.add_argument(
        '--db-dsn', action='store',
        default=os.getenv('ORACLE_DB_DSN'),
        help='Set an Oracle DB data source name [$ORACLE_DB_DSN]'
    )
    logging_level_parser = parser.add_mutually_exclusive_group()
    logging_level_parser.add_argument(
        '--debug', action='store_true', help='Set logging level to DEBUG'
    )
    logging_level_parser.add_argument(
        '--info', action='store_true', help='Set logging level to INFO'
    )
    command_parser = parser.add_mutually_exclusive_group()
    command_parser.add_argument(
        '--sql-command', action='store', type=str, help='execute SQL command'
    )
    command_parser.add_argument(
        '--sql-path', action='store', type=str, help='execute SQL file'
    )
    command_parser.add_argument(
        '--user-tables', action='store_true', help='list user tables'
    )
    command_parser.add_argument(
        '--user-views', action='store_true', help='list user views'
    )
    format_parser = parser.add_mutually_exclusive_group()
    format_parser.add_argument(
        '--csv', action='store', type=str, help='print CSV data'
    )
    format_parser.add_argument(
        '--tsv', action='store_true', help='print TSV data'
    )
    return parser.parse_args()


if __name__ == '__main__':
    main()
