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

"""
import os,sys,pwd,datetime
import MySQLdb,shutil
import optparse
from optparse import OptionParser
import formatText
from dbConnect import _dbConnect_

class Search_TrajData:                
	def __init__(self,required_options):
		class Check_OptionParser (optparse.OptionParser):
    			def _check_required_ (self, opt):
        			option = self.get_option(opt)
				
        			# Assumes the option's 'default' is set to None!
				if (getattr(self.values, option.dest) == None):
					self.error("\n %s option not supplied." % option)
		usage = """\n \n \"%prog -s <search keywords> \" The program looks for the keywords in protein name, program name, user comments, username or trajid.
"""
		self.parser = Check_OptionParser(usage=usage)
		self._search_options_()
		(self.options, self.args) = self.parser.parse_args()	
		for req_option in required_options:
        		self.parser._check_required_(req_option)
		
	def _search_options_(self):		# function to parse the search option
    		self.parser.add_option("-s", "--search", action="store", dest="SearchOpt",
                      help="\nEnter the keyword to search the database.")

def WriteData(rows,searchWord):
	header= "\n \"Results of your search based on - %s\"" %searchWord#PATH
	print ("\x1B[1m%s\x1B[0m\n" % header)	
	print '-'*200
	dim=[(25,'LEFT'),(10,'LEFT'),(10,'LEFT'),(20,'LEFT'),(10,'LEFT'),(50,'LEFT'),(5,'LEFT'),(30,'LEFT'),(10,'LEFT')]
	column_name=['TRAJID','USERNAME','DATE','PROTEIN NAME','PROGRAM CODE','USER COMMENTS','PMF','DOI','PUBID']
	data=formatText.FormatColumns(dim,column_name)
	print("\x1B[1m%s\x1B[0m" % data)
	print '-'*200
	for row in rows:
		b=list(row)
		data=formatText.FormatColumns(dim,b)
		print data
		print '-'*200

if __name__ == "__main__":
	DataParser = Search_TrajData(("-s",) )
	options = DataParser.options
	KeyWords = DataParser.args
	searchOption=options.SearchOpt
	conn=_dbConnect_()
	cursor=conn.cursor()
	if searchOption:
		if searchOption =="all":
			try:
				cursor.execute(
		    	"Select TrajId,UserName,DATE_FORMAT(Date,'%d/%m/%y')as Date,ProteinName,ProgramCode,UserComments,PmfOption,Doi,Pid from TrajData")
			except (MySQLdb.ProgrammingError, MySQLdb.OperationalError), error:
				print "Error browsing the database. Error %d: %s" % (error.args[0], error.args[1])
				sys.exit(1)
			rows = cursor.fetchall()	
			WriteData(rows,searchOption)
		else:
			try:
				cursor.execute(
		    		"Select TrajId,UserName,DATE_FORMAT(Date,'%d/%m/%y')as Date,ProteinName,ProgramCode,UserComments,PmfOption,Doi,Pid from TrajData where ProteinName like '%"+ searchOption +"%' OR UserName like '%"+ searchOption +"%'OR ProgramCode like '%"+ searchOption +"%' OR UserComments like '%"+ searchOption +"%'OR TrajId like '%"+ searchOption +"%'")
			except (MySQLdb.ProgrammingError, MySQLdb.OperationalError), error:
				print "Error browsing the database. Error %d: %s" % (error.args[0], error.args[1])
				sys.exit(1)
			rows = cursor.fetchall()
			if rows:
				WriteData(rows,searchOption)
			else:
				print "\nNo match found."

	if KeyWords:
		if KeyWords[0] =="all": 
			try:
				cursor.execute(
		    		"Select TrajId,UserName,DATE_FORMAT(Date,'%d/%m/%y')as Date,ProteinName,ProgramCode,UserComments,PmfOption,Doi,Pid from TrajData")
			except (MySQLdb.ProgrammingError, MySQLdb.OperationalError), error:
				print "Error browsing the database. Error %d: %s" % (error.args[0], error.args[1])
				sys.exit(1)
			rows = cursor.fetchall()
			if rows:
				WriteData(rows,KeyWords)
			else:
				print "\nNo match found."
		else:
			for items in KeyWords:
				try:
					cursor.execute(
		    			"Select TrajId,UserName,DATE_FORMAT(Date,'%d/%m/%y')as Date,ProteinName,ProgramCode,UserComments,PmfOption,Doi,Pid from TrajData where ProteinName like '%"+ items +"%' OR UserName like '%"+ items +"%'OR ProgramCode like '%"+ items +"%' OR UserComments like '%"+ items +"%'OR TrajId like '%"+ items +"%'")
				except (MySQLdb.ProgrammingError, MySQLdb.OperationalError), error:
					print "Error browsing the database. Error %d: %s" % (error.args[0], error.args[1])
					sys.exit(1)
				rows = cursor.fetchall()
				if rows:
					WriteData(rows,KeyWords)
				else:
					print "\nNo match found."

