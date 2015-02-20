#!/usr/bin/env python
# -*- coding: utf-8 -*-
##############################################################################
#
#  Mongotail, Log all MongoDB queries in a "tail"able way.
#  Copyright (C) 2015 Mariano Ruiz (<http://mrdev.com.ar>).
#
#  Author: Mariano Ruiz <mrsarm@gmail.com>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

__author__ = 'Mariano Ruiz'
__version__ = '0.1.0'
__license__ = 'GPL-3'
__url__ = 'https://github.com/mrsarm/mongotail'
__doc__ = """Mongotail, Log all MongoDB queries in a "tail"able way."""
__usage__ = """%(prog)s [db address] [options]

db address can be:
  foo                   foo database on local machine (IPv4 connection)
  192.169.0.5/foo       foo database on 192.168.0.5 machine
  192.169.0.5:9999/foo  foo database on 192.168.0.5 machine on port 9999
  "[::1]:9999/foo"      foo database on ::1 machine on port 9999 (IPv6 connection)"""


import sys, re, argparse, getpass
from pymongo import MongoClient

from conn import get_host_port_db
from out import print_obj
from err import error_unknown, error_parsing


DEFAULT_LIMIT = 10
LOG_QUERY = {
        "ns": re.compile("^((?!\.system\.).)*$"),
        "command.profile": {"$exists": False},
        "command.collStats": {"$exists": False},
        "command.count": {"$ne": "system.profile"},
        "op": {"$ne":"getmore"},
}
LOG_FIELDS = ['ts', 'op', 'ns', 'query', 'updateobj', 'command', 'ninserted', 'ndeleted', 'nMatched']

def tail(args, address):
    try:
        host,  port, dbname = get_host_port_db(address)
        try:
            client = MongoClient(host=host, port=port)
        except Exception as e:
            sys.stderr.write("Error trying to connect: %s\n" % str(e))
            exit(-2)
        db = client[dbname]
        if args.username:
            if args.password != None:
                password = args.password
            else:
                password = getpass.getpass()
            try:
                db.authenticate(args.username, password, mechanism='MONGODB-CR')
            except Exception as e:
                sys.stderr.write("Error trying to authenticate: %s\n" % str(e))
                exit(-3)
        cursor = db.system.profile.find(LOG_QUERY, fields=LOG_FIELDS)
        if args.n.upper() != "ALL":
            try:
                skip = cursor.count() - int(args.n)
            except ValueError:
                error_parsing('Invalid lines number "%s"' % args.n)
            if skip > 0:
                cursor.skip(skip)
        if args.follow:
            cursor.add_option(2)  # Set the tailable flag
        while cursor.alive:
            try:
                result = next(cursor)
                print_obj(result)
            except StopIteration:
                pass
    except KeyboardInterrupt:
        pass


def main():
    parser = argparse.ArgumentParser(description=__doc__, usage=__usage__)
    egroup = parser.add_mutually_exclusive_group()
    parser.add_argument("-u", dest="username", default=None,
                        help="username for authentication")
    parser.add_argument("-p", "--password", dest="password", default=None,
                        help="password for authentication. If username is given and password isn't,\
                              it's asked from the tty.")
    parser.add_argument("-n", "--lines", dest="n", default=str(DEFAULT_LIMIT),
                        help="output the last N lines, instead of the last 10. Use ALL value to show all lines")
    parser.add_argument("-f", "--follow", dest="follow", action="store_true", default=False,
                        help="output appended data as the log grows")
    parser.add_argument('--version', action='version', version='%(prog)s ' + __version__ + "\n<" + __url__ + ">")
    args, address = parser.parse_known_args()
    if address and len(address) and address[0] == sys.argv[1]:
        address = address[0]
    elif len(address) == 0:
        error_parsing("db address expected")
    else:
        error_parsing()
    if address.startswith("-"):
        error_parsing()
    tail(args, address)

if __name__ == "__main__":
    main()
