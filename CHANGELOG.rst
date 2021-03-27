Mongotail changelog
===================


2.4.1
-----

* Fix bug cause "aggregate" queries not be logged.
* Minor rewording of the messages used when
  the user checks or changes the profiling level.


2.4.0
-----

* Added support to cursor pagination
  arguments in queries: ``limit`` and ``skip``.


2.3.0
-----

* Added BSON ``Timestamp`` type support.
* Moved address parsing code to a new library
  called ``res-address`` that now it's a
  Mongotail's dependency.
* Support addresses as ``:PORT/DBNAME``,
  eg. ``mongotail :123/test``.
* Improved address validations.


2.2.0
-----

* Added support to MongoDB 3.6 log format.
* Added binary data support (``BinData`` type).
* Added python version info to ``--version`` option.
* Now ``insert`` operations with just one document inserted
  are showed without ``[]`` notation
* Fixed error when ``insert`` operations doesn't have
  recorded the document saved in the profiler


2.1.2
-----

* Fixed #20 CPU runaway using ``-f`` option with local
  connections.
* Avoid ``IOError: [Errno 32] Broken pipe`` that some
  times is launched when ``Ctrl+C`` is used.


2.1.1
-----

* On ``TypeError`` exceptions dump the output with
  warn message instead of exit the program.
* Filtered ``explain`` queries from the log.


2.1.0
-----

* Support ``sort`` parameters logging (compatible with MongoDB 3.2+).
* Support ``NumberDecimal`` type (MongoDB 3.4+).
* Added Docker support.
* Fixed #15 Exception when list collection indexes.


2.0.2
-----

* Fixed exception with ``$out`` operator in aggregation operations.


2.0.1
-----

* Fixed #12 Error when explore the database collections with MongoChef tool.
* Fixed #13 Error "close failed in file object destructor..." after closing
  ``mongotail -f`` piped with some other command.
* Avoid output of empty metadata results.


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
