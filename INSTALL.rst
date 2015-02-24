Installing mongotail
====================

Prerequisites
-------------

* Python 2.6+ or Python 3.3+ (only tested with 2.7 and 3.4)
* pymongo (only tested with version 2.8)


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
