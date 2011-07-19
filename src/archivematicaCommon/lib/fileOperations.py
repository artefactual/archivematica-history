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
# @subpackage transcoder
# @author Joseph Perry <joseph@artefactual.com>
# @version svn: $Id$

import os
import databaseInterface

#Used to write to file
#@output - the text to append to the file
#@fileName - The name of the file to create, or append to.
#@returns - 0 if ok, non zero if error occured.
def writeToFile(output, fileName):
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
    eventOutcomeDetailNote = checksum.__str__()

    databaseInterface.insertIntoEvents(fileUUID, eventIdentifierUUID, eventType, eventDateTime, eventDetail, eventOutcomeDetailNote)

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

        databaseInterface.insertIntoEvents(fileUUID, eventIdentifierUUID, eventType, eventDateTime, eventDetail, eventOutcomeDetailNote)
        
    
        databaseInterface.runSQL("UPDATE Files " + \
           "SET removedTime='" + utcDate + "', currentLocation=NULL " + \
           "WHERE fileUUID='" + file + "'" )
        