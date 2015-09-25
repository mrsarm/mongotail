# -*- coding: utf-8 -*-
##############################################################################
#
#  Mongotail, Log all MongoDB queries in a "tail"able way.
#  Copyright (C) 2015 Mariano Ruiz (<http://mrdev.com.ar>).
#
#  Author: Mariano Ruiz <mrsarm@gmail.com>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


from setuptools import setup
from mongotail import __version__, __license__, __doc__, __url__


setup(
    name = 'mongotail',
    version=__version__,
    license=__license__,
    url=__url__,
    download_url=__url__ + '/tarball/' + __version__,
    author='Mariano Ruiz',
    author_email='mrsarm@gmail.com',
    description=__doc__,
    packages=[
        'mongotail',
    ],
    zip_safe=False,
    platforms='any',
    install_requires=[
        'pymongo>=2.8',
    ],
    entry_points = {
        'console_scripts': [
            'mongotail = mongotail.mongotail:main',
        ],
    },
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: Public Domain',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Database',
    ],
)
