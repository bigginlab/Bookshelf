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

    updated and refactored December 2020 by Philip Biggin

"""
try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass

import MySQLdb
import shutil
import hashlib
import os
import sys
import datetime
from mysql_connect import _mysql_connect_

homeDir = "defaultpath"
tempFolder = homeDir + "bookshelf/temp/"  # PATH may have to be set .Store files temporarily
trajFolder = homeDir + "bookshelf/data/trajfiles/"  # PATH may have to be set .Folder where the files will be stored
junkFolder = homeDir + "bookshelf/data/error_trajfiles/"  # PATH may have to be set .store folders if not deposited


def _remove_folder_(dirs):  # delete folder after they have been copied to the trajfiles folder
    deleteFolder = tempFolder + dirs
    try:
        shutil.rmtree(deleteFolder)
    except OSError as xxx_todo_changeme3:
        (errno, strerror) = xxx_todo_changeme3.args
        sys.stderr.write("\n Error deleting the folder from temp directory"
                         "%s Error no: %s Error- %s." % (dirs, errno, strerror))
        sys.exit(1)


def _move_folder_(dirs):  # move folder to junkFolder if deposition is not successful
    removeFolder = junkFolder + dirs
    copyFolder = tempFolder + dirs
    try:
        shutil.copytree(copyFolder, removeFolder)
        os.system('chmod -R 755 %s' % removeFolder)
    except OSError as xxx_todo_changeme4:
        (errno, strerror) = xxx_todo_changeme4.args
        sys.stderr.write("\nError copying %s directroy to "
                         "error_trajFiles folder-%s, Error-%s." % (dirs, errno, strerror))
        sys.exit(1)
    if os.path.isdir(trajFolder + dirs):
        try:
            shutil.rmtree(trajFolder + dirs)
        except OSError as xxx_todo_changeme2:
            (errno, strerror) = xxx_todo_changeme2.args
            sys.stderr.write("\n Error deleting the folder from trajFiles "
                             "-%s Error no: %s Error- %s." % (dirs, errno, strerror))
            sys.exit(1)


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
        flag = 1
    except FileName.DoesNotExist:
        sys.stderr.write('\n "There was a problem with md5sum for file %s!!! "' % FileName)
        flag = 2
    return checksum, flag


def calculateSize(folderName):  # to calculate the size of the folder for PMF deposition
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folderName):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
        return total_size


def _daemon_process_():  # Daemon that copies the folder form temp folder to the permanent folder
    RemoveElements = []
    dir_List = os.listdir(tempFolder)  # list all the dirs in the tempfolder to be copied
    dir_List.sort()
    for dirs in dir_List:
        flag = 0
        copyFolder = tempFolder + dirs
        destFolder = trajFolder + dirs
        conn = _mysql_connect_()
        cursor = conn.cursor()
        if os.path.isfile(tempFolder + dirs + "/%s.metadata" % dirs):  # check if metadata file exists
            try:
                inputFileOne = open(tempFolder + dirs + "/%s.metadata" % dirs, 'r')  # read metadata file
                fileContent = inputFileOne.readlines()
            except OSError as xxx_todo_changeme1:
                (errno, strerror) = xxx_todo_changeme1.args
                sys.stderr.write("\nError opening or reading the %s metadata file-%s, "
                                 "Error-%s." % (dirs, errno, strerror))
                RemoveElements.append(dirs)
                continue
            inputFileOne.close()
            for lines in fileContent:
                lines = lines.strip()
                temp_List = lines.split("\t")
                if temp_List[0] == 'flag':  # to see if the flag is set true or false
                    if temp_List[1].strip() == "flagTrue":
                        flag = 1
                    elif temp_List[1].strip() == "flagFalse":
                        RemoveElements.append(dirs)
                        sys.stderr.write("\nError !!There was problem with the deposition for TrajId -%s. Flag was "
                                         "set to False. You can check the metadata file for details. " % dirs)
                        continue

            if flag == 1:
                sys.stderr.write("\n####TrajId for the deposition is %s ####" % dirs)
                sys.stderr.write("\n" + str(datetime.datetime.now()) + "\n")
                # this block is executed only if the flag is set flagtrue
                file_list = {}
                for lines in fileContent:
                    lines = lines.strip()
                    temp_List = lines.split("\t")
                    if temp_List[0].strip() == 'USERNAME':
                        userName = temp_List[1].strip()
                    elif temp_List[0].strip() == 'SYSTEMDATE':
                        systemDate = temp_List[1].strip()
                    elif temp_List[0].strip() == 'MOLNAME':
                        molName = temp_List[1].strip()
                    elif temp_List[0].strip() == 'PROGNAME':
                        progName = temp_List[1].strip()
                    elif temp_List[0].strip() == 'USERCOMMENTS':
                        userComments = temp_List[1].strip()
                    elif temp_List[0].strip() == 'TRAJID':
                        trajId = temp_List[1].strip()
                    elif temp_List[0].strip() == 'PMFFLAG':
                        pmfFlag = temp_List[1].strip()
                    elif temp_List[0].strip() == 'DOI':
                        doi = temp_List[1].strip()
                    elif temp_List[0].strip() == 'PID':
                        pid = temp_List[1].strip()
                    elif temp_List[0].strip() == 'flag':
                        pass
                    elif temp_List[0].strip() == 'sizeError':
                        pass
                    else:
                        file_list[temp_List[0]] = temp_List[1]

                if trajId != dirs:
                    sys.stderr.write("\nError! Mismatch in trajId and the directory name for %s." % dirs)
                    RemoveElements.append(dirs)
                    continue

                try:  # copy the traj folder from temp to permanent folder and change permissions to read
                    shutil.copytree(copyFolder, destFolder)
                    os.system('chmod -R 755 %s' % destFolder)
                except OSError as xxx_todo_changeme:
                    (errno, strerror) = xxx_todo_changeme.args
                    sys.stderr.write("\nError copying %s to destination folder or changing permission for "
                                     "TrajId-%s, Error-%s." % (dirs, errno, strerror))
                    RemoveElements.append(dirs)
                    continue

                if pmfFlag == 'No':
                    errcount = 0
                    TrajFilesRows = 0
                    for trajFiles, checkSum in list(file_list.items()):  # see if folders have been copied correctly
                        newFile = "%s/%s" % (destFolder, trajFiles)
                        newCheckSum, flag = _md5Check_(newFile)
                        if flag == 2:
                            errcount += 1
                        if newCheckSum != checkSum:
                            sys.stderr.write("\nError copying %s files for trajid %s. Checksum varies!!! \n "
                                             "Original checksum=%s New checksum=%s"
                                             % (trajFiles, dirs, checkSum, newCheckSum)
                                             )
                            errcount += 1
                    try:  # entry into TrajData
                        cursor.execute(
                            'INSERT INTO TrajData VALUES("%s","%s","%s","%s","%s","%s","%s","%s","%s")'
                            % (trajId, userName, systemDate, molName, progName, userComments, pmfFlag, doi, pid)
                        )
                    except (MySQLdb.ProgrammingError, MySQLdb.OperationalError) as error:
                        sys.stderr.write("\nDatabase error for TrajId %s "
                                         "Error-%d: %s" % (dirs, error.args[0], error.args[1]))
                        errcount += 1
                        continue
                    TrajdataRow = cursor.rowcount

                    for trajFiles, checkSum in list(file_list.items()):  # entry into TrajFiles
                        try:
                            cursor.execute('INSERT into TrajFiles(FileName, UserName, CheckSum,'
                                           'TrajId, FilePathName, Date) VALUES( %s, %s, %s, %s, %s, %s)',
                                           (trajFiles, userName, checkSum, trajId, destFolder, systemDate))
                        except (MySQLdb.ProgrammingError, MySQLdb.OperationalError) as error:
                            sys.stderr.write("\nDatabase error for file %s for TrajId %s Error %d: %s"
                                             % (trajFiles, dirs, error.args[0], error.args[1]))
                            errcount += 1
                        TrajFilesRows += cursor.rowcount

                elif pmfFlag == 'Yes':  # PMF deposition
                    errcount = 0
                    TrajFilesRows = 0
                    fileListKeys = list(file_list.keys())
                    dirName = str(fileListKeys[0])
                    destFileName = destFolder + "/" + dirName
                    fileListvalues = list(file_list.values())
                    dir_size = int(fileListvalues[0])
                    new_dir_size = calculateSize(destFileName)  # check this
                    diff = abs(new_dir_size - dir_size)
                    if diff > 0:
                        sys.stderr.write("\nError copying the \"%s\" folder. File size varies!!! \n Original "
                                         "size =%s New size=%s." % (dirName, dir_size, new_dir_size))
                        errcount += 1

                    try:  # entry into TrajData
                        cursor.execute(
                            'INSERT INTO TrajData VALUES("%s","%s","%s","%s","%s","%s","%s","%s","%s")'
                            % (trajId, userName, systemDate, molName, progName, userComments, pmfFlag, doi, pid)
                        )
                    except (MySQLdb.ProgrammingError, MySQLdb.OperationalError) as error:
                        sys.stderr.write("\nDatabase error for trajid -%s.Error %d: %s."
                                         % (dirName, error.args[0], error.args[1]))
                        errcount += 1
                        continue
                    TrajdataRow = cursor.rowcount

                    try:  # entry into TrajFiles
                        cursor.execute('INSERT into TrajFiles(FileName, UserName, CheckSum, TrajId, '
                                       'FilePathName, Date) VALUES(%s, %s, %s, %s, %s, %s)', (dirName, userName,
                                                                                              new_dir_size, trajId,
                                                                                              destFolder, systemDate)
                                       )
                    except (MySQLdb.ProgrammingError, MySQLdb.OperationalError) as error:
                        sys.stderr.write("\nDatabase error for trajid -%s in Files "
                                         "database.Error %d: %s." % (dirName, error.args[0], error.args[1]))
                        errcount += 1
                        continue
                    TrajFilesRows += cursor.rowcount
                if errcount > 0:  # if error while copying add directory into removal list
                    RemoveElements.append(dirs)
                    continue
                else:
                    sys.stderr.write("\nNumber of entries in the trajectory database "
                                     "for %s: %d." % (trajId, TrajdataRow))
                    sys.stderr.write("\nNumber of entries in the trajectory files database "
                                     "for %s: %d." % (trajId, TrajFilesRows))
                conn.commit()

            if flag == 1:
                sys.stderr.write("\n" + str(datetime.datetime.now()))
                sys.stderr.write("\n#### The deposition was sucessfully done by %s. TrajId for "
                                 "deposition -%s ####\n" % (userName, trajId))
                _remove_folder_(dirs)  # deleting the directory after it has been succesfully copied
        else:
            continue
        cursor.close()
        conn.close()

    for dirs in RemoveElements:
        conn = _mysql_connect_()
        cursor = conn.cursor()
        _move_folder_(dirs)
        _remove_folder_(dirs)
        sys.stderr.write("\n #### The deposition was not successful.Folder has been moved to removeFolder TrajId "
                         "for deposition -%s ####\n" % dirs)
        try:
            cursor.execute("delete from TrajFiles where TrajId = '%s'" % dirs)  # delete entry from the database
            sys.stderr.write('\nNumber of files deleted in TrajFiles database: "%d"' % cursor.rowcount)
            cursor.execute("delete from TrajData where TrajId = '%s'" % dirs)  # delete entry from the database
            sys.stderr.write('\nNumber of files deleted in TrajData database: "%d"' % cursor.rowcount)
        except OSError as e:
            sys.stderr.write("Error deleting entries from database-%s [%d]" % (e.strerror, e.errno))
            continue
        cursor.close()
        conn.close()


#  DAEMON #

def _daemonize_(stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
    # perform first fork
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)  # Exit first parent
    except OSError as e:
        sys.stdout.write("\nFork 1 failed: (%d) %s\n" % (e.errno, e.strerror))
        sys.exit(1)
    # Decouple from parent environment
    os.chdir("/")
    os.umask(0)
    os.setsid()
    # Perform second fork
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)  # Exit first parent
    except OSError as e:
        sys.stdout.write("\nFork 2 failed: (%d) %s\n" % (e.errno, e.strerror))
        sys.exit(1)
    # The process is now daemonized, redirect standard file descriptors
    # In code snippets open is sometimes file - I think that is incorrect (PCB 2020)
    for f in sys.stdout, sys.stderr:
        f.flush()
        si = open(stdin, 'r')
        so = open(stdout, 'a+')
        se = open(stderr, 'a+', 0)
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())


def _main_():
    import time
    PID = os.getpid()
    sys.stdout.write("\nDaemon started with pid %d\n" % PID)
    sys.stdout.write("\nDaemon stdout output\n")
    sys.stderr.write("\nDaemon started with pid %d\n" % PID)
    sys.stderr.write("\nDaemon stderr output\n")
    c = 0
    while True:
        sys.stdout.write('%d: %s\n' % (c, time.ctime()))
        sys.stdout.flush()
        c = c + 1
        _daemon_process_()
        time.sleep(5)


if __name__ == "__main__":
    # path may have to be set .Store logs
    _daemonize_('/dev/null', homeDir + "exe/logs/daemon.log", homeDir + "exe/logs/error.log")
    _main_()
