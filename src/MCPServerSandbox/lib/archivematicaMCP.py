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

#~DOC~
#
# --- This is the MCP (master control program) ---
# The intention of this program is to provide a centralized automated distributed system for performing an arbitrary set of tasks on a directory.
# Distributed in that the work can be performed on more than one physical computer simultaneously.
# Centralized in that there is one centre point for configuring flow through the system.
# Automated in that the tasks performed will be based on the config files and instantiated for each of the targets.
#
# It loads configurations from the XML files.
# These files contain:
# -The associated watch directory
# -A set of commands to run on the files within that directory.
# -The place to move the directory to once it has been processed.
#
# When a directory is placed within a a watch directory, it generates an event.
# The event creates an associated Job.
# The job is an instance of one of the config files (depending on which watch directory generated the event).
# The job will have a number of steps, for each of the commands.
# The commands will be instantiated into tasks for each of the files within the watch directory of the event, or just one task for the directory (depending on the config).



import signal
import os
import pyinotify
from archivematicaReplacementDics import replacementDics 
from MCPlogging import *
from MCPloggingSQL import getUTCDate
import ConfigParser
from mcpModules.modules import modulesClass
from pyinotify import WatchManager
from pyinotify import Notifier
from pyinotify import ThreadedNotifier
from pyinotify import EventsCodes
from pyinotify import ProcessEvent
import uuid
import threading
import string
import math
import copy
import time
import subprocess
import shlex
import sys
import lxml.etree as etree
from twisted.internet import reactor
from twisted.internet import protocol as twistedProtocol
from twisted.protocols.basic import LineReceiver
import xmlrpclib
#from SimpleXMLRPCServer import SimpleXMLRPCServer
from twisted.web import xmlrpc
from twisted.web import server
from twisted.application import service
from twisted.application import internet
application = service.Application("archivematicaMCPServer")

config = ConfigParser.SafeConfigParser({'MCPArchivematicaServerInterface': ""})
config.read("/etc/archivematica/MCPServer/serverConfig.conf")
archivematicaRD = replacementDics(config)


#depends on OS whether you need one line or other. I think Events.Codes is older.
mask = pyinotify.IN_CREATE | pyinotify.IN_MOVED_TO  #watched events
maskForCopied = pyinotify.IN_CREATE | pyinotify.IN_MODIFY
#mask = EventsCodes.IN_CREATE | EventsCodes.IN_MOVED_TO  #watched events
configs = []
jobsAwaitingApproval = []
jobsQueue = [] #jobs shouldn't remain here long (a few seconds max) before they are turned into tasks (jobs being processed)
jobsBeingProcessed = []
tasksQueue = []
tasksBeingProcessed = []
tasksLock = threading.Lock()
movingDirectoryLock = threading.Lock()
factory = twistedProtocol.ServerFactory()
jobsLock = threading.Lock()
watchedDirectories = []

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

