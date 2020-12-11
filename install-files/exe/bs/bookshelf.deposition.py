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

    Refactored by Philip Biggin 2020

"""
import os
import sys
import pwd
import datetime
import time
import shutil
import signal
import hashlib
import progressbar
import optparse
from xml.dom import minidom

homeDir = 'defaultpath'
destPath = homeDir + "bookshelf/temp/"  # PATH-The directory where the trajectories will be stored temporary


class Universal_Get_Options:
    #  PCB  - -   Reworked following into _get_trajdata  - - PCB
    # def __init__(self, required_options):
    #    class Check_OptionParser (optparse.OptionParser):
    #        def _check_required_(self, opt):
    #            option = self.get_option(opt)
    #        if getattr(self.values, option) is None:
    #            self.error("\n %s option not supplied" % option)

    #    usage = """\n \n \"%prog -m <protein name> -p <program name> -c <"comments"> -f <pmf> <file1> \
    #        <file2> <file3> <file4>\" \
    #       This program archives molecular dynamics trajectories in a central repository. All options \
    #        except -f are required. The -f flag accepts 'yes' or 'no' as values and the default value='no'. \
    #        The files themselves are given as command line arguments.You must always supply the trajectory \
    #        (eg a dcd or xtc), a structure (pdb), a topology (psf or top, itp, tpr), and a run input \
    #        (inp script, mdp). Additional files are simply added to the command line (such as additional\
    #        streaming str files or itps).To a minimum one should be able to \
    #        (1) analyze the simulation and \
    #        (2) rerun the simulation (possibly with changed parameters) using the files submitted. \
    #        The files with the appropriate extensions need to be deposited depending on the MD tool \
    #        used to generate the trajectory. \
    #        """
    #    self.parser = Check_OptionParser(usage=usage)
    #    self._get_trajdata_()
    #    (self.options, self.args) = self.parser.parse_args()
    #    for req_option in required_options:
    #        self.parser._check_required_(req_option)

    def _get_trajdata_(self):  # function to parse the options
        self.parser = optparse.OptionParser(usage='usage: %prog -m <protein name> -p <program name> -c <"comments"> -f \
            <pmf> -d <doi> -i pubmedID <file1> <file2> <file3> <file4>\
            This program archives molecular dynamics trajectories in a central repository. Protein name \
            program name and comments are required fields as are the four files \
            themselves, which are given as command line arguments. You must always supply the trajectory \
            (eg a dcd or xtc), a structure (pdb), a topology (psf or top, itp, tpr), and a run input \
            (inp script, mdp). Additional files are simply added to the command line (such as additional\
            streaming str files or itps).To a minimum one should be able to \
            (1) analyze the simulation and \
            (2) rerun the simulation (possibly with changed parameters) using the files submitted. \
            The files with the appropriate extensions need to be deposited depending on the MD tool \
            used to generate the trajectory.\
            The -f flag accepts "yes" or "no" as values and the default value="no".')

        self.parser.add_option("-m", "--molname", action="store", dest="molName",
                               help="\nEnter the name of the protein or the molecule.")
        self.parser.add_option("-p", "--program", action="store", dest="progName",
                               help="\nEnter the name of the MD tool used to generate the trajectory. \
                                   It accepts GROMACS/NAMD/CHARMM/GAUSSIAN.")
        self.parser.add_option("-c", "--comments", action="store", type="string", dest="userComments",
                               help="\nEnter brief comments about the trajectory in double quotes.")
        self.parser.add_option("-f", "--pmf", action="store", type="string", default="n", dest="pmf",
                               help="\nEnter the flag for pmf. It takes YES or NO as values and the \
                                   default is NO.")
        self.parser.add_option("-d", "--doi", action="store", type="string", default="none", dest="doi",
                               help="\nEnter the flag for doi. It takes the doi identifier (not the url) \
                                   and the default is set to NONE.")
        self.parser.add_option("-i", "--pid", action="store", type="string", default="none", dest="pid",
                               help="\nEnter the flag for pubmed id. It takes pubmed id (not the url) and \
                                   the default is set to NONE.")
        (options, args) = self.parser.parse_args()
        if not options.molName:
            self.parser.error('No name of protein or molecule given')
        if not options.progName:
            self.parser.error('No name of programe name given')
        if not options.userComments:
            self.parser.error('No comments provided')


