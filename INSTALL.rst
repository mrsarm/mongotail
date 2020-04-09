Installing mongotail
====================

Prerequisites
-------------

* Python 3.3+ or 2.6+ Python (only tested with 2.7, 3.4, 3.5 and 3.7)
* PyMongo (tested with versions 2.8, 3.0, 3.2, 3.4, 3.9 and 3.10)


Installation
------------

Once you've installed the dependencies, and downloaded and unpacked
the mongotail source release, enter the directory where the archive
was unpacked, and run::

    python3 setup.py install

Note that you may need administrator/root privileges for this step, as
this command will by default attempt to install module to the Python
site-packages directory on your system.

For advanced options, please refer to the easy_install and/or the distutils
documentation.


Install requirements in Debian based Linux distribution
-------------------------------------------------------

First, install essential build packages and Python build tools with::

    $ apt-get install python3-pip python3-dev build-essential python3-setuptools

Then install ``pymongo`` library with::

    $ pip3 install pymongo

Like the *Installation* instructions, you may need administrator/root privileges
for this step.
