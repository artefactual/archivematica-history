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
# http://code.google.com/p/archivematica/source/browse/trunk/src/transfer/lib/transferD.py?r=1656

#Variables to move to config file


#imports
import pyinotify
import uuid
import MySQLdb
import sys
import os
import copy
import threading
import time

import archivematicaMCP
from unitTransfer import unitTransfer
from unitSIP import unitSIP

completedTransfersDirectory = "/var/archivematica/sharedDirectory/watchedDirectories/preIngest/SIPCreation/completedTransfers/"
sipCreationDirectory = "/var/archivematica/sharedDirectory/watchedDirectories/preIngest/SIPCreation/SIPsUnderConstruction/"


sys.path.append("/usr/lib/archivematica/archivematicaCommon")
import databaseInterface
a = """
from fileOperations import checksumFile
from fileOperations import removeFile


sys.path.append("/usr/lib/archivematica/MCPServer")
from MCPloggingSQL import getUTCDate
from MCPloggingSQL import runSQL
from MCPloggingSQL import sqlLoggingLock
import MCPloggingSQL 

sys.path.append("/usr/lib/archivematica/MCPClient/clientScripts")
from fileAddedToSIP import sha_for_file
"""

#Variables to move to config file
transferDirectory = '/var/archivematica/sharedDirectory/transfer/'
delayTimer = 4
waitToActOnMoves = 1

#Local Variables
mask = pyinotify.IN_CREATE | pyinotify.IN_MODIFY | pyinotify.IN_MOVED_FROM | pyinotify.IN_MOVED_TO | pyinotify.IN_DELETE | pyinotify.IN_CLOSE_WRITE
separator = "', '"
movedFrom = {} #cookie, current location
movedFromLock = threading.Lock()

def timerExpired(event, utcDate):
    global transferDirectory
    
    movedFromLock.acquire()
    truePath = os.path.join(event.path, event.name)
    filePath = truePath.replace(transferDirectory, "transfer/", 1)
    if event.cookie in movedFrom:
        #remove it from the list of unfound moves
        fevent = movedFrom.pop(event.cookie)
        movedFromLock.release()
        if event.dir:
            #recursively remove directory
            filesWithMatchingPath = []
            sqlLoggingLock.acquire()
            #Find the file pk/UUID
            c=MCPloggingSQL.database.cursor()
            sql = """SELECT Files.currentLocation FROM Files WHERE removedTime = 0 AND Files.currentLocation LIKE '""" + MySQLdb.escape_string(filePath + "/") + """%';"""
            c.execute(sql)
            row = c.fetchone()
            while row != None:
                filesWithMatchingPath.append(row[0])
                row = c.fetchone()
            sqlLoggingLock.release()
            #Update the database
            for file in filesWithMatchingPath:
                updateDBFileWasRemoved(file, utcDate)
        else:
            updateDBFileWasRemoved(filePath, utcDate)        
    else: #was moved internally
        movedFromLock.release()

