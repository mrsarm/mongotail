#!/usr/bin/env python
# -*- coding: utf-8 -*-
##############################################################################
#
#  Mongotail, Log all MongoDB queries in a "tail"able way.
#  Copyright (C) 2015 Mariano Ruiz (<https://github.com/mrsarm/mongotail>).
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


from __future__ import absolute_import
import sys, re, argparse
from .conn import connect
from .out import print_obj
from .err import error, error_parsing, EINTR, EDESTADDRREQ
from pymongo import get_version_string
from pymongo.read_preferences import ReadPreference
from pymongo.errors import ConnectionFailure

from . import __version__, __license__, __doc__, __url__, __usage__

DEFAULT_LIMIT = 10
LOG_QUERY = {
        "ns": re.compile(r"^((?!(admin\.\$cmd|\.system)).)*$"),
        "command.profile": {"$exists": False},
        "command.collStats": {"$exists": False},
        "command.collstats": {"$exists": False},
        "command.createIndexes": {"$exists": False},
        "command.dbstats": {"$exists": False},
        "command.count": {"$ne": "system.profile"},
        "op": re.compile(r"^((?!(getmore|killcursors)).)"),
}
LOG_FIELDS = ['ts', 'op', 'ns', 'query', 'updateobj', 'command', 'ninserted', 'ndeleted', 'nMatched']

def tail(client, db, lines, follow):
    if get_version_string() >= "3.0":
        # From PyMongo 3.0 fields are passed to `find` function with the parameter `projection`
        cursor = db.system.profile.find(LOG_QUERY, projection=LOG_FIELDS)
    else:
        # From PyMongo <= 2.8 fields are passed to `find` function with the parameter `fields`
        cursor = db.system.profile.find(LOG_QUERY, fields=LOG_FIELDS)
    if lines.upper() != "ALL":
        try:
            skip = cursor.count() - int(lines)
        except ValueError:
            error_parsing('Invalid lines number "%s"' % lines)
        if skip > 0:
            cursor.skip(skip)
    if follow:
        cursor.add_option(2)  # Set the tailable flag
    while cursor.alive:
        try:
            result = next(cursor)
            print_obj(result)
        except StopIteration:
            pass


def show_profiling_level(client, db):
    try:
        level = db.profiling_level()
        sys.stdout.write("Profiling level currently in level %s\n" % level)
    except Exception as e:
        error('Error trying to get profiling level. %s' % e, EINTR)


def set_profiling_level(client, db, level):
    try:
        db.set_profiling_level(int(level))
        sys.stdout.write("Profiling level set to level %s\n" % level)
    except Exception as e:
        err = str(e).replace("OFF", "0").replace("SLOW_ONLY", "1").replace("ALL", "2")
        error('Error configuring profiling level to "%s". %s' % (level, err), EINTR)


def set_slowms_level(client, db, slowms):
    profiling_level = db.profiling_level()
    try:
        db.set_profiling_level(profiling_level, int(slowms))
        sys.stdout.write("Threshold profiling set to %s milliseconds\n" % slowms)
    except Exception as e:
        error('Error configuring threshold profiling in "%s" milliseconds. %s' % (slowms, str(e)), EINTR)


def show_slowms_level(client, db):
    try:
        level = db.command("profile", -1, read_preference=ReadPreference.PRIMARY)
        sys.stdout.write("Threshold profiling currently in %s milliseconds\n" % level['slowms'])
    except Exception as e:
        error('Error trying to get threshold profiling level. %s' % e, EINTR)


def main():
    try:
        # Parsing command line options
        parser = argparse.ArgumentParser(description=__doc__, usage=__usage__)
        egroup = parser.add_mutually_exclusive_group()
        parser.add_argument("-u", "--username", dest="username", default=None,
                            help="username for authentication")
        parser.add_argument("-p", "--password", dest="password", default=None,
                            help="password for authentication. If username is given and password isn't,\
                                  it's asked from tty.")
        parser.add_argument("-b", "--authenticationDatabase", dest="auth_database", default=None,
                            help="database to use to authenticate the user. If not specified, the user "
                                 "will be authenticated against the database specified in the [db address].")
        parser.add_argument("-n", "--lines", dest="n", default=str(DEFAULT_LIMIT),
                            help="output the last N lines, instead of the last 10. Use ALL value to show all lines")
        parser.add_argument("-f", "--follow", dest="follow", action="store_true", default=False,
                            help="output appended data as the log grows")
        parser.add_argument("-l", "--level", dest="level", default=None,
                            help="Specifies the profiling level, which is either 0 for no profiling, "
                                 "1 for only slow operations, or 2 for all operations. Or use with 'status' word "
                                 "to show the current level configured. "
                                 "Uses this option once before logging the database")
        parser.add_argument("-s", "--slowms", dest="ms", default=None,
                            help="Sets the threshold in milliseconds for the profile to consider a query "
                                 "or operation to be slow (use with `--level 1`). Or use with 'status' word "
                                 "to show the current milliseconds configured. ")
        parser.add_argument('--version', action='version', version='%(prog)s ' + __version__ + "\n<" + __url__ + ">")
        args, address = parser.parse_known_args()
        if address and len(address) and address[0] == sys.argv[1]:
            address = address[0]
        elif len(address) == 0:
            error("db address expected", EDESTADDRREQ)
        else:
            error_parsing()
        if address.startswith("-"):
            error_parsing()

        # Getting connection
        client, db = connect(address, args.username, args.password, args.auth_database)

        # Execute command
        if args.level:
            if args.level.lower() == "status":
                show_profiling_level(client, db)
            else:
                set_profiling_level(client, db, args.level)
        elif args.ms:
            if args.ms.lower() == "status":
                show_slowms_level(client, db)
            else:
                set_slowms_level(client, db, args.ms)
        else:
            tail(client, db, args.n, args.follow)
    except KeyboardInterrupt:
        sys.stdout.write("\n")
    except ConnectionFailure as e:
        error("Error trying to authenticate: %s" % str(e), -3)

if __name__ == "__main__":
    main()
