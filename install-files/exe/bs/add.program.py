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

    Refactored in December 2020 by Philip Biggin

"""

import sys
import optparse
from xml.dom.minidom import Document


class Add_program:

    def __init__(self, options="", args=""):
        self.options = options
        self.args = args
        self._search_options_()

    def _search_options_(self):        # function to parse the search option
        self.parser = optparse.OptionParser(usage='usage: %prog -p <program name> <.ext1> <.ext2> <.ext3> <.ext4> '
                                                  '\n where program name is the software tool you want to add to the '
                                                  'existing list and ext1, ext2 ext3, ext4 etc.. are the extensions '
                                                  'for the input, topology, coordinate,trajectory files. '
                                                  '\n \n The program name is followed by -p flag and the extensions '
                                                  'are prived as arguments. \n \n The number of extensions can be more '
                                                  'than four depending on what files you want to make it mandatory '
                                                  'for the users to deposit while submitting a trajectory.')
        self.parser.add_option("-p", "--programme", action="store", dest="progname",
                               help='\nEnter the program name to be added followed by the extensions for the files '
                               'you want to make it mandatory for the users for the depostion of trajectory')
        (self.options, self.args) = self.parser.parse_args()
        if not self.options.progname:   # if no programe name provided
            self.parser.error('No programme name given')


if __name__ == "__main__":
    DataParser = Add_program(("-p",))
    options = DataParser.options
    file_exts = DataParser.args
    pname = options.progname
    pname = pname.upper()
    flag = 'false'
    fileTemp = open("program.txt", 'r')
    for lines in fileTemp.readlines():
        lines = lines.strip("\n")
        if pname == lines:
            opt = eval(input("\nProgram name already exists. Do you want to overwrite? yes/no - "))
            if opt == "yes":
                flag = 'true'
            elif opt == "no":
                print("\nQuitting")
                sys.exit(1)
            else:
                print("\nInvalid option")
                sys.exit(1)

        else:
            pass
    fileTemp.close()

    if flag == 'false':
        fileTwo = open("program.txt", 'a')
        fileTwo.write("%s\n" % pname)

    fileOne = open("%s.xml" % pname, 'w')
    # Create the minidom document
    doc = Document()

    # Create the <program> base element
    program = doc.createElement("program")
    doc.appendChild(program)

    # Create the program name element
    progname = doc.createElement("progname")
    progname.setAttribute("name", pname)
    program.appendChild(progname)
    for item in file_exts:
        # Create a <file> element and give the <file> element some text
        item = item.lstrip(".")
        item = ".%s" % item
        newfile = doc.createElement("file")
        progname.appendChild(newfile)

        ptext = doc.createTextNode(item)
        newfile.appendChild(ptext)

    fileOne.write(doc.toprettyxml(indent="  "))
