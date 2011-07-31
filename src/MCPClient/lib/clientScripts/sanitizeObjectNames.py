#!/usr/bin/python

# This file is part of Archivematica.
#
# Copyright 2010-2011 Artefactual Systems Inc. <http://artefactual.com>
#
# Archivematica is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# Archivematica is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Archivematica.  If not, see <http://www.gnu.org/licenses/>.

# @package Archivematica
# @subpackage Ingest
# @author Joseph Perry <joseph@artefactual.com>
# @version svn: $Id$
import sys
import shlex
import subprocess
import os
import MySQLdb
import uuid
sys.path.append("/usr/lib/archivematica/archivematicaCommon")
import databaseInterface
from databaseFunctions import insertIntoEvents


#import lxml.etree as etree
def updateFileLocation(src, dst, eventType, eventDateTime, eventDetail, eventIdentifierUUID = uuid.uuid4().__str__(), fileUUID="None", sipUUID="None"):
    """If the file uuid is not provided, will use the sip uuid and old path to find the file uuid"""
    
    if not fileUUID:
        sql = "SELECT Files.fileUUID FROM Files WHERE Files.currentLocation = '" + MySQLdb.escape_string(src) + "' AND Files.sipUUID = '" + sipUUID + "';"  
        c, sqlLock = databaseInterface.querySQL(sql) 
        row = c.fetchone()
        while row != None:
            print row
            fileUUID = row[0] 
            row = c.fetchone()
        sqlLock.release()
        
    eventOutcomeDetailNote = "Original name=\"" + src + "\"; cleaned up name=\"" + dst + "\""
    eventOutcomeDetailNote = eventOutcomeDetailNote.decode('utf-8')
    
    #CREATE THE EVENT
    if not fileUUID:
        print >>sys.stderr, "Unable to find file uuid for: ", src, " -> ", dst
        exit(6)
    insertIntoEvents(fileUUID=fileUUID, eventIdentifierUUID=eventIdentifierUUID, eventType=eventType, eventDateTime=eventDateTime, eventDetail="", eventOutcome="", eventOutcomeDetailNote=eventOutcomeDetailNote)
        
    #UPDATE THE CURRENT FILE PATH
    sql =  """UPDATE Files SET currentLocation='""" + dst + """' WHERE fileUUID='""" + fileUUID + """';"""
    databaseInterface.runSQL(sql)

 
       
if __name__ == '__main__':
    objectsDirectory = sys.argv[1]
    sipUUID =  sys.argv[2]
    date = sys.argv[3]
    taskUUID = sys.argv[4]

    #def executeCommand(taskUUID, requiresOutputLock = "no", sInput = "", sOutput = "", sError = "", execute = "", arguments = "", serverConnection = None):
    command = "sanitizeNames \"" + objectsDirectory + "\""
    lines = []
    commandVersion = "sanitizeNames -V"
    version = ""
    try:
        p = subprocess.Popen(shlex.split(command), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        #p.wait()
        output = p.communicate()
        retcode = p.returncode
        
        #print output

        #it executes check for errors
        if retcode != 0:
            print >>sys.stderr, "error code:" + retcode.__str__()
            print output[1]# sError
            quit(retcode)
        lines = output[0].split("\n")
        
        #GET VERSION
        p = subprocess.Popen(shlex.split(commandVersion), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
        #p.wait()
        output = p.communicate()
        retcode = p.returncode
        
        #it executes check for errors
        if retcode != 0:
            print >>sys.stderr, "Error getting version; error code:" + retcode.__str__()
            print output[1]# sError
            quit(retcode)
        version = output[0].replace("\n", "")
    except OSError, ose:
        print >>sys.stderr, "Execution failed:", ose
        quit(2)

    eventDetailText= "program=\"sanitizeNames\"; version=\"" + version + "\""
    for line in lines:
        detoxfiles = line.split(" -> ")
        if len(detoxfiles) > 1 :
            oldfile = detoxfiles[0].split('\n',1)[0]
            newfile = detoxfiles[1]
            #print "line: ", line
            if os.path.isfile(newfile):
                oldfile = oldfile.replace(objectsDirectory, "%SIPDirectory%objects/", 1)
                newfile = newfile.replace(objectsDirectory, "%SIPDirectory%objects/", 1)
                print oldfile, " -> ", newfile 

                updateFileLocation(oldfile, newfile, "name cleanup", date, "prohibited characters removed", fileUUID=None, sipUUID=sipUUID)
                
            elif os.path.isdir(newfile):
                oldfile = oldfile.replace(objectsDirectory, "%SIPDirectory%objects/", 1) + "/"
                newfile = newfile.replace(objectsDirectory, "%SIPDirectory%objects/", 1) + "/"
                directoryContents = []
                
                sql = "SELECT * FROM Files WHERE Files.currentLocation LIKE '" + MySQLdb.escape_string(oldfile).replace("%","\%") + "%' AND Files.sipUUID = '" + sipUUID + "';"
                 
                c, sqlLock = databaseInterface.querySQL(sql) 
                row = c.fetchone()
                while row != None:
                    print row
                    fileUUID = row[0] 
                    oldPath = row[1]
                    newPath = oldPath.replace(oldfile, newfile, 1)
                    directoryContents.append((fileUUID, oldPath, newPath))
                    row = c.fetchone()
                sqlLock.release()

                print oldfile, " -> ", newfile

                for fileUUID, oldPath, newPath in directoryContents:
                    updateFileLocation(oldPath, newPath, "name cleanup", date, "prohibited characters removed", fileUUID=fileUUID)
                    