class archivematicaXMLrpc(xmlrpc.XMLRPC):
    # Used by RPC
    #@returns - string of XML representation of JOBs awaiting approval.
    def xmlrpc_getJobsAwaitingApproval(self):
        """returns - string of XML representation of JOBs awaiting approval."""
        jobsLock.acquire()
        ret = etree.Element("JobsAwaitingApproval")
        for job in jobsAwaitingApproval:
            ret.append(job.xmlify())
        jobsLock.release()
        #print etree.tostring(ret, encoding=unicode, method='text')
        #return etree.tostring(ret, encoding=unicode, method='text')
        return etree.tostring(ret, pretty_print=True)

    # Used by RPC
    #Searches for job with matching UUID in the 
    #jobsAwaitingApproval list, and if found, rejects it.
    #@jobUUID - string to match to a job's UUID
    def xmlrpc_rejectJob(self, jobUUID):
        """Reject job with the give string UUID"""
        theJob = None
        for job in jobsAwaitingApproval:
            if job.UUID.__str__() == jobUUID:
                theJob = job
                break
        if theJob:
            print "Rejecting Job: " + theJob.UUID.__str__()
            theJob.reject()
            return "Rejecting Job: " + theJob.UUID.__str__()
        return "Rejecting Job Failed: " + jobUUID

    
    # Used by RPC
    #Searches for job with matching UUID in the 
    #jobsAwaitingApproval list, and if found, approves it.
    #@jobUUID - string to match to a job's UUID
    def xmlrpc_approveJob(self, jobUUID):
        """Approves job with the give string UUID"""
        theJob = None
        for job in jobsAwaitingApproval:
            if job.UUID.__str__() == jobUUID:
                theJob = job
                break
        if theJob:
            print "Approving Job: " + theJob.UUID.__str__()
            theJob.approve()
            return "Approving Job: " + theJob.UUID.__str__()
        return "Approving Job Failed " + jobUUID
    
    # Used by RPC
    #@returns - string of XML representation of clients
    def xmlrpc_getClientInfo(self):
        """returns - string of XML representation of clients."""
        ret = etree.Element("Clients")
        for client in factory.clients:
            ret.append(client.xmlify())
        return etree.tostring(ret, pretty_print=True)

# Used to move/rename Directories that the archivematica user
# may or may not have writes to move.
def renameAsSudo(source, destination):
    """Used to move/rename Directories that the archivematica user may or may not have writes to move"""
    commandString = "sudo mv \"" + source + "\"   \"" + destination + "\""
    p = subprocess.Popen(shlex.split(commandString))
    p.wait()

#This is where the Job processing starts.
#directory is moved to processing directory 
#tasks are created.
def checkJobQueue():
    """Creates Tasks for new auto approved jobs, or just approved jobs."""
    jobsLock.acquire()
    for job in jobsQueue:
        #print "  " + job.UUID.__str__() + "\t" + job.config.identifier + "\t" + job.directory.__str__() + "\t" + job.step
        directory = job.config.processingDirectory + job.UUID.__str__() + "/"
        print
        print "job UUID: " + job.UUID.__str__()
        print "moving: " + job.directory + "\t to: \t" + directory + job.directory.split("/")[-1]
        os.makedirs(directory, mode=0777)
        renameAsSudo(job.directory, directory + job.directory.split("/")[-1])
        tasksCreated = job.createTasksForCurrentStep() 
        jobsQueue.remove(job)
        if tasksCreated:
            jobsBeingProcessed.append(job) 
        else:
            job.step = "completedSuccessfully"
            logJobStepChanged(job)
    jobsLock.release()
    processTaskQueue()

#This is where tasks are assigned to clients.
#Pseudo code
##For Each Task 
###IF there is a client available that supports this task
####Assign it to that client
def processTaskQueue():
    """Attempts to assign tasks to clients."""
    tasksLock.acquire()
    print "Processing Tasks Queue {" + len(tasksBeingProcessed).__str__() + "/"+ len(tasksQueue).__str__() + "/" + \
    (len(tasksBeingProcessed) + len(tasksQueue)).__str__() + "}..."
    for task in tasksQueue:
        taskAssigned = False
        for client in factory.clients:
            #print client.clientName, client.supportedCommands
            client.clientLock.acquire()
            if client.currentThreads < client.maxThreads:
                for supportedCommand in client.supportedCommands:
                    #print client.clientName, supportedCommand, task.execute, supportedCommand == task.execute  
                    if supportedCommand == task.execute:
                        tasksQueue.remove(task)
                        task.assignedDate=getUTCDate()
                        task.arguments = task.arguments.__str__().replace("%date%", task.assignedDate)
                        task.arguments = task.arguments.__str__().replace("%jobCreatedDate%", task.job.createdDate)
                        tasksBeingProcessed.append(task)
                        task.client = client
                        send = config.get('Protocol', "performTask")
                        send += config.get('Protocol', "delimiter")
                        send += task.UUID.__str__()
                        send += config.get('Protocol', "delimiter")
                        if task.standardIn:
                            send += task.standardIn.__str__() 
                        send += config.get('Protocol', "delimiter")
                        send += task.execute.__str__()
                        send += config.get('Protocol', "delimiter")
                        send += task.arguments.__str__()
                        client.write(send)
                        client.currentThreads += 1
                        taskAssigned = True
                        logTaskAssigned(task, client)
                        print "assigned task: " + task.UUID.__str__()
                        print "client threads{" + client.clientName + "}: " + client.currentThreads.__str__()
                        break 
            client.clientLock.release()
            if taskAssigned:
                break #break up to next task
            #else:
                #print "\tNo client currently available to run: " + task.execute + " {" + task.UUID.__str__() + "}"
    tasksLock.release()    

