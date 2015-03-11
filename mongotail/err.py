# -*- coding: utf-8 -*-
##############################################################################
#
#  Mongotail, Log all MongoDB queries in a "tail"able way.
#  Copyright (C) 2015 Mariano Ruiz (<https://github.com/mrsarm/mongotail>).
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


import sys
from errno import EINVAL, EINTR, ECONNREFUSED, EFAULT, EDESTADDRREQ


def warn(msg):
    sys.stderr.write("Mongotail EXCEPTION - %s\n" % msg)

def error(msg, exit_code):
    """
    Print `msg` error and exit with status `exit_code`
    """
    sys.stderr.write("%s\ntry '%s --help' for more information\n" % (msg, sys.argv[0]))
    exit(exit_code)


def error_parsing(msg="unknown options"):
    """
    Print any parsing error and exit with status -1
    """
    sys.stderr.write("Error parsing command line: %s\ntry '%s --help' for more information\n" % (msg, sys.argv[0]))
    exit(EINVAL)


def error_unknown():
    """
    Print an unexpected error and exit with status -5
    """
    sys.stderr.write("Unknown Error\ntry '%s --help' for more information\n" % sys.argv[0])
    exit(-1)
