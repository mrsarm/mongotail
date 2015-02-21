Mongotail
=========

Mongotail, Log all MongoDB queries in a *"tail"able* way.

``mongotail`` is a command line tool to outputs any operation from a Mongo
database in the standard output. You can see the operations collected by the
database profiler from a console, or redirect the result to a file, pipes
it with ``grep`` or other command line tool, etc.

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

**NOTE**: You have to active first in the current database the
`profiler <http://docs.mongodb.org/manual/reference/method/db.setProfilingLevel>`_,
so MongoDB will capture all the activity in a special document that is read by Mongotail.
See `Enable Database Profiling.. <http://docs.mongodb.org/manual/tutorial/manage-the-database-profiler/#enable-database-profiling-and-set-the-profiling-level>`_
to read how to active it.


Installation
------------

You can install the latest stable version with ``pip`` in your environment with::

    $ pip install mongotail

See `<INSTALL.rst>`_ guide to install from sources.


TODO
----

Project under construction. It's working now, but these are some tasks to do:

- Output some BSON types in a more convenient format
  (like ObjectId and Timestamp types).
- Enable / Disable profiler from the command (without the need to do
  from an external client).
- Publish it in *PyPI* repository (for now install from sources).
- More documentation, and better english to write it  :-)


About
-----

Project: https://github.com/mrsarm/mongotail

Authors: (2015) Mariano Ruiz <mrsarm@gmail.cm>

License: GPL-3
