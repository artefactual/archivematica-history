#!/usr/bin/python -OO
# This file is part of Archivematica.
#
# Copyright 2010-2011 Artefactual Systems Inc. <http://artefactual.com>
#
# Archivematica is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
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
# @subpackage transcoder
# @author Joseph Perry <joseph@artefactual.com>
# @version svn: $Id$

import os
import uuid
import sys
import databaseInterface
from databaseFunctions import insertIntoFiles
from executeOrRunSubProcess import executeOrRun
from externals.checksummingTools import sha_for_file
from databaseFunctions import insertIntoEvents
import MySQLdb


def updateSizeAndChecksum(fileUUID, filePath, date, eventIdentifierUUID):   
    fileSize = os.path.getsize(filePath).__str__()
    checksum = sha_for_file(filePath).__str__()
    
    sql = "UPDATE Files " + \
        "SET fileSize='" + fileSize +"', checksum='" + checksum +  "' " + \
        "WHERE fileUUID='" + fileUUID + "'"
    databaseInterface.runSQL(sql)

    insertIntoEvents(fileUUID=fileUUID, \
                     eventIdentifierUUID=eventIdentifierUUID, \
                     eventType="message digest calculation", \
                     eventDateTime=date, \
                     eventDetail="program=\"python\"; module=\"hashlib.sha256()\"", \
                     eventOutcomeDetailNote=checksum)  


def addFileToTransfer(filePathRelativeToSIP, fileUUID, transferUUID, taskUUID, date, sourceType="ingestion", eventDetail="", use="original"):
    insertIntoFiles(fileUUID, filePathRelativeToSIP, date, transferUUID=transferUUID, use=use)
    insertIntoEvents(fileUUID=fileUUID, \
                   eventIdentifierUUID=taskUUID, \
                   eventType=sourceType, \
                   eventDateTime=date, \
                   eventDetail=eventDetail, \
                   eventOutcome="", \
                   eventOutcomeDetailNote="")

def addFileToSIP(filePathRelativeToSIP, fileUUID, sipUUID, taskUUID, date, sourceType="ingestion", use="original"):
    insertIntoFiles(fileUUID, filePathRelativeToSIP, date, sipUUID=sipUUID, use=use)
    insertIntoEvents(fileUUID=fileUUID, \
                   eventIdentifierUUID=taskUUID, \
                   eventType=sourceType, \
                   eventDateTime=date, \
                   eventDetail="", \
                   eventOutcome="", \
                   eventOutcomeDetailNote="")

#Used to write to file
#@output - the text to append to the file
#@fileName - The name of the file to create, or append to.
#@returns - 0 if ok, non zero if error occured.
def writeToFile(output, fileName, writeWhite=False):
    if not writeWhite and output.isspace():
        return 0
    if fileName and output:
        print "writing to: " + fileName
        if fileName.startswith("<^Not allowed to write to file^> "):
            return -1
        try:
            f = open(fileName, 'a')
            f.write(output.__str__())
            f.close()
            os.chmod(fileName, 488)
        except OSError, ose:
            print >>sys.stderr, "output Error", ose
            return -2
        except IOError as (errno, strerror):
            print "I/O error({0}): {1}".format(errno, strerror)
            return -3
    else:
        print "No output, or file specified"
    return 0

def checksumFile(filePath, fileUUID):
    global transferDirectory
    truePath = filePath.replace("transfer/", transferDirectory, 1)
    checksum = sha_for_file(truePath)
    utcDate = databaseInterface.getUTCDate()
    
    #Create Event
    eventIdentifierUUID = uuid.uuid4().__str__()
    eventType = "message digest calculation"
    eventDateTime = utcDate
    eventDetail = 'program="python"; module="hashlib.sha256()" ; file="/usr/lib/python2.6/hashlib.pyc"'
    eventOutcome = ""
    eventOutcomeDetailNote = checksum.__str__()

    databaseInterface.insertIntoEvents(fileUUID=fileUUID, \
                                       eventIdentifierUUID=eventIdentifierUUID, \
                                       eventType=eventType, \
                                       eventDateTime=eventDateTime, \
                                       eventDetail=eventDetail, \
                                       eventOutcome=eventOutcome, \
                                       eventOutcomeDetailNote=eventOutcomeDetailNote)