# ~Class Task~
#Tasks are what are assigned to clients.
#They have a zero-many(tasks) TO one(job) relationship
#This relationship is formed by storing a pointer to it's owning job in its job variable.
#They use a "replacement dictionary" to define variables for this task.  
#Variables used for the task are defined in the Job's configuration/module (The xml file)    
class Task():
    """A task is an instance of a command, operating on an entire directory, or a single file."""
    
    #instantiates a task object
    #@job - The associated job this task belongs to
    #@target - The file or directory this task is to operate on.
    #@command - The command this task is to execute
    def __init__(self, job, target, command):
        self.UUID = uuid.uuid4()
        self.job = job
        self.command = command
        self.execute = command.execute.lower()
        self.arguments = command.arguments
        self.description = command.descriptionWhileExecuting
        self.target = target
        self.standardIn = command.standardIn
        self.standardOut = command.standardOut
        self.standardError = command.standardError
        self.stdOut = ""
        self.stdError = ""
        self.client = None
        
        
        commandReplacementDic = archivematicaRD.commandReplacementDic(self, job, target, command)
        
        #for each key replace all instances of the key in the command string
        for key in commandReplacementDic.iterkeys():
            value = commandReplacementDic[key].replace("\"", ("\\\""))
            if self.description:
                self.description = self.description.replace(key, value)
            if self.execute:
                self.execute = self.execute.replace(key, value)
            if self.arguments:
                self.arguments = self.arguments.replace(key, value)
            if self.standardIn:
                self.standardIn = self.standardIn.replace(key, value)
            if self.standardOut:
                self.standardOut = self.standardOut.replace(key, value)
            if self.standardError:
                self.standardError = self.standardError.replace(key, value)

        logTaskCreated(self, commandReplacementDic)
    
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

