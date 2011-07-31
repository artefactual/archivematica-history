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
# @subpackage MCPServer
# @author Joseph Perry <joseph@artefactual.com>
# @version svn: $Id$
import sys
import uuid
from linkTaskManagerDirectories import linkTaskManagerDirectories
from linkTaskManagerFiles import linkTaskManagerFiles
from linkTaskManagerChoice import linkTaskManagerChoice
sys.path.append("/usr/lib/archivematica/archivematicaCommon")
import databaseInterface
from databaseFunctions import logJobCreatedSQL

#Constants
constOneTask = 0
constTaskForEachFile = 1
constSelectPathTask = 2 

class jobChainLink:
    def __init__(self, jobChain, jobChainLinkPK, unit):
        self.UUID = uuid.uuid4().__str__()
        self.jobChain = jobChain
        self.pk = jobChainLinkPK
        self.unit = unit
        self.createdDate = databaseInterface.getUTCDate()
        sql = """SELECT MicroServiceChainLinks.currentTask, MicroServiceChainLinks.defaultNextChainLink, TasksConfigs.taskType, TasksConfigs.taskTypePKReference, TasksConfigs.description FROM MicroServiceChainLinks JOIN TasksConfigs on MicroServiceChainLinks.currentTask = TasksConfigs.pk WHERE MicroServiceChainLinks.pk = """ + jobChainLinkPK.__str__() 
        c, sqlLock = databaseInterface.querySQL(sql) 
        row = c.fetchone()
        while row != None:
            print row
            self.currentTask = row[0]
            self.defaultNextChainLink = row[1]
            taskType = row[2]
            taskTypePKReference = row[3]
            self.description = row[4]
            self.reloadFileList = row[4]
            row = c.fetchone()
        sqlLock.release()
        

        
        print "<<<<<<<<< ", self.description, " >>>>>>>>>"
        self.unit.reload()
        
        logJobCreatedSQL(self)        
        
        if self.createTasks(taskType, taskTypePKReference) == None:
            self.getNextChainLinkPK(None)
            #can't have none represent end of chain, and no tasks to process.
            #could return negative?
    
    def createTasks(self, taskType, taskTypePKReference):
        if taskType == constOneTask:
            linkTaskManagerDirectories(self, taskTypePKReference, self.unit)
            
        elif taskType == constTaskForEachFile:
            if self.reloadFileList:
                self.unit.reloadFileList();
            linkTaskManagerFiles(self, taskTypePKReference, self.unit)
        elif taskType == constSelectPathTask:
            linkTaskManagerChoice(self, taskTypePKReference, self.unit)
        else:
            print sys.stderr, "unsupported task type: ", taskType
    
    def getNextChainLinkPK(self, exitCode):
        if exitCode != None:
            ret = self.defaultNextChainLink
            sql = "SELECT nextMicroServiceChainLink FROM MicroServiceChainLinksExitCodes WHERE microServiceChainLink = %s AND exitCode = %s" % (self.pk.__str__(), exitCode.__str__()) 
            c, sqlLock = databaseInterface.querySQL(sql) 
            row = c.fetchone()
            if row != None:
                ret = row[0]
            sqlLock.release()
            return ret
            
    def linkProcessingComplete(self, exitCode):
        self.jobChain.nextChainLink(self.getNextChainLinkPK(exitCode))
    
    