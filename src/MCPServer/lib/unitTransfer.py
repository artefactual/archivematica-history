#!/usr/bin/python -OO

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
# @subpackage MCPServer
# @author Joseph Perry <joseph@artefactual.com>
# @version svn: $Id$

from unit import unit
from unitFile import unitFile
import uuid
import archivematicaMCP
import os
import time
import sys
import pyinotify
import threading
import shutil
from pyinotify import WatchManager
from pyinotify import Notifier
from pyinotify import ThreadedNotifier
from pyinotify import EventsCodes
from pyinotify import ProcessEvent
sys.path.append("/usr/lib/archivematica/archivematicaCommon")
import databaseInterface
import lxml.etree as etree
from fileOperations import renameAsSudo
from databaseFunctions import insertIntoEvents

a = """
class watchDirectoryProcessEvent(ProcessEvent):
    ""Determine which action to take based on the watch directory. ""
    config = None
    def __init__(self, unit):
        self.unit = unit
        self.cookie = None
        
    def process_IN_MOVED_TO(self, event):  
        if self.cookie == event.cookie:
            unit.updateLocation(os.path.join(event.path, event.name) + "/")
            self.cookie = None
    
    def process_IN_MOVED_FROM(self, event):
        if self.unit.currentPath == os.path.join(event.path, event.name) + "/" :
            self.cookie = event.cookie
"""    
class unitTransfer(unit):
    def __init__(self, currentPath, UUID=""):
        #Just Use the end of the directory name
        self.pathString = "%transferDirectory%"
        currentPath2 = currentPath.replace(archivematicaMCP.config.get('MCPServer', "sharedDirectory"), \
                       "%sharedPath%", 1)
        
        if UUID == "":
            sql = """SELECT transferUUID FROM Transfers WHERE currentLocation = '""" + currentPath2 + "'"
            time.sleep(.5)
            c, sqlLock = databaseInterface.querySQL(sql) 
            row = c.fetchone()
            while row != None:
                UUID = row[0]
                print "Opening existing Transfer:", UUID, "-", currentPath2
                row = c.fetchone()
            sqlLock.release()
            
        if UUID == "":
            uuidLen = -36           
            if  archivematicaMCP.isUUID(currentPath[uuidLen-1:-1]):
                UUID = currentPath[uuidLen-1:-1]
            else:
                UUID = uuid.uuid4().__str__()
                self.UUID = UUID
                sql = """INSERT INTO Transfers (transferUUID, currentLocation)
                VALUES ('""" + UUID + databaseInterface.separator + currentPath2 + "');"
                databaseInterface.runSQL(sql)
                
        self.currentPath = currentPath2
        self.UUID = UUID
        self.fileList = {}
        #create a watch of the transfer directory path /.. watching for moves 
        a = """wm = WatchManager()
        notifier = ThreadedNotifier(wm, watchDirectoryProcessEvent(self))
        mask = pyinotify.IN_MOVED_TO | pyinotify.IN_MOVED_FROM
        wdd = wm.add_watch(self.currentPath + "..", mask, rec=False)
        notifier.start()
        self.notifier = notifier
        #^ if the item moved is this unit:
        #update this unit's current location - here and db?"""
    
    def reloadFileList(self):
        print "DEBUG reloading transfer file list: ", self.UUID
        self.fileList = {}
        #os.walk(top[, topdown=True[, onerror=None[, followlinks=False]]])
        currentPath = self.currentPath.replace("%sharedPath%", \
                                               archivematicaMCP.config.get('MCPServer', "sharedDirectory"), 1) + "/"
        print "currentPath: ", currentPath
        for directory, subDirectories, files in os.walk(currentPath):
            directory = directory.replace( currentPath, "%transferDirectory%", 1)
            for file in files:
                filePath = os.path.join(directory, file)
                print filePath
                self.fileList[filePath] = unitFile(filePath)
        
        sql = """SELECT  fileUUID, currentLocation FROM Files WHERE removedTime = 0 AND transferUUID =  '""" + self.UUID + "'"
        c, sqlLock = databaseInterface.querySQL(sql) 
        row = c.fetchone()
        while row != None:
            print row
            UUID = row[0]
            currentPath = row[1]
            if currentPath in self.fileList:
                self.fileList[currentPath].UUID = UUID
            else:
                print >>sys.stderr, self.fileList
                eventDetail = "Transfer {" + self.UUID + "} has file {" + UUID + "}\"" + currentPath + "\" in the database, but file doesn't exist in the file system."
                print >>sys.stderr, "!!!", eventDetail, "!!!"
                #insertIntoEvents(fileUUID=UUID, eventIdentifierUUID=uuid.uuid4().__str__(), eventType="MCP warning", eventDetail=eventDetail)
            row = c.fetchone()
        sqlLock.release()
        
    def updateLocation(self, newLocation):
        self.currentPath = newLocation
        sql =  """UPDATE Transfers SET currentPath='""" + newLocation + """' WHERE transferUUID='""" + self.UUID + """';"""
        databaseInterface.runSQL(sql)
    
    def setMagicLink(self,link, exitStatus=""):
        if exitStatus != "":
            sql =  """UPDATE Transfers SET magicLink='""" + link + """', magicLinkExitMessage='""" + exitStatus + """' WHERE transferUUID='""" + self.UUID + """';"""
        else:
            sql =  """UPDATE Transfers SET magicLink='""" + link + """' WHERE transferUUID='""" + self.UUID + """';"""        
        databaseInterface.runSQL(sql)
    
    def getMagicLink(self):
        ret = None
        sql = """SELECT magicLink, magicLinkExitMessage FROM Transfers WHERE transferUUID =  '""" + self.UUID + "'" 
        c, sqlLock = databaseInterface.querySQL(sql) 
        row = c.fetchone()
        while row != None:
            print row
            ret = row
            row = c.fetchone()
        sqlLock.release()
        return ret
        
        
    def reload(self):
        sql = """SELECT transferUUID, currentLocation FROM Transfers WHERE transferUUID =  '""" + self.UUID + "'" 
        c, sqlLock = databaseInterface.querySQL(sql) 
        row = c.fetchone()
        while row != None:
            print row
            self.UUID = row[0]
            #self.createdTime = row[1] 
            self.currentPath = row[1]
            row = c.fetchone()
        sqlLock.release()
        return
             
        
    def getReplacementDic(self, target):
        # self.currentPath = currentPath.__str__()
        # self.UUID = uuid.uuid4().__str__()
        #Pre do some variables, that other variables rely on, because dictionaries don't maintain order
        SIPUUID = self.UUID
        if self.currentPath.endswith("/"):
            SIPName = os.path.basename(self.currentPath[:-1]).replace("-" + SIPUUID, "")
        else:
            SIPName = os.path.basename(self.currentPath).replace("-" + SIPUUID, "")
        SIPDirectory = self.currentPath.replace(archivematicaMCP.config.get('MCPServer', "sharedDirectory"), "%sharedPath%")
        relativeDirectoryLocation = target.replace(archivematicaMCP.config.get('MCPServer', "sharedDirectory"), "%sharedPath%")
      
        
        ret = { \
        "%SIPLogsDirectory%": SIPDirectory + "logs/", \
        "%SIPObjectsDirectory%": SIPDirectory + "objects/", \
        "%SIPDirectory%": SIPDirectory, \
        "%transferDirectory%": SIPDirectory, \
        "%SIPDirectoryBasename%": os.path.basename(os.path.abspath(SIPDirectory)), \
        "%relativeLocation%": target.replace(self.currentPath, relativeDirectoryLocation, 1), \
        "%processingDirectory%": archivematicaMCP.config.get('MCPServer', "processingDirectory"), \
        "%checksumsNoExtention%":archivematicaMCP.config.get('MCPServer', "checksumsNoExtention"), \
        "%watchDirectoryPath%":archivematicaMCP.config.get('MCPServer', "watchDirectoryPath"), \
        "%AIPsStore%":archivematicaMCP.config.get('MCPServer', "AIPsStore"), \
        "%rejectedDirectory%":archivematicaMCP.config.get('MCPServer', "rejectedDirectory"), \
        "%SIPUUID%":SIPUUID, \
        "%SIPName%":SIPName \
        }
        return ret
    
    def xmlify(self):
        ret = etree.Element("unit")
        etree.SubElement(ret, "type").text = "Transfer"
        unitXML = etree.SubElement(ret, "unitXML")
        etree.SubElement(unitXML, "UUID").text = self.UUID
        etree.SubElement(unitXML, "currentPath").text = self.currentPath.replace(archivematicaMCP.config.get('MCPServer', "sharedDirectory"), "%sharedPath%")
        return ret

a = """    
    def __del__(self):
        #TODO - cleanup the watch directory for this unit
        self. notifier.stop()
        super.__del__()
"""