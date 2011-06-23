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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.    See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Archivematica.    If not, see <http://www.gnu.org/licenses/>.

# @package Archivematica
# @subpackage transfer
# @author Joseph Perry <joseph@artefactual.com>
# @version svn: $Id$

#Related Docs
# http://pyinotify.sourceforge.net/doc-v07/index.html

#Variables to move to config file


#imports
import pyinotify
import uuid
import MySQLdb
import _mysql
import sys
import os
sys.path.append("/usr/lib/archivematica/MCPServer")
from MCPloggingSQL import getUTCDate
from MCPloggingSQL import runSQL
import MCPloggingSQL 

separator = "', '"

#Variables to move to config file
transferDirectory = '/var/archivematica/sharedDirectory/transfer/'

#Local Variables
mask = pyinotify.IN_CREATE | pyinotify.IN_MODIFY | pyinotify.IN_MOVED_FROM | pyinotify.IN_MOVED_TO | pyinotify.IN_DELETE | pyinotify.IN_CLOSE_WRITE
movedFrom = {} #cookie, current location


def remove_file(filePath):
    global separator
    utcDate = getUTCDate()
    filesWithMatchingPath = []
    
    #Find the file pk/UUID
    c=MCPloggingSQL.database.cursor()
    sql = """SELECT fileUUID FROM Files WHERE removedTime = 0 AND Files.currentLocation = '""" + _mysql.escape_string(filePath) + """';"""
    c.execute(sql)
    row = c.fetchone()
    while row != None:
        filesWithMatchingPath.append(row[0])
        row = c.fetchone()
        
    #Update the database
    for file in filesWithMatchingPath: 
        eventIdentifierUUID = uuid.uuid4().__str__()
        eventType = "file removed"
        eventDateTime = utcDate
        eventDetail = ""
        eventOutcomeDetailNote = "removed from: " + filePath

        runSQL("""INSERT INTO Events (fileUUID, eventIdentifierUUID, eventType, eventDateTime, eventDetail, eventOutcomeDetailNote)
                VALUES ( '"""   + file + separator \
                                + eventIdentifierUUID + separator \
                                + _mysql.escape_string(eventType) + separator \
                                + _mysql.escape_string(eventDateTime) + separator \
                                + _mysql.escape_string(eventDetail) + separator \
                                + _mysql.escape_string(eventOutcomeDetailNote) + "' )" )
        
    
        runSQL("UPDATE Files " + \
           "SET removedTime='" + utcDate + "', currentLocation=NULL " + \
           "WHERE fileUUID='" + file + "'" )
              
class transferNotifier(pyinotify.ProcessEvent):
    def __init__(self):
        self.IN_CREATE_COUNT = 0 
        self.IN_MODIFY_COUNT = 0 
        self.IN_MOVED_FROM_COUNT = 0 
        self.IN_MOVED_TO_COUNT = 0 
        self.IN_DELETE_COUNT = 0 
        self.IN_CLOSE_WRITE_COUNT = 0
    
    def process_IN_CREATE(self, event):
        #Do nothing
        print event
        self.IN_CREATE_COUNT += 1
        print self.IN_CREATE_COUNT 
        
    def process_IN_MODIFY(self, event):
        print event
        self.IN_MODIFY_COUNT += 1
        print self.IN_MODIFY_COUNT
        print "File was modified, but is still open."
        #if it exists in the db
            #log the new checksum
        #else
            #ignore
        
    def process_IN_MOVED_FROM(self, event):
        print event
        self.IN_MOVED_FROM_COUNT += 1
        print self.IN_MOVED_FROM_COUNT
        #Wait for a moved to, and if one doesn't occur, consider it moved outside of the system.
        
    def process_IN_MOVED_TO(self, event):
        print event
        self.IN_MOVED_TO_COUNT += 1
        print self.IN_MOVED_TO_COUNT
        
        
    def process_IN_DELETE(self, event):
        print event
        self.IN_DELETE_COUNT += 1
        print self.IN_DELETE_COUNT
        print "file was removed"
        fileName = os.path.join(event.path, event.name).replace(transferDirectory, "transfer/")
        remove_file(fileName)
        
    def process_IN_CLOSE_WRITE(self, event):
        global separator
        print event
        self.IN_CLOSE_WRITE_COUNT += 1
        print self.IN_CLOSE_WRITE_COUNT
        print "File was closed, and may be modified."
        
        fileName = os.path.join(event.path, event.name).replace(transferDirectory, "transfer/")
        fileUUID = ""
        
        if False: #file in db  
            print "TODO"
        else:
            #Create new file
            fileUUID = uuid.uuid4().__str__() 
            runSQL("""INSERT INTO Files (fileUUID, originalLoacation, currentLocation, enteredSystem)
                VALUES ( '"""   + fileUUID + separator \
                                + MySQLdb.escape_string(fileName) + separator \
                                + _mysql.escape_string(fileName) + separator \
                                + getUTCDate() + "' )" )
        print "TODO"
        #log the new checksum

def startWatching():
    wm = pyinotify.WatchManager()
    notifier = pyinotify.Notifier(wm, transferNotifier())
    wm.add_watch(transferDirectory, mask, rec=True, auto_add=True)
    #notifier.start()
    notifier.loop()

def loadExistingFiles():
    a=1

if __name__ == '__main__':
    loadExistingFiles()
    startWatching()