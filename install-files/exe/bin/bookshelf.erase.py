#!/usr/bin/python
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

    refactored and updated by Philip Biggin 2020

"""
try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass

import sys
import MySQLdb
import shutil
import optparse


class Erase_TrajData:
    def __init__(self, required_options):
        class Check_OptionParser (optparse.OptionParser):
            def _check_required_(self, opt):
                option = self.get_option(opt)
                # Assumes the option's 'default' is set to None!
                if (getattr(self.values, option.dest) is None):
                    self.error("\n %s option not supplied" % option)
        usage = """\n \n \"%prog -e <TrajId> \" The program deletes the entry based on the TrajId. "
                                            "You can provide a list of IDs as arguments with or "
                                            "without the erase option.
"""
        self.parser = Check_OptionParser(usage=usage)
        self._erase_options_()
        (self.options, self.args) = self.parser.parse_args()
        for req_option in required_options:
            self.parser._check_required_(req_option)

    def _erase_options_(self):        # function to parse the search option
        self.parser.add_option("-e", "--erase", action="store", dest="eraseOpt",
                               help="\nEnter the trajId to delete the entry.")


if __name__ == "__main__":
    from mysql_connect import _mysql_connect_    # connection to the bookshelf database
    conn = _mysql_connect_()
    cursor = conn.cursor()
    homeDir = "defaultpath"  # PATH - has to be set after installing the bookshelf folder
    dataParser = Erase_TrajData(("-e",))  # parsing data
    options = dataParser.options
    eraseOption = options.eraseOpt  # options
    trajIdList = dataParser.args  # args
    if eraseOption:
        fileName = homeDir + "bookshelf/data/trajfiles/" + eraseOption  # PATH
        try:
            shutil.rmtree(fileName)  # delete folder
        except OSError as e:
            print("Error deleting the folder - %s. Exiting. Error no: %d Error- %s" % (fileName, e.args[0], e.args[1]))
            sys.exit(1)
        try:
            cursor.execute("delete from TrajFiles where TrajId = '%s'" % eraseOption)  # delete entry from the database
            print("Number of files deleted in TrajFiles database: %d" % cursor.rowcount)
            cursor.execute("delete from TrajData where TrajId = '%s'" % eraseOption)  # delete entry from the database
            print("Number of files deleted in TrajData database: %d " % cursor.rowcount)
        except (MySQLdb.ProgrammingError, MySQLdb.OperationalError) as error:
            print("Error deleting entries from database for trajid -%s. Error %d: %s"
                  % (eraseOption, error.args[0], error.args[1]))
            sys.exit(1)

    if trajIdList:
        for items in trajIdList:
            items = items.strip()
            fileName = homeDir + "bookshelf/data/trajfiles/" + items  # PATH
            try:
                shutil.rmtree(fileName)
            except OSError as e:
                print("Error deleting folder - %s. Exiting!Error no: %s Error- %s." % (fileName, e.args[0], e.args[1]))
                sys.exit(1)
            try:
                cursor.execute("Delete from TrajFiles where TrajId = '%s'" % items)  # delete entry from the database
                print("Number of files deleted in TrajFiles database: %d" % cursor.rowcount)
                cursor.execute("delete from TrajData where TrajId = '%s'" % items)  # delete entry from the database
                print("Number of files deleted in TrajData database: %d" % cursor.rowcount)
            except (MySQLdb.ProgrammingError, MySQLdb.OperationalError) as error:
                print("Error deleting entries from database for trajid -%s. Error %d: %s"
                      % (items, error.args[0], error.args[1]))
                sys.exit(1)

    conn.commit()
    cursor.close()
    conn.close()
