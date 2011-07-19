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
import gearman
import cPickle
import datetime
import archivematicaMCP
import sys
sys.path.append("/usr/lib/archivematica/archivematicaCommon")
from fileOperations import writeToFile


# ~Class Task~
#Tasks are what are assigned to clients.
#They have a zero-many(tasks) TO one(job) relationship
#This relationship is formed by storing a pointer to it's owning job in its job variable.
#They use a "replacement dictionary" to define variables for this task.  
#Variables used for the task are defined in the Job's configuration/module (The xml file)    
class taskStandard():
    """A task is an instance of a command, operating on an entire directory, or a single file."""
    
    def __init__(self, linkTaskManager, execute, arguments, standardOutputFile, standardErrorFile, outputLock=None):
        self.UUID = uuid.uuid4().__str__()
        self.linkTaskManager = linkTaskManager
        self.execute = execute
        self.arguments = arguments
        self.standardOutputFile = standardOutputFile
        self.standardErrorFile = standardErrorFile
        self.outputLock = outputLock
        print "init done"
        self.performTask()
        
    def performTask(self):
        from archivematicaMCP import limitGearmanConnectionsSemaphore
        limitGearmanConnectionsSemaphore.acquire()
        gm_client = gearman.GearmanClient(['localhost:4730', 'otherhost:4730'])
        data = {"createdDate" : datetime.datetime.now().__str__()}
        data["arguments"] = self.arguments
        print '"'+self.execute+'"', data
        completed_job_request = gm_client.submit_job(self.execute.lower(), cPickle.dumps(data), self.UUID)
        limitGearmanConnectionsSemaphore.release()
        self.check_request_status(completed_job_request)
    
    def check_request_status(self, job_request):
        if job_request.complete:
            self.results = cPickle.loads(job_request.result)
            print "Task %s finished!  Result: %s - %s" % (job_request.job.unique, job_request.state, self.results)
            self.writeOutputs()
            self.linkTaskManager.taskCompletedCallBackFunction(self)
            
        elif job_request.timed_out:
            print "Task %s timed out!" % job_request.unique
        elif job_request.state == JOB_UNKNOWN:
            print "Task %s connection failed!" % job_request.unique
        


   
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
                ret = ret.replace("%sharedPath%", archivematicaMCP.config.get('MCPServer', "sharedDirectory"), 1)
            else:
                ret = "<^Not allowed to write to file^> " + ret
        return ret
    
    #Used to write the output of the commands to the specified files
    def writeOutputs(self):
        """Used to write the output of the commands to the specified files"""
        
        
        if self.outputLock != None:
            self.outputLock.acquire()
        
        standardOut = self.writeOutputsValidateOutputFile(self.standardOutputFile)
        standardError = self.writeOutputsValidateOutputFile(self.standardErrorFile)
         
        #output , filename
        a = writeToFile(self.results["stdOut"], standardOut)
        b = writeToFile(self.results["stdError"], standardError)

        if self.outputLock != None:
            self.outputLock.release()
            
        if a:
            self.stdError = "Failed to write to file{" + standardOut + "}\r\n" + self.results["stdOut"]
        if b:
            self.stdError = "Failed to write to file{" + standardError + "}\r\n" + self.results["stdError"]
        if  self.results['exitCode']:
            return self.results['exitCode']
        return a + b 

