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

    Refactored by Philip Biggin 20202

"""

import formatText
import pymysql
import optparse
import sys
from dbConnect import _dbConnect_

#  STILL NEEEDS FIXING- Just need to parse the args dont' we?


class Search_TrajData:

    def __init__(self, options="", args=""):
        self.options = options
        self.args = args
        self._search_options_()

    def _search_options_(self):        # function to parse the search option
        self.parser = optparse.OptionParser(usage='usage: %prog -s <search keywords>   The program looks for '
                                                  'keywords in protein name, programe name, user comments, '
                                                  'username or trajid')
        self.parser.add_option("-s", "--search", action="store", dest="SearchOpt",
                               help="\nEnter the keyword to search the database.")
        (self.options, self.args) = self.parser.parse_args()
        if not self.options.SearchOpt:   # if no search options provided
            self.parser.error('No search options given')


def WriteData(rows, searchWord):
    header = "\n \"Results of your search based on - %s\"" % searchWord  # PATH
    print(("\x1B[1m%s\x1B[0m\n" % header))
    print(('-' * 200))
    dim = [(25, 'LEFT'), (10, 'LEFT'), (10, 'LEFT'), (20, 'LEFT'),
           (10, 'LEFT'), (50, 'LEFT'), (5, 'LEFT'), (30, 'LEFT'), (10, 'LEFT')]
    column_name = ['TRAJID', 'USERNAME', 'DATE', 'PROTEIN NAME', 'PROGRAM CODE', 'USER COMMENTS', 'PMF', 'DOI', 'PUBID']
    data = formatText.FormatColumns(dim, column_name)
    print(("\x1B[1m%s\x1B[0m" % data))
    print(('-' * 200))
    for row in rows:
        b = list(row)
        data = formatText.FormatColumns(dim, b)
        print(data)
        print(('-' * 200))


if __name__ == "__main__":
    DataParser = Search_TrajData()
    options = DataParser.options
    KeyWords = DataParser.args
    searchOption = options.SearchOpt
    conn = _dbConnect_()
    cursor = conn.cursor()
    if searchOption:
        if searchOption == "all":
            try:
                cursor.execute("Select TrajId, UserName, DATE_FORMAT(Date,'%d/%m/%y')as Date,\
                                ProteinName, ProgramCode, UserComments, PmfOption, Doi, Pid from TrajData")
            except (pymysql.ProgrammingError, pymysql.OperationalError) as error:
                print(("Error browsing the database. Error %d: %s" % (error.args[0], error.args[1])))
                sys.exit(1)
            rows = cursor.fetchall()
            WriteData(rows, searchOption)
        else:
            try:
                cursor.execute("Select TrajId, UserName, DATE_FORMAT(Date,'%d/%m/%y')as Date,\
                                ProteinName, ProgramCode, UserComments, PmfOption, Doi, Pid from TrajData\
                                where ProteinName like '%" + searchOption + "%' OR UserName \
                                like '%" + searchOption + "%'OR ProgramCode like '%" + searchOption + "%' OR \
                                UserComments like '%" + searchOption + "%'OR TrajId like '%" + searchOption + "%'")
            except (pymysql.ProgrammingError, pymysql.OperationalError) as error:
                print(("Error browsing the database. Error %d: %s" % (error.args[0], error.args[1])))
                sys.exit(1)
            rows = cursor.fetchall()
            if rows:
                WriteData(rows, searchOption)
            else:
                print("\nNo match found.")

    if KeyWords:
        if KeyWords[0] == "all":
            try:
                cursor.execute("Select TrajId, UserName, DATE_FORMAT(Date,'%d/%m/%y')as Date,\
                                ProteinName, ProgramCode, UserComments, PmfOption, Doi, Pid from TrajData")
            except (pymysql.ProgrammingError, pymysql.OperationalError) as error:
                print(("Error browsing the database. Error %d: %s" % (error.args[0], error.args[1])))
                sys.exit(1)
            rows = cursor.fetchall()
            if rows:
                WriteData(rows, KeyWords)
            else:
                print("\nNo match found.")
        else:
            for items in KeyWords:
                try:
                    cursor.execute("Select TrajId, UserName, DATE_FORMAT(Date,'%d/%m/%y')as Date,\
                                    ProteinName, ProgramCode, UserComments, PmfOption, Doi, Pid from TrajData\
                                    where ProteinName like '%" + items + "%' OR UserName \
                                    like '%" + items + "%'OR ProgramCode like '%" + items + "%' OR \
                                    UserComments like '%" + items + "%'OR TrajId like '%" + items + "%'")
                except (pymysql.ProgrammingError, pymysql.OperationalError) as error:
                    print(("Error browsing the database. Error %d: %s" % (error.args[0], error.args[1])))
                    sys.exit(1)
                rows = cursor.fetchall()
                if rows:
                    WriteData(rows, KeyWords)
                else:
                    print("\nNo match found.")
