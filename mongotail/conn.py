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
import getpass
from .err import error, error_parsing, ECONNREFUSED, EFAULT
from pymongo import MongoClient

def get_host_port_db(address):
    """
    :param address: the address, possible values are:
        foo                   foo database on local machine (IPv4 connection)
        192.169.0.5/foo       foo database on 192.168.0.5 machine
        192.169.0.5:9999/foo  foo database on 192.168.0.5 machine on port 9999
        "[::1]:9999/foo"      foo database on ::1 machine on port 9999 (IPv6 connection)
    :return: a tuple with ``(host, port, db name)``. If one or more value aren't in the `address`
    string, ``None`` replace it in the tuple
    """
    host = port = dbname = None
    if '/' in address:
        try:
            host, dbname = address.split('/')
        except ValueError:
            error('Invalid address "%s"' % address, EFAULT)
        else:
            if host.startswith("[") and "]" in host:
                # IPv6 address
                # See http://api.mongodb.org/python/2.8/api/pymongo/connection.html
                # If the connection is refused, you have to ensure that `mongod`
                # is running with `--ipv6` option enabled, and "bind_ip" value are
                # disabled in `mongod.conf`, or is enabled with your
                # IPv6 address in the list.
                if "]:" in host:
                    port = host[host.index("]:")+2:]
                    host = host[:host.index("]:")+1]
            elif ':' in host:
                # IPv4 address
                try:
                    host, port = host.split(':')
                except ValueError:
                    error_parsing('Invalid host "%s"' % host)
            if port:
                try:
                    port = int(port)
                except ValueError:
                    error_parsing('Invalid port number "%s"' % port)
    else:
        dbname = address
    return host, port, dbname


def connect(address, username=None, password=None, auth_database=None):
    """
    Connect with `address`, and return a tuple with a :class:`~pymongo.MongoClient`,
    and a :class:`~pymongo.database.Database` object.
    :param address: a string representation with the db address
    :param username: username for authentication (optional)
    :param password: password for authentication. If username is given and password isn't,
    it's asked from tty.
    :param auth_database: authenticate the username and password against that database (optional).
    If not specified, the database specified in address will be used.
    :return: a tuple with ``(client, db)``
    """
    host,  port, dbname = get_host_port_db(address)
    try:
        client = MongoClient(host=host, port=port)
    except Exception as e:
        error("Error trying to connect: %s" % str(e), ECONNREFUSED)

    if username:
        if password is None:
            password = getpass.getpass()
        if auth_database is None:
            auth_database = dbname
        try:
            auth_db = client[auth_database]
            auth_db.authenticate(username, password)
        except Exception as e:
            error("Error trying to authenticate: %s" % str(e), -3)
    db = client[dbname]
    return client, db