# ~Class Task~
#Tasks are what are assigned to clients.
#They have a one(job) TO zero-many(tasks) relationship
#This relationship is maintained by storing a pointer to the job in the task.   
class Job:
    """A job is an instance of a file in a watch directory (from a config file)."""
    
    #instantiates a job object
    #@config - the config to use against the given directory
    #@directory - The directory this job operates on.
    def __init__(self, configs, directory, step="exeCommand"):
        self.combinedRet = 0
        self.UUID = uuid.uuid4()
        self.config = copy.deepcopy(configs)
        self.step = step
        self.directory = directory
        self.writeLock = threading.Lock()
        self.createdDate=getUTCDate()
        
        if config.get('MCPServer', "forceNoApprovalRequiredOnAllJobs").lower() == "true":
            self.config.requiresUserApproval = False
            configs.requiresUserApproval = False
        
        replacementDic = archivematicaRD.jobReplacementDic(self, configs, directory, step)
        
        if self.config.requiresUserApproval:
            self.step="requiresApproval"
      
        #for each key replace all instances of the key in the strings
        for key in replacementDic.iterkeys():
            self.directory = self.directory.replace(key, replacementDic[key])
            self.config.processingDirectory = self.config.processingDirectory.replace(key, replacementDic[key])
            self.config.successDirectory = self.config.successDirectory.replace(key, replacementDic[key])
            self.config.failureDirectory = self.config.failureDirectory.replace(key, replacementDic[key])
            self.config.rejectDirectory = self.config.rejectDirectory.replace(key, replacementDic[key])
            self.config.descriptionForApproval = self.config.descriptionForApproval.replace(key, replacementDic[key])
        logJobCreated(self)

    #used by RPC functions.
    #@return - an xml represenation of the job    
    def xmlify(self):
        ret = etree.Element("Job")
        etree.SubElement(ret, "UUID").text = self.UUID.__str__()
        etree.SubElement(ret, "directory").text = self.directory
        etree.SubElement(ret, "descriptionForApproval").text = self.config.descriptionForApproval
        return ret

    #used by RPC functions.
    #Pseudo code
    ##remove from jobs awaiting approval
    ##append to jobsQueue
    ##Call to process the jobsQueue
    def approve(self):
        jobsLock.acquire()
        logJobStepCompleted(self)
        self.step = "exeCommand"
        if self in jobsAwaitingApproval:
            jobsAwaitingApproval.remove(self)
        jobsQueue.append(self)
        jobsLock.release()
        checkJobQueue()
    
    #used by RPC functions.
    #Pseudo code
    ##remove from jobs awaiting approval
    ##Move directory to rejected location
    def reject(self):
        jobsLock.acquire()
        logJobStepCompleted(self)
        self.step = "Rejected"
        logJobStepChanged(self)
        if self in jobsAwaitingApproval:
            jobsAwaitingApproval.remove(self)
        jobsLock.release()
        renameAsSudo(self.directory, self.config.rejectDirectory)

    #Called when last task for job is completed.
    #Advances the job to the next step [if there is one]
    #If the last step is completed, moves the processed directory to it's output location.
    def jobStepCompleted(self):
        """When a job step is completed, move to the next step, or if the job is completed, move everthing in the directory to the output directory. """
        logJobStepCompleted(self)
        #if last step completed
        if self.step == "cleanupSuccessfulCommand"\
        or self.step == "cleanupUnsuccessfulCommand":
            #time.sleep(5) - attempt to fix Resource busy
            #lock to ensure it doesn't start processing the next step, before the entire directory is moved.
            movingDirectoryLock.acquire()
            #move directory to next location, depending on fail status
            destination = ""
            if self.step == "cleanupSuccessfulCommand":
                self.step="completedSuccessfully"
                destination = self.config.successDirectory
            else: #"cleanupUnsuccessfulCommand"
                destination = self.config.failureDirectory
                self.step="completedUnsuccessfully"
            directory = self.config.processingDirectory + self.UUID.__str__() + "/"
            for f in os.listdir(directory):
                print "rename: " + os.path.join(directory, f) + "{" + self.directory + "} TO: " + os.path.join(destination, f)
                renameAsSudo( os.path.join(directory, f), os.path.join(destination, f) )
            os.rmdir(directory)
            movingDirectoryLock.release()
            
            #remove this job from the jobsQueue
            for job in jobsBeingProcessed:
                if job == self:
                    jobsBeingProcessed.remove(self)
                    break

            
            #TODO - Log
            
        elif self.step == "exeCommand":
            self.step = "verificationCommand"
            self.createTasksForCurrentStep()
            processTaskQueue()
        elif self.step == "verificationCommand":
            if self.combinedRet:
                self.step = "cleanupUnsuccessfulCommand"
            else:
                self.step = "cleanupSuccessfulCommand"
            self.createTasksForCurrentStep()
            processTaskQueue()
        else:
            print "MCP error: Job in bad step: " + job.step.__str__()
        
        logJobStepChanged(self)
    
    #Creates the task(s) for the given command
    #@command the command object to base the steps on. See ./mcpModules/commands/commands.py for class source.        
    def createTasksForStep(self, command):
        """Creates the tasks for the given command"""
        ret = []
        directory = self.config.processingDirectory + self.UUID.__str__() + "/" + os.path.basename(self.directory) + "/"
        if command.filterDir:
            directory += command.filterDir   
        if command.executeOnEachFile:
            ret = self.createTasksForStepInDirectory(command, directory)
        else:
            ret.append(Task(self, directory, command))
        return ret
    
    #Creates the task(s) for the given command, for every file in the directory
    #@command the command object to base the steps on. See ./mcpModules/commands/commands.py for class source.
    def createTasksForStepInDirectory(self, command, directory):
        """for every file in the directory, recursively, create a new task."""
        ret = []
        #print "Creating tasks for directory: " + directory
        if os.path.isdir(directory):
            for f in os.listdir(directory):
                #print f
                if os.path.isdir(os.path.join(directory, f)):
                    sub = self.createTasksForStepInDirectory(command, os.path.join(directory, f))
                    for task in sub:
                        ret.append(task)
                if command.filterFileEnd or command.filterFileStart:
                    if os.path.isfile(os.path.join(directory, f)):
                        if command.filterFileEnd and command.filterFileStart \
                        and f.__str__().endswith(command.filterFileEnd) \
                        and f.__str__().startswith(command.filterFileStart):
                            task = Task(self, os.path.join(directory, f).__str__(), command)
                            ret.append(task)
                        elif command.filterFileEnd and f.__str__().endswith(command.filterFileEnd):
                            task = Task(self, os.path.join(directory, f).__str__(), command)
                            ret.append(task)
                        elif command.filterFileStart and f.__str__().startswith(command.filterFileStart):
                            task = Task(self, os.path.join(directory, f).__str__(), command)
                            ret.append(task)
                else:
                    if os.path.isfile(os.path.join(directory, f)):
                        task = Task(self, os.path.join(directory, f).__str__(), command)
                        ret.append(task)
        else:
            print "error: tried to process file, not directory." + self.directory.__str__()
        return ret
    
    #@return - returns a list of the tasks created            
    def createTasksForCurrentStep(self):
        """Determine the current step, and if it is to be skipped. 
        If it's not to be skipped, create the tasks for it, append them to the queue and process the queue"""
        if self.step == "exeCommand":
            if not self.config.exeCommand.skip:
                tasks = self.createTasksForStep(self.config.exeCommand)
                tasksLock.acquire()
                for task in tasks:
                    tasksQueue.append(task)
                tasksLock.release()
                processTaskQueue()
                return tasks
            else:
                self.step = "verificationCommand"
                return self.createTasksForCurrentStep()
        elif self.step == "verificationCommand":
            if not self.config.verificationCommand.skip:
                tasks = self.createTasksForStep(self.config.verificationCommand)
                tasksLock.acquire()
                for task in tasks:
                    tasksQueue.append(task)
                tasksLock.release()
                processTaskQueue()
                return tasks
            else:
                if self.combinedRet:
                    self.step = "cleanupUnsuccessfulCommand"
                else:
                    self.step = "cleanupSuccessfulCommand"
                return self.createTasksForCurrentStep()
        elif self.step == "cleanupSuccessfulCommand":
            if not self.config.cleanupSuccessfulCommand.skip:
                tasks = self.createTasksForStep(self.config.cleanupSuccessfulCommand)
                tasksLock.acquire()
                for task in tasks:
                    tasksQueue.append(task)
                tasksLock.release()
                processTaskQueue()
                return tasks
            else:
                self.jobStepCompleted()
                return []
        elif self.step == "cleanupUnsuccessfulCommand":
            if not self.config.cleanupUnsuccessfulCommand.skip:
                tasks = self.createTasksForStep(self.config.cleanupUnsuccessfulCommand)
                tasksLock.acquire()
                for task in tasks:
                    tasksQueue.append(task)
                tasksLock.release()
                processTaskQueue()
                return tasks
            else:
                self.jobStepCompleted()
                return []
        else:
            print "Job in bad step: " + self.step.__str__()
            return []

