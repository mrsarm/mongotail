# -*- coding: utf-8 -*-
##############################################################################
#
#  Mongotail, Log all MongoDB queries in a "tail"able way.
#  Copyright (C) 2015-2022 Mariano Ruiz <https://github.com/mrsarm/mongotail>
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
from .err import error, error_parsing, ECONNREFUSED
from pymongo import MongoClient
from res_address import get_res_address, AddressError


def connect(address, args):
    """
    Connect with `address`, and return a tuple with a :class:`~pymongo.MongoClient`,
    and a :class:`~pymongo.database.Database` object.
    :param address: a string representation with the db address
    :param args: connection arguments:
    - username: username for authentication (optional)
    - password: password for authentication. If username is given and password isn't,
      it's asked from tty.
    - auth_database: authenticate the username and password against that database (optional).
      If not specified, the database specified in address will be used.
    - tls, tlsCertificateKeyFile, tlsAllowInvalidCertificates, ...: TSL authentication options
    :return: a tuple with ``(client, db)``
    """
    try:
        host,  port, dbname = get_res_address(address)
    except AddressError as e:
        error_parsing(str(e).replace("resource", "database"))

    try:
        options = {}
        if args.tls:
            options["tls"] = True
            if args.tlsCertificateKeyFile:
                options["tlsCertificateKeyFile"] = args.tlsCertificateKeyFile
            if args.tlsCertificateKeyFilePassword:
                options["tlsCertificateKeyFilePassword"] = args.tlsCertificateKeyFilePassword
            if args.tlsCAFile:
                options["tlsCAFile"] = args.tlsCAFile
            if args.tlsCRLFile:
                options["tlsCRLFile"] = args.tlsCRLFile
            if args.tlsAllowInvalidCertificates:
                options["tlsAllowInvalidCertificates"] = args.tlsAllowInvalidCertificates

        client = MongoClient(host=host, port=port, **options)
    except Exception as e:
        error("Error trying to connect: %s" % str(e), ECONNREFUSED)

    username = args.username
    password = args.password
    auth_database = args.auth_database

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