class fileCheckOptions:
    # check if all the basic files relevant to run the simulation using the tool metioned are submitted
    def _file_check_(self, fileList, extList):
        for item in extList:
            if item not in fileList:
                print("\n ERROR!!! You have not entered \"%s\" file. You need to deposit all the files "
                      "required for deposition. \n The list inicludes files with extension \n%s \n" % (item, extList))
                sys.exit(1)


class Check_Options:
    def _program_check_(self, ProgName):  # function to check if the software tool exist in the list
        inFile = open(homeDir + "exe/bs/program.txt", 'r')
        ProgramList = []
        for lines in inFile.readlines():
            lines = lines.strip("\n")
            ProgramList.append(lines)
        if ProgName not in ProgramList:
            print("\n  \"ERROR!!!  Program option not in lookup list!\"  \n\n  \"List includes "
                  "GROMACS/NAMD/CHARMM/GAUSSIAN.\" ")
            sys.exit(1)
        else:
            return ProgName

    def _file_duplicate_check_(self, file_list):     # function to check if duplicate files have been submitted
        newFileList = []
        for files in range(len(file_list)):
            file_path, file_name = os.path.split(file_list[files])
            newFileList.append(file_name)
        for index, item in enumerate(newFileList):
            if newFileList[index] in newFileList[index + 1:]:
                print("\n ERROR!!! You have entered \"%s\" more than once. \n" % newFileList[index])
                sys.exit(1)

    def _file_checks_(self, file_list, ProgName):
        RemoveElements = []
        fileList = []
        for files in range(len(file_list)):  # check if the files exist in the directory mentioned in the filepath
            if file_list[files] == "":
                print("\n\"ERROR!!! Trailing comma at the end of the file_list,expecting files. \"")
                sys.exit(1)
            file_path, file_name = os.path.split(file_list[files])
            if file_path != "":
                if os.path.isfile(file_list[files]) is not True:
                    RemoveElements.append(file_list[files])
                else:
                    head, tail = os.path.splitext(file_name)
                    fileList.append(tail)
            elif file_path == "":
                if os.path.isfile(file_list[files]) is not True:
                    RemoveElements.append(file_list[files])
                else:
                    head, tail = os.path.splitext(file_list[files])
                    fileList.append(tail)

        for item in RemoveElements:
            print("\nERROR!!! \n\"File \"%s\" does not exist in the current or mentioned directory. \""
                  % file_list[files])
            sys.exit(1)
        extList = self.Get_ExtList(ProgName)
        fc = fileCheckOptions()
        fc._file_check_(fileList, extList)

    def Get_ExtList(self, progName):
        progFile = homeDir + 'exe/bs/%s.xml' % progName
        xmldoc = minidom.parse(progFile)
        extList = []
        rootNode = xmldoc.firstChild
        progNode = rootNode.childNodes[1]
        for nodes in progNode.childNodes:
            fileNode = nodes
            for node in fileNode.childNodes:
                x = node.toxml()
                x = ' '.join(x.split())
                extList.append(str(x))
        return extList


def createDestFolder(destFolder):
    try:
        os.mkdir(destFolder)
    except OSError as xxx_todo_changeme2:
        (errno, strerror) = xxx_todo_changeme2.args
        print('\n "ERROR!!! Cannot create destination folder. Exiting!!Error No -%s. Error-%s."' % errno, strerror)
        sys.exit(1)


def copydir(dirName, destfolderName):
    try:
        shutil.copytree(dirName, destfolderName)
    except OSError as xxx_todo_changeme3:
        (errno, strerror) = xxx_todo_changeme3.args
        print('\n "ERROR!!! %s was not copied due to system error. Error No -%s. Error-%s."'
              % (dirName, errno, strerror))
        sys.exit(1)


