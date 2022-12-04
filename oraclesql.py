#!/usr/bin/env python

import argparse
import fileinput
import logging

__version__ = 'v0.0.1'


def main():
    args = _parse_arguments()
    _set_log_config(args=args)
    logger = logging.getLogger(__name__)
    logger.info('Run oracle-cli-scaffold.')
    for s in _read_input_sql(sql_path=args.sql_path):
        print(s)


def _read_input_sql(sql_path='-'):
    for s in fileinput.input(files=sql_path, encoding='utf-8'):
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
