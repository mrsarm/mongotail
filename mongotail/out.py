# -*- coding: utf-8 -*-
##############################################################################
#
#  Mongotail, Log all MongoDB queries in a "tail"able way.
#  Copyright (C) 2015-2020 Mariano Ruiz <https://github.com/mrsarm/mongotail>
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
import collections
import sys
from .jsondec import JSONEncoder
from .err import warn


json_encoder = JSONEncoder()


def print_obj(obj, verbose, metadata, mongo_version):
    """
    Print the dict returned by a MongoDB Query in the standard output.
    """
    if verbose:
        sys.stdout.write(json_encoder.encode(obj) + '\n')
        sys.stdout.flush()
    else:
        try:
            ts_time = obj['ts']
            operation = obj['op']
            doc = None
            if operation == 'query':
                if mongo_version < "3.2":
                    doc = obj['ns'].split(".")[-1]
                    query = json_encoder.encode(obj['query']) if 'query' in obj else "{}"
                else:
                    if "query" in obj:
                        cmd = obj['query']      # Mongo 3.2 - 3.4
                    else:
                        cmd = obj['command']    # Mongo 3.6+
                    doc = cmd['find']
                    query = json_encoder.encode(cmd['filter']) if 'filter' in cmd else "{}"
                    if 'sort' in cmd:
                        query += ', sort: ' + json_encoder.encode(cmd['sort'])
                    if 'limit' in cmd:
                        query += ', limit: ' + json_encoder.encode_number(cmd['limit'])
                    if 'skip' in cmd:
                        query += ', skip: ' + json_encoder.encode_number(cmd['skip'])
                if 'nreturned' in obj:
                    # If a query fails Mongo doesn't record nreturned
                    query += '. %s returned.' % obj['nreturned']
            elif operation == 'update':
                doc = obj['ns'].split(".")[-1]
                if mongo_version < "3.6":
                    query = json_encoder.encode(obj['query']) if 'query' in obj else "{}"
                    query += ', ' + json_encoder.encode(obj['updateobj'])
                else:
                    query = json_encoder.encode(obj['command']['q']) if 'command' in obj and 'q' in obj['command'] else "{}"
                    query += ', ' + json_encoder.encode(obj['command']['u'])
                if 'nModified' in obj:
                    query += '. %s updated.' % obj['nModified']
                elif 'nMatched' in obj:
                    query += '. %s updated.' % obj['nMatched']
            elif operation == 'insert':
                if mongo_version < "3.2":
                    doc = obj['ns'].split(".")[-1]
                    query = json_encoder.encode(obj['query']) if 'query' in obj else "{}"
                else:
                    if 'query' in obj:
                        doc = obj['query']['insert']
                        if 'documents' in obj['query']:
                            if isinstance(obj['query']['documents'], collections.Iterable) \
                                    and len(obj['query']['documents']) > 1:
                                query = json_encoder.encode(obj['query']['documents']) + ". "
                            else:
                                query = json_encoder.encode(obj['query']['documents'][0]) + ". "
                        else:
                            query = ""
                    else:
                        # Mongo 3.6+ profiler looks like doens't record insert details (document object), and
                        # some tools like Robo 3T (formerly Robomongo) allows to duplicate collections
                        # but the profiler doesn't record the element inserted
                        doc = obj['ns'].split(".")[-1]
                        query = ""
                query += '%s inserted.' % obj['ninserted']
            elif operation == 'remove':
                doc = obj['ns'].split(".")[-1]
                if mongo_version < "3.6":
                    query = json_encoder.encode(obj['query']) if 'query' in obj else "{}"
                else:
                    query = json_encoder.encode(obj['command']['q']) if 'command' in obj and 'q' in obj['command'] else "{}"
                query += '. %s deleted.' % obj['ndeleted']
            elif operation == "command":
                if 'count' in obj["command"]:
                    operation = "count"
                    query = json_encoder.encode(obj['command']['query'])
                elif 'aggregate' in obj["command"]:
                    operation = "aggregate"
                    query = json_encoder.encode(obj['command']['pipeline'])
                elif 'distinct' in obj["command"]:
                    operation = "distinct"
                    query = json_encoder.encode(obj['command']['query'])
                    query = '"%s", %s' % (obj['command']['key'], query)
                elif 'drop' in obj["command"]:
                    operation = "drop"
                    query = ""
                elif 'findandmodify' in obj["command"]:
                    operation = "findandmodify"
                    query = "query: " + json_encoder.encode(obj['command']['query'])
                    if 'sort' in obj["command"]:
                        query += ", sort: " + json_encoder.encode(obj['command']['sort'])
                    if 'update' in obj["command"]:
                        query += ", update: " + json_encoder.encode(obj['command']['update'])
                    if 'remove' in obj["command"]:
                        query += ", remove: " + str(obj['command']['remove']).lower()
                    if 'fields' in obj["command"]:
                        query += ", fields: " + json_encoder.encode(obj['command']['fields'])
                    if 'upsert' in obj["command"]:
                        query += ", upsert: " + str(obj['command']['upsert']).lower()
                    if 'new' in obj["command"]:
                        query += ", new: " + str(obj['command']['new']).lower()
                elif 'group' in obj["command"]:
                    operation = "group"
                    doc = obj["command"]['group']["ns"]
                    if 'key' in obj['command']['group']:
                        key = "key: " + json_encoder.encode(obj['command']['group']['key'])
                    else:
                        key = None
                    if 'initial' in obj['command']['group']:
                        initial = "initial: " + json_encoder.encode(obj['command']['group']['initial'])
                    else:
                        initial = None
                    if 'cond' in obj['command']['group']:
                        cond = "cond: " + json_encoder.encode(obj['command']['group']['cond'])
                    else:
                        cond = None
                    if '$keyf' in obj['command']['group']:
                        key_function = "keyf: " + min_script(obj['command']['group']['$keyf'])
                    else:
                        key_function = None
                    if '$reduce' in obj['command']['group']:
                        reduce_func = "reduce: " + min_script(obj['command']['group']['$reduce'])
                    else:
                        reduce_func = None
                    if 'finalize' in obj['command']['group']:
                        finalize_func = "finalize: " + min_script(obj['command']['group']['finalize'])
                    else:
                        finalize_func = None
                    query = ", ".join(list(filter(lambda x: x, (key, reduce_func, initial, key_function, cond, finalize_func))))
                elif 'map' in obj["command"]:
                    operation = "map"
                    doc = obj["command"]["mapreduce"]
                    del obj["command"]["mapreduce"]
                    map_func = min_script(obj['command']["map"])
                    del obj['command']["map"]
                    reduce_func = min_script(obj['command']["reduce"])
                    del obj['command']["reduce"]
                    query = "{%s, %s, %s}" % (map_func, reduce_func, json_encoder.encode(obj['command']))
                else:
                    warn('Unknown command operation\nDump: %s' % json_encoder.encode(obj))
                if not doc:
                    doc = obj["command"][operation]
            else:
                warn('Unknown operation "%s"\nDump: %s' % (operation, json_encoder.encode(obj)))

            if metadata:
                met = []
                for m in metadata:
                    if m in obj and obj[m] != {}:
                        q = m + ": "
                        if isinstance(obj[m], str):
                            q += '"%s"' % obj[m]
                        elif isinstance(obj[m], dict):
                            q += json_encoder.encode(obj[m])
                        else:
                            q += str(obj[m])
                        met.append(q)
                if met:
                    if not query.endswith("."): query += ". "
                    if not query.endswith(" "): query += " "
                    query += ", ".join(met)

            sys.stdout.write("%s %s [%s] : %s\n" % (ts_time.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
                                                    operation.upper().ljust(9), doc, query))
            sys.stdout.flush()  # Allows pipe the output during the execution with others tools like 'grep'
        except (KeyError, TypeError):
            warn('Unknown registry\nDump: %s' % json_encoder.encode(obj))


def min_script(js):
    """
    Minify script in a very insecure way.
    """
    if js:
        return js.replace("\n", " ")
            #.replace("                        ", " ") \
            #.replace("                    ", " ") \
            #.replace("                ", " ") \
            #.replace("            ", " ") \
            #.replace("        ", " ") \
            #.replace("    ", " ").replace("\t", " ")
    return ""
