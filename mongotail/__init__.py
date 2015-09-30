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


__author__ = 'Mariano Ruiz'
__version__ = '1.1.0'
__license__ = 'GPL-3'
__url__ = 'https://github.com/mrsarm/mongotail'
__doc__ = """Mongotail, Log all MongoDB queries in a "tail"able way."""
__usage__ = """%(prog)s [db address] [options]

db address can be:
  foo                   foo database on local machine (IPv4 connection)
  192.169.0.5/foo       foo database on 192.168.0.5 machine
  192.169.0.5:9999/foo  foo database on 192.168.0.5 machine on port 9999
  "[::1]:9999/foo"      foo database on ::1 machine on port 9999 (IPv6 connection)"""
