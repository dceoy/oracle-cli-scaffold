#!/usr/bin/env python

import argparse
import fileinput
import logging
import os
from pprint import pformat

import cx_Oracle

__version__ = 'v0.0.1'


def main():
    args = _parse_arguments()
    _set_log_config(args=args)
    logger = logging.getLogger(__name__)
    logger.debug('args:' + os.linesep + pformat(vars(args)))
    sql = ''.join(_read_input(path=args.sql_path))
    logger.info(f'sql:{os.linesep}{sql}')
    connection = cx_Oracle.connect(
        user=args.db_user, password=args.db_password,
        dsn=args.db_dsn, encoding='UTF-8'
    )
    cursor = connection.cursor()
    cursor.execute(sql)


def _read_input(path='-'):
    for s in fileinput.input(files=path, encoding='utf-8'):
        yield s


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
        prog='oraclesql.py',
        description='Scaffold for cx_Oracle-based CLI tools'
    )
    parser.add_argument(
        '--version', action='version', version=f'%(prog)s {__version__}'
    )
    parser.add_argument(
        'sql_path', action='store', type=str, help='SQL file path'
    )
    parser.add_argument(
        '--db-user', dest='db_user', action='store',
        default=os.getenv('CX_ORACLE_DB_USER'),
        help='Set an Oracle DB user [$CX_ORACLE_DB_USER]'
    )
    parser.add_argument(
        '--db-password', dest='db_password', action='store',
        default=os.getenv('CX_ORACLE_DB_PASSWORD'),
        help='Set an Oracle DB password [$CX_ORACLE_DB_PASSWORD]'
    )
    parser.add_argument(
        '--db-dsn', dest='db_dsn', action='store',
        default=os.getenv('CX_ORACLE_DB_DSN'),
        help='Set an Oracle DB data source name [$CX_ORACLE_DB_DSN]'
    )
    logging_level_parser = parser.add_mutually_exclusive_group()
    logging_level_parser.add_argument(
        '--debug', action='store_true', help='Set logging level to DEBUG'
    )
    logging_level_parser.add_argument(
        '--info', action='store_true', help='Set logging level to INFO'
    )
    return parser.parse_args()


if __name__ == '__main__':
    main()