#Used to monitor directories copied to the MCP, to act when they are done copying.
class archivematicaWatchDirectoryTimer():
    def __init__(self, watchDirectory, event, watchManager, path, delay=config.getint('MCPServer', "MCPWaitForCopyToCompleteSeconds")):
        self.watchDirectory = watchDirectory
        self.event = event
        self.delay = delay
        self.watchManager = watchManager
        self.path = path
        self.timerLock = threading.Lock()    
        args=[self]
        self.timer = threading.Timer(self.delay, self.timerExpired)
        self.timer.start()

    def resetDelay(self):
        self.timerLock.acquire()
        #print "resetting delay: ", self
        self.timer.cancel()
        self.timer = threading.Timer(self.delay, self.timerExpired)
        self.timer.start()
        self.timerLock.release()
    
    def timerExpired(self):
        self.timerLock.acquire()
        #print "time expired", self
        wd = self.watchManager.get_wd(self.path)
        self.watchManager.rm_watch(wd, rec=True) 
        self.watchDirectory.process_IN_MOVED_TO(self.event)

#Used to monitor directories copied to the MCP, to see when they are done copying.
class directoryCreated(ProcessEvent):
    """Determine which action to take based on the watch directory. """
    def __init__(self, watchDirectory, event, watchManager, path, timer=None):
        self.timer = timer
        if self.timer == None:
            self.timer = archivematicaWatchDirectoryTimer(watchDirectory, event, watchManager, path) # self to rm, wd and event to activate Processing.
            
    def process_IN_CREATE(self, event):
        self.process_IN_MODIFY(event)
        
    def process_IN_MODIFY(self, event):
        self.timer.resetDelay()


