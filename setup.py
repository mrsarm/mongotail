# -*- coding: utf-8 -*-
##############################################################################
#
#  Mongotail, Log all MongoDB queries in a "tail"able way.
#  Copyright (C) 2015-2022 Mariano Ruiz <https://github.com/mrsarm/mongotail>
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
from os.path import abspath, dirname, join
from mongotail import __version__, __license__, __doc__, __url__


def read(*pathcomponents):
    """Read the contents of a file located relative to setup.py"""
    with open(join(abspath(dirname(__file__)), *pathcomponents)) as thefile:
        return thefile.read()

setup(
    name = 'mongotail',
    version=__version__,
    license=__license__,
    url=__url__,
    download_url=__url__ + '/tarball/' + __version__,
    author='Mariano Ruiz',
    author_email='mrsarm@gmail.com',
    description=__doc__,
    long_description=read('README.rst'),
    packages=[
        'mongotail',
    ],
    zip_safe=False,
    platforms='any',
    install_requires=[
        'pymongo>=3.12,<5.0.0',
        'res-address',
    ],
    entry_points={
        'console_scripts': [
            'mongotail = mongotail.mongotail:main',
        ],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Topic :: Database',
        'Topic :: Utilities',
        'Topic :: Terminals',
        'License :: Public Domain',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
