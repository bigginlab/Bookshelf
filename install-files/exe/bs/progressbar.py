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

    Refactored in Dec 2020 by Philip Biggin
"""


class progressBar:
    def __init__(self, minValue=0, maxValue=10, totalWidth=12):
        self.progBar = "[]"  # print the progress bar within brackets
        self.min = minValue
        self.max = maxValue
        self.span = maxValue - minValue
        self.width = totalWidth
        self.amount = 0
        self.updateAmount(0)  # Build progress bar string

    def updateAmount(self, newAmount=0):
        if newAmount < self.min:
            newAmount = self.min
        if newAmount > self.max:
            newAmount = self.max
        self.amount = newAmount

        # Figure out the new percent done, round to an integer
        diffFromMin = float(self.amount - self.min)
        percentDone = (diffFromMin / float(self.span)) * 100.0
        percentDone = round(percentDone)
        percentDone = int(percentDone)
        percentString = str(percentDone) + "% done"
        self.progBar = "[ " + percentString + " ]"

    def __str__(self):
        return str(self.progBar)


def myReportHook(newDirSize, totalSize):
    import sys
    global prog
    prog = ""
    if prog == "":
        prog = progressBar(0, totalSize, 20)
        prog.updateAmount(newDirSize)
        sys.stdout.flush()
        sys.stderr.write(str(prog))
        sys.stderr.write("\r")
