Mongotail
=========

Mongotail, Log all `MongoDB <http://www.mongodb.org>`_ queries in a *"tail"able* way.

``mongotail`` is a command line tool to outputs any operation from a Mongo
database in the standard output. You can see the operations collected by the
database profiler from a console, or redirect the result to a file, pipes
it with ``grep`` or other command line tool, etc.

The syntax is very similar to ``mongo`` client, and the output, as like
``tail`` command will be the latest 10 lines of logging.

But the more interesting feature (also like ``tail``) is to see the changes
in *"real time"* with the ``-f`` option, and occasionally filter the result
with ``grep`` to find a particular operation.

Syntax
------

Usage::

    mongotail [db address] [options]

"db address" can be:

+----------------------+-------------------------------------------------------------+
| foo                  | foo database on local machine (IPv4 connection)             |
+----------------------+-------------------------------------------------------------+
| 192.169.0.5/foo      | foo database on 192.168.0.5 machine                         |
+----------------------+-------------------------------------------------------------+
| remotehost/foo       | foo database on *remotehost* machine                        |
+----------------------+-------------------------------------------------------------+
| 192.169.0.5:9999/foo | foo database on 192.168.0.5 machine on port 9999            |
+----------------------+-------------------------------------------------------------+
| "[::1]:9999/foo"     | foo database on ::1 machine on port 9999 (IPv6 connection)  |
+----------------------+-------------------------------------------------------------+


Optional arguments:

-u USERNAME, --username USERNAME
                      username for authentication
-p PASSWORD, --password PASSWORD
                      password for authentication. If username is given and
                      password isn't, it's asked from tty
-b AUTH_DATABASE, --authenticationDatabase AUTH_DATABASE
                      database to use to authenticate the user. If not
                      specified, the user will be authenticated against the
                      database specified in the [db address]
-n N, --lines N       output the last N lines, instead of the last 10. Use
                      ALL value to show all lines
-f, --follow          output appended data as the log grows
-l LEVEL, --level LEVEL
                      specifies the profiling level, which is either 0 for
                      no profiling, 1 for only slow operations, or 2 for all
                      operations. Or use with 'status' word to show the
                      current level configured. Uses this option once before
                      logging the database
-s MS, --slowms MS    sets the threshold in milliseconds for the profile to
                      consider a query or operation to be slow (use with
                      `--level 1`). Or use with 'status' word to show the
                      current milliseconds configured
-m, --metadata        extra metadata fields to show. Know fields (may vary
                      depending of the operation and the MongoDB version):
                      millis, nscanned, docsExamined, execStats, lockStats ...
-i, --info            get information about the MongoDB server we're connected to
-v, --verbose         verbose mode (not recommended). All the operations will
                      printed in JSON without format and with all the
                      information available from the log
--ssl                 creates the connection to the server using SSL
--sslCertFile SSL_CERT_FILE
                      certificate file used to identify the local connection
                      against MongoDB
--sslKeyFile SSL_KEY_FILE
                      private keyfile used to identify the local connection
                      against MongoDB. If included with the certfile then
                      only the sslCertFile is needed
--sslCertReqs SSL_CERT_REQS
                      specifies whether a certificate is required from the
                      other side of the connection, and whether it will be
                      validated if provided. It must be any of three values:
                      0 (certificate ignored), 1 (not required, but
                      validated if provided), 2 (required and validated)
--sslCACerts SSL_CA_CERTS
                      file that contains a set of concatenated
                      "certification authority" certificates, which are used
                      to validate certificates passed from the other end of
                      the connection
--sslPEMPassword SSL_PEM_PASSPHRASE
                      password or passphrase for decrypting the private key
                      in sslCertFile or sslKeyFile. Only necessary if the
                      private key is encrypted
--sslCrlFile SSL_CRLFILE
                      path to a PEM or DER formatted certificate revocation
                      list
-h, --help            show this help message and exit
-V, --version         show program's version number and exit


Enabling Database Profiling and Showing Logs
--------------------------------------------

You have to activate first in the current database the
`profiler <http://docs.mongodb.org/manual/reference/method/db.setProfilingLevel>`_,
so MongoDB will capture all the activity in a special document that is read by Mongotail.

You can achieve this with ``-l, --level`` option. For example, if you want to see the logs
from MYDATABASE, first you have to execute this::

    $ mongotail MYDATABASE -l 2

Then you can see the latest lines of logging with::

    $ mongotail MYDATABASE
    2015-02-24 19:17:01.194 QUERY  [Company] : {"_id": ObjectId("548b164144ae122dc430376b")}. 1 returned.
    2015-02-24 19:17:01.195 QUERY  [User] : {"_id": ObjectId("549048806b5d3db78cf6f654")}. 1 returned.
    2015-02-24 19:17:01.196 UPDATE [Activation] : {"_id": "AB524"}, {"_id": "AB524", "code": "f2cbad0c"}. 1 updated.
    2015-02-24 19:17:10.729 COUNT  [User] : {"active": {"$exists": true}, "firstName": {"$regex": "mac"}}
    ...

To Connect with SSL or a remote Mongo instance, check the options with ``mongotail --help`` command.

**NOTE**: The level chosen can affect performance. It also can allow the
server to write the contents of queries to the log, which might have
information security implications for your deployment. Remember to setup your
database profiling level to ``0`` again after debugging your data::

    $ mongotail MYDATABASE -l 0


Installation
------------

You can install the latest stable version with ``pip`` in your environment with::

    $ pip install mongotail

Execute this command with administrator/root privileges.

You have to be installed ``pip`` tool first. In Debian/Ubuntu Linux
distribution you can install it with (also with root privileges)::

    $ apt-get install python-pip python-dev

See `<INSTALL.rst>`_ guide to install from sources.


About
-----

Project: https://github.com/mrsarm/mongotail

Authors: (2015) Mariano Ruiz <mrsarm@gmail.cm>

Changelog: `<CHANGELOG.rst>`_

License: GPL-3
