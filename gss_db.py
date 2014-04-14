#!/usr/bin/env python
#-*- coding: utf-8 -*-

import argparse
import ConfigParser
import getpass
import os
import sys

import gdata.spreadsheet.service as spreadsheet_service

GOOGLE_SPREADSHEET = os.environ.get(
    'GOOGLE_SPREADSHEET',
    '0Auqi3YThSgB5dGZyTWNSWmQzbXJfRmJpcjVSSGhUZWc')
GOOGLE_WORKSHEET = 'od6'

CONFIG = dict()


def config(key, unset=False):

    conf_dir_name = '~/.config/gss_db'
    conf_file_name = conf_dir_name + '/gss_db.conf'

    config_file = os.path.expanduser(conf_file_name)
    parser = ConfigParser.ConfigParser()

    if os.path.isfile(config_file):
        parser.read(config_file)
    else:
        print 'no config file found, generating it'
        if not os.path.isdir(os.path.expanduser(conf_dir_name)):
            os.makedirs(os.path.expanduser(conf_dir_name))

    parser.has_section('general') or parser.add_section('general')

    if unset:
        del CONFIG[key]
        parser.remove_option('general', key)

    if key in CONFIG:
        return CONFIG.get(key)
    elif parser.has_option('general', key):
        CONFIG[key] = parser.get('general', key)
        return parser.get('general', key)
    elif key == 'username':
        user = raw_input('enter username:')
        CONFIG['username'] = user
        parser.set('general', 'username', user)
    elif key == 'password':
        password = getpass.getpass('enter password:')
        CONFIG['password'] = password
        parser.set('general', 'password', password)

    with open(config_file, 'wb') as conf_file:
        parser.write(conf_file)
    return CONFIG[key]


def insert(row, SSService, spreadsheet_id, worksheet_name):

    SSService.InsertRow(row, spreadsheet_id, worksheet_name)


def get_argparser():

    parser = argparse.ArgumentParser(prog='gss_db',
                                     description='Utility for working with '
                                     'Google Spreadsheet like with a database')
    # credentials
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
    SSService.email = config('username')
    SSService.password = config('password')
    SSService.ProgrammaticLogin()

    insert(row, SSService, options.spreadsheet_id, options.worksheet_name)


if __name__ == '__main__':
    main()
