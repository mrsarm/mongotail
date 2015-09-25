Mongotail changelog
===================


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
