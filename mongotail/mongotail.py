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

import sys, re, time
from pymongo import MongoClient
from bson import json_util

DEFAULT_LIMIT = 10
LOG_QUERY = {
        "ns": re.compile("^((?!\.system\.).)*$"),
        "command.profile": {"$exists": False},
        "command.collStats": {"$exists": False},
        "command.count": {"$ne": "system.profile"},
        "op": {"$ne":"getmore"},
}
LOG_FIELDS = ['ts', 'op', 'ns', 'query', 'updateobj', 'command', 'ninserted', 'ndeleted', 'nMatched']

def main():
    client = MongoClient()
    db = client[sys.argv[1]]
    try:
        cursor = db.system.profile.find(LOG_QUERY, fields=LOG_FIELDS)
        skip = cursor.count() - DEFAULT_LIMIT
        if skip > 0:
            cursor.skip(skip)
        if len(sys.argv) == 3 and sys.argv[2] == "-f":
            cursor.add_option(2)  # Set the tailable flag
        while cursor.alive:
            try:
                result = next(cursor)
                print_obj(result)
            except StopIteration:
                pass
    except KeyboardInterrupt:
        pass

def print_obj(obj):
    time = obj['ts']
    operation = obj['op']
    doc = obj['ns'].split(".")[1]
    if operation in ('query', 'insert', 'remove', 'update'):
        if 'query' in obj:
            query = json_util.dumps(obj['query'])
        else:
            query = ""
        if operation == 'update':
            if 'updateobj' in obj:
                query += ' -> ' + json_util.dumps(obj['updateobj'])
                query += '. %s updated.' % obj['nMatched']
        elif operation == 'insert':
            if query != "":
                query += ". "
            query += '%s inserted.' % obj['ninserted']
        elif operation == 'remove':
            query += '. %s deleted.' % obj['ndeleted']
    elif operation == "command":
        query = json_util.dumps(obj['command']['query'])
        if 'count' in obj["command"]:
            doc = obj["command"]["count"]
            operation = "count"
        else:
            raise RuntimeError('Unknow command "%s"\nDump: %s' % (operation, json_util.dumps(obj)))
    else:
        raise RuntimeError('Unknow command "%s"\nDump: %s' % (operation, json_util.dumps(obj)))
    #print json_util.dumps(obj)
    sys.stdout.write("%s %s [%s] : %s\n" % (time.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3], operation.upper().ljust(6), doc, query))
    sys.stdout.flush()  # Allows pipe the output during the execution with others tools like 'grep'

if __name__ == "__main__":
    main()
