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

MongoDB version 2.8 and above are supported.

Syntax
------

Usage::

    mongotail [db address] [options]

"db address" can be:

+----------------------+-------------------------------------------------------------+
| foo                  | foo database on local machine (IPv4 connection)             |
+----------------------+-------------------------------------------------------------+
| :1234/foo            | foo database on local machine on port 1234                  |
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
-m METADATA, --metadata METADATA
                      extra metadata fields to show. Known fields may vary
                      depending of the operation and the MongoDB version:
                      millis, nscanned, docsExamined, execStats, lockStats ...
                      (pass each METADATA field separated by one space)
-i, --info            get information about the MongoDB server we're connected to
-v, --verbose         verbose mode (not recommended). All the operations will
                      printed in JSON without format and with all the
                      information available from the log
--tls                 creates the connection to the server using
                      transport layer security
--tlsCertificateKeyFile TLSCERTIFICATEKEYFILE
                      client certificate to connect against MongoDB.
                      It's the concatenation of both the private key and and
                      the certificate file
--tlsAllowInvalidCertificates
                      disable the requirement of a certificate from the
                      server when TLS is enabled
--tlsCAFile TLSCAFILE
                      file that contains a set of concatenated CA certificates,
                      which are used to validate certificates passed
                      from the other end of the connection
--tlsCertificateKeyFilePassword TLSCERTIFICATEKEYFILEPASSWORD
                      password or passphrase to decrypt the encrypted private
                      keys if the private key contained in the
                      certificate keyfile is encrypted.
--tlsCRLFile TLSCRLFILE
                      path to a PEM or DER formatted certificate revocation list
-h, --help            show this help message and exit
-V, --version         show program's version number and exit


Enabling Database Profiling and Showing Logs
--------------------------------------------

First you have to activate in the current database the
`profiler <http://docs.mongodb.org/manual/reference/method/db.setProfilingLevel>`_,
so MongoDB will capture all the activity in a special collection that is read by Mongotail.

You can achieve this with the ``-l, --level`` option. For example, if you want to see the logs
from MYDATABASE, first you have to execute::

    $ mongotail MYDATABASE -l 2

Then you can see the latest logged records with::

    $ mongotail MYDATABASE
    2015-02-24 19:17:01.194 QUERY  [Company] : {"_id": ObjectId("548b164144ae122dc430376b")}. 1 returned.
    2015-02-24 19:17:01.195 QUERY  [User] : {"_id": ObjectId("549048806b5d3db78cf6f654")}. 1 returned.
    2015-02-24 19:17:01.196 UPDATE [Activation] : {"_id": "AB524"}, {"_id": "AB524", "code": "f2cbad0c"}. 1 updated.
    2015-02-24 19:17:10.729 COUNT  [User] : {"active": {"$exists": true}, "firstName": {"$regex": "mac"}}
    ...

To Connect with SSL or a remote Mongo instance, check the options with ``mongotail --help``.

**NOTE**: The level chosen can affect performance. It also can allow the
server to write the content of queries to the log, which might have
information security implications for your deployment. Remember to setup your
database profiling level to ``0`` again after debugging your data::

    $ mongotail MYDATABASE -l 0

A *step-by-step* guide of how to use Mongotail and the latest features
is `here <http://mrsarm.blogspot.com.ar/2016/08/mongotail-2-0-with-new-features-mongodb-3-2-support.html>`_.


Installation
------------

See `INSTALL.rst <https://github.com/mrsarm/mongotail/blob/master/INSTALL.rst>`_
guide to install from sources. To install
from `PyPI repositories <https://pypi.org/project/mongotail/>`_,
follow these instructions depending of your OS:


Linux Installation
^^^^^^^^^^^^^^^^^^

You can install the latest stable version with ``pip`` in your
environment, but it's recommended to install it with
Python 3 (``pip3``)::

    $ pip3 install mongotail

Execute this command with administrator/root privileges (in
Debian/Ubuntu Linux distribution prepend ``sudo`` to the command).

You have to be installed ``pip`` / ``pip3`` tool first. In Debian/Ubuntu Linux
distribution you can install it with (also with root privileges)::

    $ apt-get install python3-pip

Install mongotail in the user space without root privileges is also
possible with::

    $ pip3 install --user mongotail

Note that the ``mongotail`` executable will be installed in the ``$HOME/.local/bin``
folder. If the folder didn't exist before, Pip will create it, but in the
shell console the path won't be added to the ``$PATH`` variable until Bash is not
instantiated again, so to be able to execute the command without the need to use
the full path (``$HOME/.local/bin/mongotail``) just open a new Bash session.


Mac OSX Installation
^^^^^^^^^^^^^^^^^^^^

First you need to install the Python package manager ``pip`` in
your environment, and then like Linux to install Mongotail you
can execute ``sudo pip install mongotail`` from the command line,
but also it can be installed with ``easy_install``, an
old Python package manager present in most OSX versions. Try this::

    $ sudo easy_install mongotail


Docker
^^^^^^

Run with Docker (you don't need to download the source code)::

    $ docker run -it --rm mrsarm/mongotail --help

If you want to connect with a database also running locally in a
container, you have to link both instances (see howto in the Docker
documentation), or if the db is a local instance running without
Docker, remember to use the local IP of your computer because the
``localhost`` address (IP 127.0.0.1) points to the container, not to
your host. Eg.::

    $ docker run -it --rm mrsarm/mongotail 192.168.0.21/test

If it does not work, it may be related with network access rules,
or because the mongo instance is not listening remote connections,
check to have properly configured the
`IP Binding <https://docs.mongodb.com/manual/core/security-mongodb-configuration/>`_.

About
-----

Project: https://github.com/mrsarm/mongotail

Authors: (2015-2022) Mariano Ruiz <mrsarm@g...l.com>

Changelog: `CHANGELOG.rst <https://github.com/mrsarm/mongotail/blob/master/CHANGELOG.rst>`_

More guides: http://mrsarm.blogspot.com.ar/search/label/Mongotail

License: GPL-3
