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

    Refactored in Dec 2020 by Philip Biggin

"""
import re
LEFT = 'left'
RIGHT = 'right'
CENTER = 'center'


def align(text, width=70, alignment=LEFT):
    ''' Align the "text" using the given alignment, padding to the given
    width.
    '''
    if alignment == CENTER:
        text = text.strip()
        space = width - len(text)
        return ' ' * (space / 2) + text + ' ' * (space / 2 + space % 2)
    elif alignment == RIGHT:
        text = text.rstrip()
        space = width - len(text)
        return ' ' * space + text
    else:
        text = text.lstrip()
        space = width - len(text)
        return text + ' ' * space


class FormatColumns:
    '''Format some columns of text with constraints on the widths of the
    columns and the alignment of the text inside the columns.
    '''
    def __init__(self, columns, contents, spacer=' | ', retain_newlines=True):
        assert len(columns) == len(contents), \
            'columns and contents must be same length'
        self.columns = columns
        self.num_columns = len(columns)
        self.contents = contents
        self.spacer = spacer
        self.retain_newlines = retain_newlines
        self.positions = [0] * self.num_columns

    def format_line(self, wsre=re.compile(r'\s+')):
        ''' Fill up a single row with data from the contents.
        '''
        temp_line = []
        data = False
        for i, (width, alignment) in enumerate(self.columns):
            content = self.contents[i]
            col = ''
            while self.positions[i] < len(content):
                word = content[self.positions[i]]
                if '\n' in word:
                    self.positions[i] += 1
                    if self.retain_newlines:
                        break
                    word = word.strip()

                # To make sure this word fits
                if col and len(word) + len(col) > width:
                    break
                # no whitespace at start-of-line
                if wsre.match(word) and not col:
                    self.positions[i] += 1
                    continue

                col += word
                self.positions[i] += 1
            if col:
                data = True
            col = align(col, width, alignment)
            temp_line.append(col)

        if data:
            return self.spacer.join(temp_line).rstrip()

        return ''

    def format(self, splitre=re.compile(r'(\n|\r\n|\r|[ \t]|\S+)')):
        for i, content in enumerate(self.contents):
            self.contents[i] = splitre.findall(content)

        # now process line by line
        temp_line = []
        line = self.format_line()
        while line:
            temp_line.append(line)
            line = self.format_line()
        return '\n'.join(temp_line)

    def __str__(self):
        return self.format()


def wrap(text, width=75, alignment=LEFT):
    return FormatColumns(((width, alignment),), [text])