#This class holds the relation betwen watched directories, and their configs.
#This is a one to one relationship.
class watchDirectory(ProcessEvent):
    """Determine which action to take based on the watch directory. """
    config = None
    def __init__(self, config):
        self.config = config
    def process_IN_CREATE(self, event):
        if config.get('MCPServer', "actOnCopied").lower() == "true":
            if os.path.isdir(os.path.join(event.path, event.name)):
                wm = WatchManager()
                notifier = ThreadedNotifier(wm, directoryCreated(self, event, wm, os.path.join(event.path, event.name)))
                wdd = wm.add_watch(os.path.join(event.path, event.name), maskForCopied, rec=True, auto_add=True)
                notifier.start()
            else:
                print "Warning: %s was created. It is a file, not a directory."
        else:
            print "Warning: %s was created. Was something copied into this directory?" %  os.path.join(event.path, event.name)
        
    def process_IN_MOVED_TO(self, event):  
        """Create a Job based on what was moved into the directory and process it."""
        #ensure no directories are in the process of moving. (so none will be in the middle of moving INTO this directory)
        movingDirectoryLock.acquire()
        movingDirectoryLock.release()    
        
        job = Job(self.config, os.path.join(event.path, event.name))
        if self.config.requiresUserApproval:
            #print "need to get user approval"
            print "Created job awaiting approval"
            jobsAwaitingApproval.append(job)
            #dashboard Alert - new job needing approval.
            
        else:
            jobsQueue.append(job)
            checkJobQueue()

def loadConfigs():
    """Loads the XML config files, with the directories to watch, and the associated commands"""
    configFiles = []
    for dirs, subDirs, files in os.walk(config.get('MCPServer', "moduleConfigDir")):
        configFiles = files
        break

    for configFile in configFiles:
        if configFile.endswith(".xml"):
            configs.append(modulesClass(config.get('MCPServer', "moduleConfigDir"), configFile))
    return configs
        
