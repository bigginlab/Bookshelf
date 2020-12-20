#!/usr/bin/env python3
"""
Copyright (C) 2010 University of Oxford. All rights reserved.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    This (refactored) version updated by Philip Biggin 2020.

"""


import pymysql
import sys


def _mysql_connect_():
    try:
        conn = pymysql.connect(host="",
                               user="",
                               passwd="",
                               db="")
    except pymysql.Error as e:
        sys.stderr.write("\nCannot connect to Bookshelf database. Error %d: %s." % (e.args[0], e.args[1]))
        sys.exit(1)
    return conn
