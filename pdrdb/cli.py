#!/usr/bin/env python

import argparse
import fileinput
import logging
import os
import sys
from pprint import pformat

import pandas as pd
from sqlalchemy import create_engine

from . import __version__


def main():
    args = _parse_arguments()
    _set_log_config(args=args)
    logger = logging.getLogger(__name__)
    logger.debug('args:' + os.linesep + pformat(vars(args)))
    if args.rdbms == 'sqlite':
        url = f'sqlite:///{args.db_dsn}'
    else:
        url = f'{args.rdbms}://{args.db_user}:{args.db_password}@{args.db_dsn}'
    if args.user_tables:
        if args.rdbms == 'sqlite':
            sqls = [
                'SELECT * FROM sqlite_master'
                ' WHERE type = \'table\' ORDER BY name'
            ]
        elif args.rdbms == 'postgresql':
            sqls = [
                'SELECT * FROM information_schema.tables ORDER BY table_name'
            ]
        elif args.rdbms == 'mysql':
            sqls = [
                'SELECT * FROM information_schema.TABLES'
                ' WHERE TABLE_TYPE = \'BASE_TABLE\' ORDER BY TABLE_NAME'
            ]
        elif args.rdbms == 'oracle':
            sqls = ['SELECT * FROM USER_TABLES ORDER BY TABLE_NAME']
        else:
            raise NotImplementedError(f'unimplemented RDBMS: {args.rdbms}')
    elif args.user_views:
        if args.rdbms == 'sqlite':
            sqls = [
                'SELECT name FROM sqlite_master'
                ' WHERE type = \'table\' ORDER BY name'
            ]
        elif args.rdbms == 'postgresql':
            sqls = [
                'SELECT * FROM information_schema.views ORDER BY table_name'
            ]
        elif args.rdbms == 'mysql':
            sqls = [
                'SELECT * FROM information_schema.TABLES'
                ' WHERE TABLE_TYPE = \'VIEW\' ORDER BY TABLE_NAME'
            ]
        elif args.rdbms == 'oracle':
            sqls = ['SELECT * FROM USER_VIEWS ORDER BY VIEW_NAME']
        else:
            raise NotImplementedError(f'unimplemented RDBMS: {args.rdbms}')
    elif args.sql_command:
        sqls = [args.sql_command]
    else:
        sqls = list(_read_sql_input(path=args.sql_path))
    engine = create_engine(url)
    logger.debug(f'engine: {engine}')
    for i, sql in enumerate(sqls):
        logger.info(f'sql: {sql}')
        df = pd.read_sql_query(sql, engine)
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
            sql = ' '.join(sql_lines)
            sql_lines = list()
            yield sql
        else:
            sql_lines.append(r)
    if sql_lines:
        yield ' '.join(sql_lines)


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
        prog='pdrdb', description='Pandas-based SQL Executor for RDBMS'
    )
    parser.add_argument(
        '--version', action='version', version=f'%(prog)s {__version__}'
    )
    parser.add_argument(
        '--rdbms', action='store',
        default=(os.getenv('PDRDB_RDBMS') or 'postgresql'),
        choices={'postgresql', 'sqlite', 'mysql', 'oracle'},
        help='choose a RDBMS'
    )
    parser.add_argument(
        '--db-user', action='store', type=str,
        default=os.getenv('PDRDB_DB_USER'),
        help='set a DB user [$PDRDB_DB_USER]'
    )
    parser.add_argument(
        '--db-password', action='store', type=str,
        default=os.getenv('PDRDB_DB_PASSWORD'),
        help='set a DB password [$PDRDB_DB_PASSWORD]'
    )
    parser.add_argument(
        '--db-dsn', action='store', type=str,
        default=os.getenv('PDRDB_DB_DSN'),
        help='set a DB data source name or a SQLite file path [$PDRDB_DB_DSN]'
    )
    logging_level_parser = parser.add_mutually_exclusive_group()
    logging_level_parser.add_argument(
        '--debug', action='store_true', help='set logging level to DEBUG'
    )
    logging_level_parser.add_argument(
        '--info', action='store_true', help='set logging level to INFO'
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
        '--csv', action='store_true', help='print CSV data'
    )
    format_parser.add_argument(
        '--tsv', action='store_true', help='print TSV data'
    )
    return parser.parse_args()


if __name__ == '__main__':
    main()