def loadDirectoryWatchLlist(configs):
    """Start watching all the watch directories defined in the configs. """
    replacementDic = archivematicaRD.watchFolderRepacementDic()
    for config in configs:
        preExisting = False
                #for each key replace all instances of the key in the strings
        for key in replacementDic.iterkeys():
          config.watchDirectory = config.watchDirectory.replace(key, replacementDic[key])
        for wd in watchedDirectories:
            if wd == config.watchDirectory:
                preExisting = True
        if not preExisting:
            wm = WatchManager()
            watchedDirectories.append(config.watchDirectory)
            notifier = ThreadedNotifier(wm, watchDirectory(config))
            wdd = wm.add_watch(config.watchDirectory, mask, rec=False)
            notifier.start()           
        else:
            print "Tried to watch a directory that is already being watched: " + config.watchDirectory
    print "Watching the following directories:"
    watchedDirectories.sort()
    for wd in watchedDirectories:
        print wd

#This class is a mix of two types of functions.
#-The functions called by the twisted python framework, 
#  asyncrounously to handle various events.
#-The functions to handle MCP processing
#The "protocolDic" associates the archivematica protocol with corresponding function.
#ie. if I receive a packet that starts with "taskCompleted", call the task completed function.
class archivematicaMCPServerProtocol(LineReceiver):
    """This is the MCP protocol implemented"""
  
    def __init__(self):
        self.channelOpen = False
        self.maxThreads = 0
        self.currentThreads = 0
        self.clientName = ""
        self.supportedCommands = []
        self.clientLock = threading.Lock()
        self.sendLock = threading.Lock()
        self.keepAliveLock = threading.Lock()
        self.MAX_LENGTH = config.getint('Protocol', "maxLen")
    
    def xmlify(self):
        tasksLock.acquire()
        self.clientLock.acquire()
        ret = etree.Element("Client")
        etree.SubElement(ret, "clientName").text = self.clientName
        etree.SubElement(ret, "maxThreads").text = self.maxThreads.__str__()
        etree.SubElement(ret, "currentThreads").text = self.currentThreads.__str__()
        tasks = etree.SubElement(ret, "currentThreads")
        for task in tasksBeingProcessed:
            if task.client == self:
                tasks.append(task.xmlify())
        supportedTasks = etree.SubElement(ret, "supportedTasks")
        for supportedCommand in self.supportedCommands:
            etree.SubElement(supportedTasks, "supportedTask").text = supportedCommand
        self.clientLock.release()
        tasksLock.release()
        return ret
    
    def lineLengthExceeded(self, line):
        print >>sys.stderr, "Protocol maxLen Exceeded."
    
    def badProtocol(self, command):
        """The client sent a command this server cannot interpret."""
        print "read(bad protocol): " + command.__str__()
   
    def lineReceived(self, line):
        "As soon as any data is received, write it back."
        command = line.split(config.get('Protocol', "delimiter"))
        if len(command):
            t = threading.Thread(target=self.protocolDic.get(command[0], archivematicaMCPServerProtocol.badProtocol),\
            args=(self, command, ))
            t.start()
        else:
            badProtocol(self, command)

    def connectionMade(self):
        """Called when a new client connects"""
        self.write("hello, client!")
        self.channelOpen = True
        t = threading.Thread(target=self.keepAlive)
        t.start()
        self.factory.clients.append(self)

    def keepAlive(self):
        while 1:
            self.keepAliveLock.acquire()
            if self.channelOpen:
                self.write(config.get('Protocol', "keepAlive"))
                self.keepAliveLock.release()
                time.sleep(string.atoi(config.get('Protocol', "keepAlivePause"))) 
            else:
                self.keepAliveLock.release()
                break
        
    def connectionLost(self, reason):
        print "Lost client: " + self.clientName
        self.keepAliveLock.acquire()
        self.channelOpen = False
        self.keepAliveLock.release()
        self.factory.clients.remove(self)
        
        tasksRunningWhileClientDisconnected = []
        tasksLock.acquire()
        for task in tasksBeingProcessed:
            if task.client == self:
                tasksRunningWhileClientDisconnected.append(task)
        tasksLock.release()
        for task in tasksRunningWhileClientDisconnected:
            task.stdOut = ""
            task.stdError = "The client " + self.clientName + " disconnected while this was processing."
            task.completed(-9)
        
    def write(self,line):      
        #Twisted isn't thread safe, use locks.
        self.sendLock.acquire() 
        reactor.callFromThread(self.transport.write, line + "\r\n")
        self.sendLock.release()
        print "\twrote: " + line.__str__()
    
    def addToListTaskHandler(self, command):
        """inform the server the client is capable of running a certain type of task"""
        if len(command) == 2:
            self.supportedCommands.append(command[1])
            processTaskQueue()
        else:
            badProtocol(self, command)
    
    def taskCompleted(self, command):
        """inform the server a task is completed""" 
        if len(command) == 5:
            
            #might be a potential DOS attack.
            ret = string.atoi(command[2])
            
            taskUUID=command[1]
            theTask = None
            tasksLock.acquire()
            for task in tasksBeingProcessed:
                if task.UUID.__str__() == taskUUID:
                    theTask = task
                    break
            tasksLock.release()
            if theTask:
                print "task completed: {" + theTask.UUID.__str__() + "}" + ret.__str__() + "\r\n\t" + command[3] + "\r\n\t" + command[4]
                self.clientLock.acquire()
                self.currentThreads = self.currentThreads - 1
                self.clientLock.release()
                print "current threads on client: " + self.currentThreads.__str__()
                theTask.stdOut = command[3]
                theTask.stdError = command[4]
                theTask.completed(ret)
            else:
                self.badProtocol(command)
            processTaskQueue()
        else:
            self.badProtocol(command)
    
    def maxTasks(self, command):
        """tell the server how many threads this client will run""" 
        if len(command) == 2:
            print self.clientName + "-setting max threads to: " + command[1]
            self.maxThreads = string.atoi(command[1])
            processTaskQueue()
        else:
            badProtocol(self, command)
    
    def setName(self, command):
        """set the associated computer name with the connection"""
        if len(command) == 2:
            print "setting client name to: " + command[1]
            self.clientName=command[1]
        else:
            badProtocol(self, command)

    #associate the protocol with the associated function.        
    protocolDic = {
    config.get('Protocol', "addToListTaskHandler"):addToListTaskHandler,
    config.get('Protocol', "taskCompleted"):taskCompleted,
    config.get('Protocol', "maxTasks"):maxTasks,
    config.get('Protocol', "setName"):setName,
    }

