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
# @subpackage MCPServer
# @author Joseph Perry <joseph@artefactual.com>
# @version svn: $Id$

from linkTaskManager import linkTaskManager
from taskStandard import taskStandard
from unitFile import unitFile
import databaseInterface
import threading
import math
import uuid
import time
import sys
import archivematicaMCP
sys.path.append("/usr/lib/archivematica/archivematicaCommon")
import databaseFunctions

import os

class linkTaskManagerFiles:
    def __init__(self, jobChainLink, pk, unit):
        self.tasks = {}
        self.tasksLock = threading.Lock()
        self.pk = pk
        self.jobChainLink = jobChainLink
        self.exitCode = 0
        self.clearToNextLink = False
        print "DEBUG pk:", pk
        sql = """SELECT * FROM StandardTasksConfigs where pk = """ + pk.__str__() 
        c, sqlLock = databaseInterface.querySQL(sql) 
        row = c.fetchone()
        while row != None:
            print row
            #pk = row[0] 
            filterFileEnd = row[1]
            filterFileStart = row[2]
            filterSubDir = row[3]
            requiresOutputLock = row[4]
            self.standardOutputFile = row[5]
            self.standardErrorFile = row[6]
            self.execute = row[7]
            self.arguments = row[8]
            row = c.fetchone()
        sqlLock.release()
        
        if requiresOutputLock:
            outputLock = threading.Lock()
        else:
            outputLock = None
        
        SIPReplacementDic = unit.getReplacementDic(unit.currentPath)

        self.tasksLock.acquire()            
        for file, fileUnit in unit.fileList.items():
            print "file:", file, fileUnit
            if filterFileEnd:
                if not file.endswith(filterFileEnd):
                    continue
            if filterFileStart:
                if not os.path.basename(file).startswith(filterFileStart):
                    continue
            if filterSubDir:
                if not file.startswith(unit.pathString + filterSubDir):
                    continue
            
            standardOutputFile = self.standardOutputFile
            standardErrorFile = self.standardErrorFile 
            execute = self.execute
            arguments = self.arguments


            commandReplacementDic = fileUnit.getReplacementDic()
            print commandReplacementDic
            for key in commandReplacementDic.iterkeys():
                value = commandReplacementDic[key].replace("\"", ("\\\""))
                if execute:
                    execute = execute.replace(key, value)
                if arguments:
                    arguments = arguments.replace(key, value)
                if standardOutputFile:
                    standardOutputFile = standardOutputFile.replace(key, value)
                if standardErrorFile:
                    standardErrorFile = standardErrorFile.replace(key, value)
            
            
            for key in SIPReplacementDic.iterkeys():
                value = SIPReplacementDic[key].replace("\"", ("\\\""))
                if execute:
                    execute = execute.replace(key, value)
                if arguments:
                    arguments = arguments.replace(key, value)
                if standardOutputFile:
                    standardOutputFile = standardOutputFile.replace(key, value)
                if standardErrorFile:
                    standardErrorFile = standardErrorFile.replace(key, value)
            
            UUID = uuid.uuid4().__str__()
            task = taskStandard(self, execute, arguments, standardOutputFile, standardErrorFile, outputLock=outputLock, UUID=UUID)
            self.tasks[UUID] = task
            databaseFunctions.logTaskCreatedSQL(self, commandReplacementDic, UUID, arguments)
            t = threading.Thread(target=task.performTask)
            t.daemon = True
            while(archivematicaMCP.limitTaskThreads <= threading.activeCount()):
                print "Waiting for active threads", threading.activeCount()
                self.tasksLock.release()
                time.sleep(archivematicaMCP.limitTaskThreadsSleep)
                self.tasksLock.acquire()
            print "Active threads:", threading.activeCount()
            t.start() 
            
            
        self.clearToNextLink = True
        self.tasksLock.release()
        if self.tasks == {} :
            self.jobChainLink.linkProcessingComplete(self.exitCode)
        
    
    def taskCompletedCallBackFunction(self, task):
        print task
        #logTaskCompleted()
        self.exitCode += math.fabs(task.results["exitCode"])
        databaseFunctions.logTaskCompletedSQL(task)

        if task.UUID in self.tasks: 
            del self.tasks[task.UUID]
        else:
            print >>sys.stderr, "Key Value Error:", task.UUID
            print >>sys.stderr, "Key Value Error:", self.tasks
            exit(1)

        self.tasksLock.acquire()        
        if self.clearToNextLink == True and self.tasks == {} :
            print "DEBUG proceeding to next link", self.jobChainLink.UUID
            self.jobChainLink.linkProcessingComplete(self.exitCode)
        self.tasksLock.release()
      
        
        
        
        