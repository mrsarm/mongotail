Mongotail
=========

Mongotail, Log all MongoDB queries in a *"tail"able* way.

``mongotail`` is a command line tool to outputs any operation from a Mongo
database in the standard output. You can see the operations from
a console, or redirect the result to a file, pipes it with ``grep`` or other
command line tool, etc.

The syntax is very similar to ``mongo`` client, and the output, as like
the ``tail`` command will be the latest 10 lines of logging.

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
| 192.169.0.5:9999/foo | foo database on 192.168.0.5 machine on port 9999            |
+----------------------+-------------------------------------------------------------+
| "[::1]:9999/foo"     | foo database on ::1 machine on port 9999 (IPv6 connection)  |
+----------------------+-------------------------------------------------------------+

Optional arguments:

    -u USERNAME           username for authentication
    -p PASSWORD, --password PASSWORD
                          password for authentication. If username is given and
                          password isn't, it's asked from the tty.
    -n N, --lines N       output the last N lines, instead of the last 10. Use
                          ALL value to show all lines
    -f, --follow          output appended data as the log grows
    -h, --help            show help message and exit
    --version             show program's version number and exit


Installation
------------

You can install the latest stable version with ``pip`` in your environment::

    $ pip install mongotail

See ``INSTALL.rst`` guide to install from the sources.


About
-----

Project: https://github.com/mrsarm/mongotail

Authors: (2015) Mariano Ruiz <mrsarm@gmail.cm>

License: GPL-3