def archivematicaMCPServerListen():
    """ Start listening for archivematica clients to connect."""
    global application
    
    archivematicaService = archivematicaServices()
    archivematicaService.setServiceParent(application)
    xmlRPC = archivematicaXMLrpc()
    xmlRPCService = internet.TCPServer(config.getint('MCPServer', "MCPArchivematicaXMLPort"), server.Site(xmlRPC))
    xmlRPCService.setServiceParent(application)
    
    factory.protocol = archivematicaMCPServerProtocol
    factory.clients = []
   
    MCPServerService = internet.TCPServer(config.getint('MCPServer', "MCPArchivematicaServerPort"),factory, interface=config.get('MCPServer', "MCPArchivematicaServerInterface"))
    MCPServerService.setServiceParent(application)
    
   

def signal_handler(signalReceived, frame):
    print signalReceived, frame
    reactor.stop()
    threads = threading.enumerate()
    for thread in threads:
        if isinstance(thread, ThreadedNotifier):
            thread.stop()
            
class archivematicaServices(service.Service):
    def startService(self):
        print "Service Started"
        configs = loadConfigs()
        directoryWatchList = loadDirectoryWatchLlist(configs)
        service.Service.startService(self)
        
        
    def stopService(self):
        print "Stopping Service"
        service.Service.stopService(self)
        threads = threading.enumerate()
        for thread in threads:
            if isinstance(thread, ThreadedNotifier):
                thread.stop()

#if __name__ == '__main__':
#    signal.signal(signal.SIGTERM, signal_handler)
#    signal.signal(signal.SIGINT, signal_handler)

#configs = loadConfigs()
#directoryWatchList = loadDirectoryWatchLlist(configs)
archivematicaMCPServerListen()
    
