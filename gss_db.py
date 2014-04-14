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
insert_parser = subparsers.add_parser('insert',
                                      help='insert row with specified columns')
# update
update_parser = subparsers.add_parser('update',
                                      help='update specified row')
update_to_subparser = update_parser.add_subparsers()
update_to_data = update_to_subparser.add_parser('to',
                                                help='new row data')
# delete
delete_parser = subparsers.add_parser('delete',
                                      help='delete specified row')
# column specification for all commands
for p in (insert_parser, update_parser, update_to_data, delete_parser):
    p.add_argument('-c', '--col',
                   action='append',
                   help='pair column-title="column value". '
                   'Can be specified multiple times')
#TODO: второй вариант - добавить subparser для каждой пары col=val, и
#   попробовать добавить такой subparser в insert_parser с action='append'

import pprint
#pprint.pprint(parser.parse_args())
#exit(1)

options = parser.parse_args()
#pprint.pprint(options.col)
row = dict()
for c in options.col:
    key, value = c.split('=', 1)
    row[key] = value
#pprint.pprint(row)


def main():
    SSService = spreadsheet_service.SpreadsheetsService()
    SSService.email = options.username
    SSService.password = options.password
    SSService.ProgrammaticLogin()

    insert(SSService, options.spreadsheet_id, options.worksheet_name)
    pass


def insert(SSService, spreadsheet_id, worksheet_name):
    SSService.InsertRow(row, spreadsheet_id, worksheet_name)


def update(SSService, spreadsheet_id, worksheet_name):
    pass


def delete(SSService, spreadsheet_id, worksheet_name):
    pass


if __name__ == '__main__':
    main()