a = """
              
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
        
        truePath = os.path.join(event.path, event.name)
        filePath = truePath.replace(transferDirectory, "transfer/", 1)
        
        #if it's a directory
        if os.path.isdir(truePath):
            for file in os.listdir(truePath):
                if os.path.isfile(os.path.join(truePath, file)):
                    fileEvent = copy.deepcopy(event)
                    fileEvent.path = truePath
                    fileEvent.name = file
                    self.process_IN_CLOSE_WRITE(fileEvent)
        
    def process_IN_MODIFY(self, event):
        print event
        self.IN_MODIFY_COUNT += 1
        print self.IN_MODIFY_COUNT
        print "File was modified, but is still open."
        
        filePath = os.path.join(event.path, event.name).replace(transferDirectory, "transfer/", 1)
        fileUUID = ""
        filesToChecksum = []
        sqlLoggingLock.acquire()
        c=MCPloggingSQL.database.cursor()
        sql = "SELECT fileUUID FROM Files WHERE removedTime = 0 AND Files.currentLocation = '" + MySQLdb.escape_string(filePath) + "';"
        c.execute(sql)
        row = c.fetchone()
        while row != None:
            fileUUID = row[0]
            filesToChecksum.append(row[0])
            row = c.fetchone()
        sqlLoggingLock.release()
        
        for file in filesToChecksum:
            checksumFile(filePath, file)
        #else
            #ignore
        
    def process_IN_MOVED_FROM(self, event):
        print event
        self.IN_MOVED_FROM_COUNT += 1
        print self.IN_MOVED_FROM_COUNT
        #Wait for a moved to, and if one doesn't occur, consider it moved outside of the system.
        movedFromLock.acquire()
        movedFrom[event.cookie] = event
        movedFromLock.release()
        utcDate = getUTCDate()
        
        movedFromLock.acquire()
        
        
        #create timer to check if it's claimed by a move to
        self.timer = threading.Timer(delayTimer, timerExpired, args=[event, utcDate], kwargs={})
        self.timer.start()
        
        
    def process_IN_MOVED_TO(self, event):
        print event
        self.IN_MOVED_TO_COUNT += 1
        print self.IN_MOVED_TO_COUNT
        movedFromLock.acquire()
        if event.cookie in movedFrom:
            #remove it from the list of unfound moves
            fevent = movedFrom.pop(event.cookie)
            movedFromLock.release()
            
            truePath = os.path.join(event.path, event.name)
            filePath = truePath.replace(transferDirectory, "transfer/", 1)
            fFilePath =  os.path.join(fevent.path, fevent.name).replace(transferDirectory, "transfer/", 1)
            filesWithMatchingPath = []
            
            #Find the file pk/UUID
            
            c=MCPloggingSQL.database.cursor()
            utcDate = getUTCDate()
            #if it's a file
            sqlLoggingLock.acquire()
            if os.path.isfile(truePath):
                sql = "SELECT fileUUID, currentLocation FROM Files WHERE removedTime = 0 AND Files.currentLocation = '" + MySQLdb.escape_string(fFilePath) + "';"
                c.execute(sql)
                row = c.fetchone()
                while row != None:
                    filesWithMatchingPath.append(row)
                    row = c.fetchone()
            elif os.path.isdir(truePath):
                sql = "SELECT fileUUID, currentLocation FROM Files WHERE removedTime = 0 AND Files.currentLocation LIKE '" + MySQLdb.escape_string(fFilePath + "/") + "%';"
                c.execute(sql)
                row = c.fetchone()
                while row != None:
                    filesWithMatchingPath.append(row)
                    row = c.fetchone()
            sqlLoggingLock.release()

            #Update the database
            for entry in filesWithMatchingPath:
                fileUUID, fromFilePath = entry
                newPath = fromFilePath.replace( fFilePath, filePath) 
                 #create the move event
                eventIdentifierUUID = uuid.uuid4().__str__()
                eventType = "file moved"
                eventDateTime = utcDate
                eventDetail = ""
                eventOutcomeDetailNote = "moveFrom=\"" + fromFilePath + "\" movedTo=\"" + newPath + "\""
        
                runSQL(""INSERT INTO Events (fileUUID, eventIdentifierUUID, eventType, eventDateTime, eventDetail, eventOutcomeDetailNote)
                        VALUES ( '""   + fileUUID + separator \
                                        + eventIdentifierUUID + separator \
                                        + MySQLdb.escape_string(eventType) + separator \
                                        + MySQLdb.escape_string(eventDateTime) + separator \
                                        + MySQLdb.escape_string(eventDetail) + separator \
                                        + MySQLdb.escape_string(eventOutcomeDetailNote) + "' )" )
                
                #update the current location
                runSQL("UPDATE Files " + \
                   "SET currentLocation='" + newPath + "' " + \
                   "WHERE fileUUID='" + fileUUID + "'" )    
                
               
                
                
        else:
            movedFromLock.release()
            self.process_IN_CLOSE_WRITE(event)
        
    def process_IN_DELETE(self, event):
        print event
        self.IN_DELETE_COUNT += 1
        print self.IN_DELETE_COUNT
        print "file was removed"
        filePath = os.path.join(event.path, event.name).replace(transferDirectory, "transfer/", 1)
        updateDBFileWasRemoved(filePath)
        
    def process_IN_CLOSE_WRITE(self, event):
        global separator
        print event
        self.IN_CLOSE_WRITE_COUNT += 1
        print self.IN_CLOSE_WRITE_COUNT
        print "File was closed, and may be modified."
        
        filePath = os.path.join(event.path, event.name).replace(transferDirectory, "transfer/", 1)
        fileUUID = ""
        
        sqlLoggingLock.acquire()
        c=MCPloggingSQL.database.cursor()
        sql = ""SELECT fileUUID FROM Files WHERE removedTime = 0 AND Files.currentLocation = '"" + MySQLdb.escape_string(filePath) + ""';""
        c.execute(sql)
        row = c.fetchone()
        sqlLoggingLock.release()

        if row == None:   
            #Create new file
            fileUUID = uuid.uuid4().__str__() 
            runSQL(""INSERT INTO Files (fileUUID, originalLoacation, currentLocation, enteredSystem)
                VALUES ( '""   + fileUUID + separator \
                                + MySQLdb.escape_string(filePath) + separator \
                                + MySQLdb.escape_string(filePath) + separator \
                                + getUTCDate() + "' )" )
        else:
            fileUUID = row[0]
        checksumFile(filePath,fileUUID)
"""