def calculateSize(folderName):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folderName):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size


def progress(dirName, destfolderName, totalSize):
    newDirSize = 0
    newpid = os.fork()
    if newpid == 0:
        time.sleep(5)
        while newDirSize < totalSize:
            newDirSize = os.stat(destfolderName).st_size
            progressbar.myReportHook(newDirSize, totalSize)
            time.sleep(40)
        sys.exit(1)
    else:
        copydir(dirName, destfolderName)
        os.kill(newpid, signal.SIGKILL)


def sizeError(errorList, trajFiles, checkSum, newCheckSum):
    newList = []
    newList.append(trajFiles)
    newList.append(checkSum)
    newList.append(newCheckSum)
    errorList.append(newList)
    return errorList


def _md5File_(FileName):
    fh = open(FileName)
    digest = hashlib.md5()
    while 1:
        buf = fh.read(4096)
        if buf == "":
            break
        digest.update(buf)
    fh.close()
    return digest.hexdigest()


def _md5Check_(FileName):
    checksum = 0
    try:
        checksum = _md5File_(FileName)  # create md5sum
        return checksum
    except:
        sys.stderr.write('\n "There was a problem with md5sum for file %s!!! "' % FileName)
        return checksum


if __name__ == "__main__":
    dataParser = Universal_Get_Options(("-m", "-p", "-c", "-f",))
    Options = dataParser.options     # passing the options print "\nThe trajid for your deposition is :%s" %trajId
    fileList = dataParser.args      # passing the arguments
    molName = Options.molName         # Read Options
    progName = (Options.progName).upper()
    userComments = Options.userComments
    pmf = Options.pmf
    doi = Options.doi
    pid = Options.pid
    userAccountInfo = pwd.getpwuid(os.getuid())
    userName = userAccountInfo[0]  # retrieve user name
    systemDate = datetime.datetime.now()   # date and time
    sysDate = systemDate.strftime("%Y%m%d%H%M%S")
    trajId = userName + sysDate
    destFolder = destPath + trajId  # PATH
    c = Check_Options()  # an object for the Check_Options class

    if doi.upper() != "NONE":
        doi = doi.strip("/")
        doilist = doi.split("/")
        if len(doilist) != 2:
            print("\nEnter the full doi identifier (10.001/pro0569104)  but not the url.\n")
            sys.exit(1)
    if pid.upper() != "NONE":
        pid = pid.strip("/")
        pidlist = pid.split("/")
        if len(pidlist) != 1:
            print("\nEnter only the pubmed id and not the full url.\n")
            sys.exit(1)
    print("\nThe trajid for your deposition is :%s" % trajId)
    errorList = []
    if pmf.upper() == "NO" or pmf.upper() == "N":
        setpmf = 'No'
        progName = c._program_check_(progName)     # calling the function to check the program
        c._file_duplicate_check_(fileList)        # to check if same file entered twice
        c._file_checks_(fileList, progName)          # to check if the files exist and are in the correct folder
        createDestFolder(destFolder)
        newFileDict = {}
        for trajFiles in fileList:
            file_path, file_name = os.path.split(trajFiles)
            if file_path == "":
                file_name = trajFiles
                checkSum = _md5Check_(file_name)  # create md5sum
                try:
                    shutil.copy(file_name, destFolder)
                except OSError as xxx_todo_changeme:
                    (errno, strerror) = xxx_todo_changeme.args
                    print('\n "ERROR!!! %s not copied due to system error. Please try again!! \
                          Error No -%s. Error-%s."' % (file_name, errno, strerror))
                    sys.exit(1)

            if file_path != "":
                checkSum = _md5Check_(trajFiles)
                try:
                    shutil.copy(trajFiles, destFolder)
                except OSError as xxx_todo_changeme1:
                    (errno, strerror) = xxx_todo_changeme1.args
                    print('\n "ERROR!!! %s not copied due to system error. Please try again!! \
                          Error No -%s. Error-%s."' % (trajFiles, errno, strerror))
                    sys.exit(1)

            newFile = "%s/%s" % (destFolder, file_name)
            newcheckSum = _md5Check_(newFile)
            if newcheckSum == checkSum:
                newFileDict[file_name] = checkSum
            else:
                print("\nError copying file -%s . Checksum varies!!! \n Original checksum=%s \
                      New checksum=%s." % (trajFiles, checkSum, newcheckSum))
                errorList = sizeError(errorList, trajFiles, checkSum, newcheckSum)
            print("%s copied" % trajFiles)

    elif pmf.upper() == "YES" or pmf.upper() == "Y":
        print('\n "**** This is a PMF deposition and will take several minutes.  ****"')
        setpmf = 'Yes'
        progName = c._program_check_(progName)
        if len(fileList) > 1:
            print(" \n ERROR!!! You have selected to submit PMF trajectories. Please place all "
                  "the files or subdirectories in a main directory and enter the name of the main directory.")
            sys.exit(1)
        else:
            dirName = str(fileList[0])

        if not os.path.isdir(dirName):
            print("\nERROR!!! The folder \"%s\" does not exist in the mentioned directory or the current "
                  "directory." % dirName)
            sys.exit(1)

        dir_size = calculateSize(dirName)
        totalSize = os.stat(dirName).st_size
        destfolder = destFolder + "/" + dirName
        createDestFolder(destFolder)
        progress(dirName, destfolder, totalSize)
        new_dir_size = calculateSize(destfolder)
        diff = abs(new_dir_size - dir_size)
        if diff == 0:
            pass
        else:
            print("\nError copying the \"%s\" folder. File size varies!!! \n Original size =%s "
                  "New size=%s." % (dirName, dir_size, new_dir_size))
            errorList = sizeError(errorList, dirName, dir_size, new_dir_size)
    else:
        print("\nERROR!!! You have used -f flag. Enter 'Yes' (if depositing pmf trajectories) or "
              "No (if not)for the -f option. Default ='No'.")
        sys.exit(1)

    try:
        outputFileOne = open("%s/%s.metadata" % (destFolder, trajId), 'w')
    except OSError as xxx_todo_changeme4:
        (errno, strerror) = xxx_todo_changeme4.args
        print(("\nError opening the file to write the metadata.Exiting!! Error No -%s. Error-%s." % (errno, strerror)))
        os.rmdir(destFolder)
        sys.exit(1)
    outputFileOne.write("USERNAME\t%s\nSYSTEMDATE\t%s\nMOLNAME\t%s\nPROGNAME\t%s\nUSERCOMMENTS\t%s\nPMFFLAG"
                        "\t%s\nDOI\t%s\nPID\t%s\nTRAJID\t%s" % (userName, systemDate, molName, progName,
                                                                userComments, setpmf, doi, pid, trajId))

    if setpmf == 'Yes':
        outputFileOne.write("\n%s\t%s" % (dirName, new_dir_size))
    elif setpmf == 'No':
        for trajFiles, checkSum in list(newFileDict.items()):
            outputFileOne.write("\n%s\t%s" % (trajFiles, checkSum))

    if errorList:
        outputFileOne.write("\nflag\tflagFalse")
        for newList in errorList:
            outputFileOne.write("\nsizeError\t")
            for items in newList:
                outputFileOne.write("%s\t" % items)
    else:
        outputFileOne.write("\nflag\tflagTrue")
    outputFileOne.close()

    try:
        os.system('chmod -R 777 %s' % destFolder)
    except OSError as xxx_todo_changeme5:
        (errno, strerror) = xxx_todo_changeme5.args
        print(("\nError changing the permissions for the destination folder.Exiting!!Error No -%s. "
               "Error-%s." % (errno, strerror)))
        os.rmdir(destFolder)
        sys.exit(1)

    print("\nThe deposition was successful. The trajid for the deposition is :%s." % trajId)
