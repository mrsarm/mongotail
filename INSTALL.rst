Installing mongotail
====================

Prerequisites
-------------

* Python 2.6+ or Python 3.3+ (only tested with 2.7 and 3.4)
* PyMongo (tested with versions 2.8, 3.0, 3.2 and 3.4)


Installation
------------

Once you've installed the dependencies, and downloaded and unpacked
the mongotail source release, enter the directory where the archive
was unpacked, and run::

    python setup.py install

Note that you may need administrator/root privileges for this step, as
this command will by default attempt to install module to the Python
site-packages directory on your system.

For advanced options, please refer to the easy_install and/or the distutils
documentation.


Install requirements in Debian based Linux distribution
-------------------------------------------------------

First, install essential build packages and Python build tools with::

    $ apt-get install python-pip python-dev build-essential python-setuptools

Then install ``pymongo`` library with::

    $ pip install pymongo

Like the *Installation* instructions, you may need administrator/root privileges
for this step.