def removeFile(filePath, utcDate = databaseInterface.getUTCDate()):
    global separator
    print "removing: ", filePath
    filesWithMatchingPath = []
    
    sqlLoggingLock.acquire()
    #Find the file pk/UUID
    c=MCPloggingSQL.database.cursor()
    sql = """SELECT fileUUID FROM Files WHERE removedTime = 0 AND Files.currentLocation = '""" + MySQLdb.escape_string(filePath) + """';"""
    c.execute(sql)
    row = c.fetchone()
    while row != None:
        filesWithMatchingPath.append(row[0])
        row = c.fetchone()
    sqlLoggingLock.release()
    #Update the database
    for file in filesWithMatchingPath: 
        eventIdentifierUUID = uuid.uuid4().__str__()
        eventType = "file removed"
        eventDateTime = utcDate
        eventDetail = ""
        eventOutcomeDetailNote = "removed from: " + filePath

        databaseInterface.insertIntoEvents(fileUUID=fileUUID, \
                                       eventIdentifierUUID=eventIdentifierUUID, \
                                       eventType=eventType, \
                                       eventDateTime=eventDateTime, \
                                       eventDetail=eventDetail, \
                                       eventOutcome=eventOutcome, \
                                       eventOutcomeDetailNote=eventOutcomeDetailNote)
        
    
        databaseInterface.runSQL("UPDATE Files " + \
           "SET removedTime='" + utcDate + "', currentLocation=NULL " + \
           "WHERE fileUUID='" + file + "'" )
        
def renameAsSudo(source, destination):
    """Used to move/rename Directories that the archivematica user may or may not have writes to move"""
    command = "sudo mv \"" + source + "\"   \"" + destination + "\""
    exitCode, stdOut, stdError = executeOrRun("command", command, "", printing=False)
    if exitCode:
        print stdOut
        print >>sys.stderr, stdError
        exit(exitCode)

#import lxml.etree as etree
def updateFileLocation(src, dst, eventType, eventDateTime, eventDetail, eventIdentifierUUID = uuid.uuid4().__str__(), fileUUID="None", sipUUID = None, transferUUID=None, eventOutcomeDetailNote = ""):
    """If the file uuid is not provided, will use the sip uuid and old path to find the file uuid"""
    
    if not fileUUID or fileUUID == "None":
        sql = "Need to define transferUUID or sipUUID"
        if sipUUID:
            sql = "SELECT Files.fileUUID FROM Files WHERE removedTime = 0 AND Files.currentLocation = '" + MySQLdb.escape_string(src) + "' AND Files.sipUUID = '" + sipUUID + "';"
        elif transferUUID:
            sql = "SELECT Files.fileUUID FROM Files WHERE removedTime = 0 AND Files.currentLocation = '" + MySQLdb.escape_string(src) + "' AND Files.transferUUID = '" + transferUUID + "';"  
        c, sqlLock = databaseInterface.querySQL(sql) 
        row = c.fetchone()
        while row != None:
            print row
            fileUUID = row[0] 
            row = c.fetchone()
        sqlLock.release()
    
    if eventOutcomeDetailNote == "":
        eventOutcomeDetailNote = "Original name=\"" + src + "\"; cleaned up name=\"" + dst + "\""
        #eventOutcomeDetailNote = eventOutcomeDetailNote.decode('utf-8')
    
    #CREATE THE EVENT
    if not fileUUID:
        print >>sys.stderr, "Unable to find file uuid for: ", src, " -> ", dst
        exit(6)
    insertIntoEvents(fileUUID=fileUUID, eventIdentifierUUID=eventIdentifierUUID, eventType=eventType, eventDateTime=eventDateTime, eventDetail=eventDetail, eventOutcome="", eventOutcomeDetailNote=eventOutcomeDetailNote)
        
    #UPDATE THE CURRENT FILE PATH
    sql =  """UPDATE Files SET currentLocation='""" + dst + """' WHERE fileUUID='""" + fileUUID + """';"""
    databaseInterface.runSQL(sql)
        