class SIPWatch(pyinotify.ProcessEvent):
    def __init__(self, unit):
        self.unit=unit
    #if a file is moved in, look for a cookie to claim
        #if there isn't one - error
        #error. No adding files to a sip in this manner.
    #else
        #Update the file to be linked to this SIP
    
    #if the SIP is moved/removed
        #???
    
    #if a file is moved in, look for a cookie to claim
    def process_IN_MOVED_TO(self, event):
        time.sleep(waitToActOnMoves)
        print event
        movedFromLock.acquire()
        if event.cookie not in movedFrom:
            #if there isn't one - error
            print event.cookie, movedFrom
            print >>sys.stderr, "#error. No adding files to a sip in this manner."
            movedFromLock.release()
            return
            
        #remove it from the list of unfound moves
        movedFromPath, filesMoved, timer = movedFrom.pop(event.cookie)
        movedFromLock.release()
              
        movedToPath = os.path.join(event.path, event.name).replace(\
                             self.unit.currentPath.replace("%sharedPath%", archivematicaMCP.config.get('MCPServer', "sharedDirectory"), 1), \
                             "%SIPDirectory%", 1)
        for fileUUID, oldLocation in filesMoved:
            newFilePath = oldLocation.replace(movedFromPath, movedToPath, 1) 
            print "Moved: ", oldLocation, "-> (" + self.unit.UUID + ")" + newFilePath
            databaseInterface.runSQL("UPDATE Files " + \
                "SET currentLocation='" + newFilePath +  "', " + \
                "Files.sipUUID = '" + self.unit.UUID + "' " \
                "WHERE fileUUID='" + fileUUID + "'" ) 
    
    def process_IN_MOVED_FROM(self, event):
        print event
        #Wait for a moved to, and if one doesn't occur, consider it moved outside of the system.
        
        movedFromPath = os.path.join(event.path, event.name).replace(\
                             self.unit.currentPath.replace("%sharedPath%", archivematicaMCP.config.get('MCPServer', "sharedDirectory"), 1), \
                             "%SIPDirectory%", 1)
        filesMoved = []
        sql = """SELECT fileUUID, currentLocation FROM Files WHERE sipUUID = '""" + self.unit.UUID + "' AND removedTime = 0 AND currentLocation LIKE '" + MySQLdb.escape_string(movedFromPath).replace("%", "%%") + "%';"
        c, sqlLock = databaseInterface.querySQL(sql) 
        row = c.fetchone()
        while row != None:
            print row
            filesMoved.append(row)            
            row = c.fetchone()
        sqlLock.release()
        
        movedFromLock.acquire()
        utcDate = databaseInterface.getUTCDate()
        timer = threading.Timer(delayTimer, timerExpired, args=[event, utcDate], kwargs={})
        movedFrom[event.cookie] = (movedFromPath, filesMoved, timer)
        movedFromLock.release()

        #create timer to check if it's claimed by a move to
        timer.start()    

        
