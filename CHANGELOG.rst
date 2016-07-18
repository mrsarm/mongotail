Mongotail changelog
===================


2.0.0
-----

* Added support to MongoDB 3.2 log format.
* Added SSL connection support.
* Added ``-m``, ``--metadata`` option to add extra metadata fields to show.
* Added ``-v``, ``--verbose`` option to print all the operations in
  JSON without format.
* Added ``-i``, ``--info`` option to get information about the server
  we're connected to.
* Added flush calls after output to the ``stderr`` file.
* Added more validations to db address parameter.


1.1.0
-----

* Added support to ``UUID`` data type.
* Fixed formatting error of ``ISODate`` data type when year < 1900 in Python 2.7.
* Fixed unknown operation "createIndexes" output.
* Fixed undesirable operations filters.


1.0.1
-----

* Fixed authentication default mechanism error in MongoDB 3.0
  when user and password are used.


1.0.0
-----

* Added support for authentication against another database with
  ``--authenticationDatabase`` option.
* Fixed unknown operation "killcursors" output.


0.3.2
-----

* Added support to PyMongo 3.0+ due its incompatibility with previous
  versions on some API calls.
* When user press Ctrl+"C" now mongotail append a "\n" character to stdout.
* Rollback how javascript code is trimmed.


0.3.1
-----

* Fixed "group" queries logging.


0.3.0
-----

* Added logging to "aggregate", "distinct", "findandmodify",
  "map", "group" and "drop" queries.


0.2.0
-----

* Added "status" parameter to ``-l`` or ``-s`` options to see
  the current profiling levels. Also where the user changes
  the levels, a message in the output standard confirms the operation.
* Fixed imports to avoid install requires exception with ``pip``.
* Removed from MANIFEST invalid license file name entry.
* Changed arbitrary error exit codes by standard *errno* codes.
* Fixed documentation.


0.1.0
-----

First release.
