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

import uuid

# ~Class Task~
#Tasks are what are assigned to clients.
#They have a zero-many(tasks) TO one(job) relationship
#This relationship is formed by storing a pointer to it's owning job in its job variable.
#They use a "replacement dictionary" to define variables for this task.  
#Variables used for the task are defined in the Job's configuration/module (The xml file)    
class taskStandard():
    """A task is an instance of a command, operating on an entire directory, or a single file."""
    
    def __init__(self, link, execute, arguments, taskAssignedCallBackFunction, taskCompletedCallBackFunction, standardOutputFile, standardErrorFile):
        self.UUID = uuid.uuid4().__str__()
        self.link = link
        self.execute = execute
        self.arguments = arguments
        self.taskAssignedCallBackFunction = taskAssignedCallBackFunction
        self.taskCompletedCallBackFunction = taskCompletedCallBackFunction
        self.standardOutputFile = standardOutputFile
        self.standardErrorFile = standardErrorFile


   
    #note lock tasksLock first
    def xmlify(self):
        ret = etree.Element("task")
        etree.SubElement(ret, "UUID").text = self.UUID.__str__()
        etree.SubElement(ret, "jobUUID").text = self.job.UUID.__str__()
        etree.SubElement(ret, "execute").text = self.execute
        etree.SubElement(ret, "arguments").text = self.arguments
        etree.SubElement(ret, "target").text = self.target
        return ret
    
    #This function is used to verify that where 
    #the MCP is writing to is an allowable location
    #@fileName - full path of file it wants to validate. 
    def writeOutputsValidateOutputFile(self, fileName):
        ret = fileName
        if ret:
            if "%sharedPath%" in ret and "../" not in ret:
                ret = ret.replace("%sharedPath%", config.get('MCPServer', "sharedDirectory"), 1)
            else:
                ret = "<^Not allowed to write to file^> " + ret
        return ret
    
    #Used to write the output of the commands to the specified files
    def writeOutputs(self):
        """Used to write the output of the commands to the specified files"""
        requiresOutputLock = self.command.requiresOutputLock.lower() == "yes"
        
        if requiresOutputLock:
            self.job.writeLock.acquire()
        
        standardOut = self.writeOutputsValidateOutputFile(self.standardOut)
        standardError = self.writeOutputsValidateOutputFile(self.standardError)
         
        #output , filename
        a = writeToFile(self.stdOut, standardOut)
        b = writeToFile(self.stdError, standardError)

        if requiresOutputLock:
            self.job.writeLock.release()
            
        if a:
            self.stdError = "Failed to write to file{" + self.standardOut + "}\r\n" + self.stdError
        if b:
            self.stdError = "Failed to write to file{" + self.standardError + "}\r\n" + self.stdError
        if  self.exitCode:
            return self.exitCode
        return a + b 

    #Called when Client reports this task is done.
    #Called from archivematicaMCPServerProtocol class
    #Pseudo code
    ##remove from tasks being processed.
    ##Determine if the Job step is done by seeing if is the last task to execute for that job.
    ##If the job step is done; let the job know.
    #@returned - The exit code of the task
    def completed(self, returned):
        """When a task is completed, check to see if it was the last task for the job to be completed (job completed)."""
        self.exitCode = returned
        returned = self.writeOutputs()
        tasksLock.acquire()
        jobStepDone = True
        if self in tasksBeingProcessed:
            tasksBeingProcessed.remove(self)
        else:
            print "This shouldn't happen"
            print "Task:", self.UUID
            print self
            for task in tasksBeingProcessed:
                print task, task.UUID
      
        for task in tasksQueue:
            if task.job.UUID == self.job.UUID:
                jobStepDone = False
                break
        if jobStepDone:
            for task in tasksBeingProcessed:
                if task.job.UUID == self.job.UUID:
                    jobStepDone = False
                    break
        self.job.combinedRet += math.fabs(returned)
        logTaskCompleted(self, returned)
        tasksLock.release() 
        
        if jobStepDone:
            print "Job step done: " + self.job.step
            self.job.jobStepCompleted()
        else:
            print "More tasks to be processed for Job"