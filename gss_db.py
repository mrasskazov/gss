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

parser = argparse.ArgumentParser(description='Utility for working with Google'
                                 'Spreadsheet as a database')
# credentials
creds = parser.add_argument('-u', '--username',
                            help='Google username',
                            default=GOOGLE_LOGIN)
creds = parser.add_argument('-p', '--password',
                            help='Google password',
                            default=GOOGLE_PASSWORD)
creds = parser.add_argument('-s', '--spreadsheet-id',
                            help='Google spreadsheet ID',
                            default=GOOGLE_SPREADSHEET)
creds = parser.add_argument('-w', '--worksheet-name',
                            help='Google worksheet name',
                            default=GOOGLE_WORKSHEET)

# db command
subparsers = parser.add_subparsers(help='DB command')
# insert
db_insert = subparsers.add_parser('insert', help='insert row')
# need to add multiple supparsers with -c key=value
db_insert.add_argument('-c', '--column-name', help='column name for insert')
#db_update = subparsers.add_parser('update', help='update row')
#db_delete = subparsers.add_parser('delete', help='delete row')

#(options, args) = parser.parse_args()
import pprint
pprint.pprint(parser.parse_args())


def main():
    SSService = spreadsheet_service.SpreadsheetsService()
    SSService.email = GOOGLE_LOGIN
    SSService.password = GOOGLE_PASSWORD
    #SSService.source = 'We are writing data'
    SSService.ProgrammaticLogin()
    #import pudb; pudb.set_trace()
    #ws = SSService.GetWorksheetsFeed(key=GOOGLE_SPREADSHEET)
    #ls = SSService.GetListFeed(key=GOOGLE_SPREADSHEET)
    #import pudb; pudb.set_trace()
    SSService.InsertRow({'datetime': str(datetime.datetime.utcnow()),
                         'project': 'openstack/nova',
                         'commiter': getpass.getuser(),
                         'change-request': 'https://gerrit.mirantis.com/13885',
                         'how-it-works': 'it works fine',
                         },
                        GOOGLE_SPREADSHEET,
                        GOOGLE_WORKSHEET)
    return 0


if __name__ == '__main__':
    main()
