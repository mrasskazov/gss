#!/usr/bin/env python
#-*- coding: utf-8 -*-

#from optparse import OptionParser
import argparse
import datetime
import getpass
import os

import gdata.spreadsheet.service as spreadsheet_service

#TODO:
# 1. storing of credentials in config file (~/.config/gdrive/creds)
# 2. CLI parameters
#       creds:
#           -u --username
#           -p --password
#       speadsheet:
#           -s --spreadsheet-id
#           -w --worksheet-name
#       commands:
#           insert row_name=row_value row_name=row_value ...
#           update row_name=row_value row_name=row_value ... to
#                   row_name=row_value row_name=row_value ...
#           delete row_name=row_value row_name=row_value ...
# gss_db.py -s -w insert name="Known User" salary=35000
# gss_db.py -s -w update name="Known User" to salary=42000


GOOGLE_LOGIN = os.environ.get('GOOGLE_LOGIN', 'oscirobot@mirantis.com')
GOOGLE_PASSWORD = os.environ.get('GOOGLE_PASSWORD', 'eo6uWoog')
GOOGLE_SPREADSHEET = os.environ.get(
    'GOOGLE_SPREADSHEET',
    '0Auqi3YThSgB5dGZyTWNSWmQzbXJfRmJpcjVSSGhUZWc')
GOOGLE_WORKSHEET = 'od6'

parser = argparse.ArgumentParser(description='Utility for working with Google '
                                 'Spreadsheet like with a database')
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

# db command
subparsers = parser.add_subparsers(help='DB command')
# insert
db_insert = subparsers.add_parser('insert',
                                  help='insert row with specified columns')
db_insert.add_argument('-c', '--col',
                       action='append',
                       help='pair column-title="column value". '
                       'Can be specified multiple times')
#TODO: второй вариант - добавить subparser для каждой пары col=val, и
#   попробовать добавить такой subparser в db_insert с action='append'
# добавить -c для каждой команды в цикле for. для update после цикла
#   добавить еще subparser 'to'
# need to add multiple supparsers with -c key=value
#db_row = db_insert.add_subparsers(help='row data')
#db_columns = db_insert.add_argument('-c', '--col', action='append')
#db_insert.add_argument('-c', '--col-name', help='col name for insert')
#db_update = subparsers.add_parser('update', help='update row')
#db_delete = subparsers.add_parser('delete', help='delete row')

#(options, args) = parser.parse_args()

import pprint
#pprint.pprint(parser.parse_args())
#exit(1)

options = parser.parse_args()
#pprint.pprint(options.col)
row = dict()
for c in options.col:
    key, value = c.split('=')[0:2]
    row[key] = value
pprint.pprint(row)


def main():
    SSService = spreadsheet_service.SpreadsheetsService()
    SSService.email = options.username
    SSService.password = options.password
    SSService.ProgrammaticLogin()
    #ws = SSService.GetWorksheetsFeed(key=GOOGLE_SPREADSHEET)
    #ls = SSService.GetListFeed(key=GOOGLE_SPREADSHEET)
    SSService.InsertRow(row, GOOGLE_SPREADSHEET, GOOGLE_WORKSHEET)
    return 0


if __name__ == '__main__':
    main()
