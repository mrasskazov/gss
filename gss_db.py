#!/usr/bin/env python
#-*- coding: utf-8 -*-

import argparse
import os
import sys

import gdata.spreadsheet.service as spreadsheet_service

GOOGLE_LOGIN = os.environ.get('GOOGLE_LOGIN', 'oscirobot@mirantis.com')
GOOGLE_PASSWORD = os.environ.get('GOOGLE_PASSWORD', 'eo6uWoog')
GOOGLE_SPREADSHEET = os.environ.get(
    'GOOGLE_SPREADSHEET',
    '0Auqi3YThSgB5dGZyTWNSWmQzbXJfRmJpcjVSSGhUZWc')
GOOGLE_WORKSHEET = 'od6'


def insert(row, SSService, spreadsheet_id, worksheet_name):
    SSService.InsertRow(row, spreadsheet_id, worksheet_name)


def get_argparser():
    parser = argparse.ArgumentParser(prog='gss_db',
                                     description='Utility for working with '
                                     'Google Spreadsheet like with a database')
    # credentials
    parser.add_argument('-u', '--username',
                        help='Google username',
                        default=GOOGLE_LOGIN)
    parser.add_argument('-p', '--password',
                        help='Google password',
                        default=GOOGLE_PASSWORD)
    parser.add_argument('-s', '--spreadsheet-id',
                        help='Google spreadsheet ID',
                        default=GOOGLE_SPREADSHEET)
    parser.add_argument('-w', '--worksheet-name',
                        help='Google worksheet name',
                        default=GOOGLE_WORKSHEET)

    subparsers = parser.add_subparsers(help='command')
    # insert
    insert_parser = subparsers.add_parser(
        'insert',
        help='insert row with specified columns')
    insert_parser.add_argument(
        '-c', '--col',
        action='append',
        help='pair column-title="column value". Can be specified few times')
    return parser


def main():
    try:
        parser = get_argparser()
        options = parser.parse_args()
    except Exception, ex:
        sys.exit(str(ex))

    row = dict()
    for c in options.col:
        key, value = c.split('=', 1)
        row[key] = value

    SSService = spreadsheet_service.SpreadsheetsService()
    SSService.email = options.username
    SSService.password = options.password
    SSService.ProgrammaticLogin()

    insert(row, SSService, options.spreadsheet_id, options.worksheet_name)


if __name__ == '__main__':
    main()