class transferWatch(pyinotify.ProcessEvent):
    def __init__(self, unit):
        self.unit=unit

    #when a file is moved out, create a cookie for the file, with the file uuid
    #and a timer, so if it isn't claimed, the cookie is removed.
    def process_IN_MOVED_FROM(self, event):
        print event
        #Wait for a moved to, and if one doesn't occur, consider it moved outside of the system.
        
        movedFromPath = os.path.join(event.path, event.name).replace(\
                             self.unit.currentPath.replace("%sharedPath%", archivematicaMCP.config.get('MCPServer', "sharedDirectory"), 1), \
                             "%transferDirectory%", 1)
        filesMoved = []
        sql = """SELECT fileUUID, currentLocation FROM Files WHERE transferUUID = '""" + self.unit.UUID + "' AND removedTime = 0 AND currentLocation LIKE '" + MySQLdb.escape_string(movedFromPath).replace("%", "%%") + "%';"
        c, sqlLock = databaseInterface.querySQL(sql) 
        row = c.fetchone()
        while row != None:
            print row
            filesMoved.append(row)            
            row = c.fetchone()
        sqlLock.release()
        
        movedFromLock.acquire()
        utcDate = databaseInterface.getUTCDate()
        timer = threading.Timer(delayTimer, timerExpired, args=[event, utcDate], kwargs={})
        movedFrom[event.cookie] = (movedFromPath, filesMoved, timer)
        movedFromLock.release()

        #create timer to check if it's claimed by a move to
        timer.start()
    
    #if a file is moved in, look for a cookie to claim
    def process_IN_MOVED_TO(self, event):
        time.sleep(waitToActOnMoves)
        print event
        movedFromLock.acquire()
        if event.cookie not in movedFrom:
            #if there isn't one - error
            print >>sys.stderr, "#error. No adding files to a sip in this manner."
            movedFromLock.release()
            return
            
        #remove it from the list of unfound moves
        movedFromPath, filesMoved, timer = movedFrom.pop(event.cookie)
        movedFromLock.release()
        
        movedToPath = os.path.join(event.path, event.name).replace(\
                             self.unit.currentPath.replace("%sharedPath%", archivematicaMCP.config.get('MCPServer', "sharedDirectory"), 1), \
                             "%transferDirectory%", 1)
        for fileUUID, oldLocation in filesMoved:
            newFilePath = oldLocation.replace(movedFromPath, movedToPath, 1)
            print "Moved: ", oldLocation, "-> (" + self.unit.UUID + ")" + newFilePath 
            print "Todo - verify it belongs to this transfer"
            #if it's from this transfer 
                #clear the SIP membership
                #update current location

            databaseInterface.runSQL("UPDATE Files " + \
                "SET currentLocation='" + newFilePath +  "', " + \
                "Files.sipUUID = NULL " + \
                "WHERE fileUUID='" + fileUUUID + "'" )        
            #else
                #error ish - file doesn't belong here
                #update current location & clear SIP
    
    #if the transfer is moved/removed
        #???    
        
def addWatchForTransfer(path, unit):
    "Watch for things being removed from the transfer to use the cookie, to know which sip they end up in, if any."
    wm = pyinotify.WatchManager()
    notifier = pyinotify.ThreadedNotifier(wm, transferWatch(unit))
    wm.add_watch(path, mask, rec=True, auto_add=True)
    notifier.start()

def addWatchForSIP(path, unit):
    "Watch for things being removed from the transfer to use the cookie, to know which sip they end up in, if any."
    wm = pyinotify.WatchManager()
    notifier = pyinotify.ThreadedNotifier(wm, SIPWatch(unit))
    wm.add_watch(path, mask, rec=True, auto_add=True)
    notifier.start()
    

def loadExistingFiles():
    #Transfers
    directory = completedTransfersDirectory
    for item in os.listdir(directory):
        if item == ".svn":
            continue
        path = os.path.join(directory, item)
        if os.path.isdir(path):
            path = path + "/"
            unit = unitTransfer(path)
            addWatchForTransfer(path, unit)
        
    #SIPS
    directory = sipCreationDirectory
    for item in os.listdir(directory):
        if item == ".svn":
            continue
        path = os.path.join(directory, item)
        if os.path.isdir(path):
            path = path + "/"
            UUID = archivematicaMCP.findOrCreateSipInDB(path)
            unit = unitSIP(path, UUID) 
            addWatchForSIP(path, unit)


class SIPCreationWatch(pyinotify.ProcessEvent):
    "watches for new sips/completed transfers"
    
    def process_IN_CREATE(self, event):
        self.process_IN_MOVED_TO(event)


    def process_IN_MOVED_TO(self, event):
        time.sleep(1) #let db be updated by the microservice that moved it.
        print event
        path = os.path.join(event.path, event.name)
        if not os.path.isdir(path):
            print >>sys.stderr, "Bad path for watching - not a directory: ", path
            return
        if os.path.abspath(event.path) == os.path.abspath(completedTransfersDirectory):
            path = path + "/"
            unit = unitTransfer(path)
            addWatchForTransfer(path, unit)
        elif os.path.abspath(event.path) == os.path.abspath(sipCreationDirectory):
            path = path + "/"
            UUID = archivematicaMCP.findOrCreateSipInDB(path)
            unit = unitSIP(path, UUID) 
            addWatchForSIP(path, unit)
        else: 
            print >>sys.stderr, "Bad path for watching: ", event.path

def startWatching():
    wm = pyinotify.WatchManager()
    notifier = pyinotify.ThreadedNotifier(wm, SIPCreationWatch())
    wm.add_watch(completedTransfersDirectory, mask, rec=False, auto_add=False)
    wm.add_watch(sipCreationDirectory, mask, rec=False, auto_add=False)
    notifier.start()
    #notifier.loop()

def main():
    loadExistingFiles()
    startWatching()
    
if __name__ == '__main__':
    main()