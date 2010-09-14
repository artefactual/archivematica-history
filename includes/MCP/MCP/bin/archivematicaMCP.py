#!/usr/bin/python

# This file is part of Archivematica.
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

# --- This is the MCP (master control program) ---
# The intention of this program is to provide a cetralized automated distributed system for performing an arbitrary set of tasks on a directory.
# Distributed in that the work can be performed on more than one physical computer symultaineously.
# Centralized in that there is one centre point for configuring flow through the system.
# Automated in that the tasks performed will be based on the config files and istantiated for each of the targets.
#
# It loads configurations from the XML files.
# These files contain:
# -The associated watch directory
# -A set of commands to run on the files within that directory.
# -The place to move the directory to once it has been processed.
#
# When a directory is placed within a a watch directory, it generates an event.
# The event creates an associated Job.
# The job is an instance of one of the config files (depending on which watch directory geneated the event).
# The job will have a number of steps, for each of the commands.
# The commands will be istanciated into tasks for each of the files within the watch directory of the event, or just one task for the directory (depending on the config).


# @package Archivematica
# @subpackage Ingest
# @author Joseph Perry <joseph@artefactual.com>
# @version svn: $Id$

import os
import pyinotify
from archivematicaReplacementDics import replacementDics 
from archivematicaLoadConfig import loadConfig
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
import time
from twisted.internet import reactor
from twisted.internet import protocol as twistedProtocol
from twisted.protocols.basic import LineReceiver


archivematicaVars = loadConfig()

protocol = loadConfig(archivematicaVars["archivematicaProtocol"])
archivematicaRD = replacementDics(archivematicaVars)

#depends on OS whether you need one line or other. I think Events.Codes is older.
mask = pyinotify.IN_CREATE | pyinotify.IN_MOVED_TO  #watched events
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
jobsLock =  threading.Lock()

def checkJobQueue():
    """Creates Tasks for new auto approved jobs, or just approved jobs."""
    jobsLock.acquire()
    for job in jobsQueue:
        #print "  " + job.UUID.__str__() + "\t" + job.config.identifier + "\t" + job.directory.__str__() + "\t" + job.step
        directory = job.config.processingDirectory + job.UUID.__str__() + "/"
        print "moving: " + job.directory + "\t to: \t" + directory
        os.makedirs(directory, mode=0777)
        os.rename(job.directory, directory + job.directory.split("/")[-1])
        tasksCreated = job.createTasksForCurrentStep() 
        jobsQueue.remove(job)
        if tasksCreated:
            jobsBeingProcessed.append(job) 
    jobsLock.release()
    processTaskQueue()

def processTaskQueue():
    """Attempts to assign tasks to clients."""
    tasksLock.acquire()
    for task in tasksQueue:
        for client in factory.clients:
            client.clientLock.acquire()
            if client.currentThreads < client.maxThreads:
                for supportedCommand in client.supportedCommands:
                    if supportedCommand == task.execute:
		                tasksQueue.remove(task)
		                tasksBeingProcessed.append(task)
		                send = protocol["performTask"]
		                send += protocol["delimiter"] 
		                send += task.UUID.__str__() 
		                send += protocol["delimiter"] 
		                if task.standardIn:
		                    send += task.standardIn.__str__() 
		                send += protocol["delimiter"] 
		                if task.standardOut:
		                    send += task.standardOut.__str__()
		                send += protocol["delimiter"] 
		                if task.standardError:
		                    send += task.standardError.__str__() 
		                send += protocol["delimiter"]  
		                send += task.execute.__str__()
		                send += protocol["delimiter"]  
		                send += task.arguments.__str__() 
		                reactor.callFromThread(client.write, send)
		                break
            client.clientLock.release()
    tasksLock.release()    
   

class Task():
    """A task is an instance of a command, operating on an entire directory, or a single file."""
    def __init__(self, job, target, command):
        self.UUID = uuid.uuid4()
        self.job = job
        self.command = command
        self.execute = command.execute
        self.arguments = command.arguments
        self.description = command.descriptionWhileExecuting
        self.target = target
        self.standardIn = command.standardIn
        self.standardOut = command.standardOut
        self.standardError = command.standardError
        
        
        commandReplacementDic = archivematicaRD.commandReplacementDic(self, job, target, command)
        
        #for each key replace all instances of the key in the command string
        for key in commandReplacementDic.iterkeys():
            if self.description:
                self.description = self.description.replace(key, commandReplacementDic[key])
            if self.execute:
                self.execute = self.execute.replace(key, commandReplacementDic[key])
            if self.arguments:
                self.arguments = self.arguments.replace(key, commandReplacementDic[key])
            if self.standardIn:
                self.standardIn = self.standardIn.replace(key, commandReplacementDic[key])
            if self.standardOut:
                self.standardOut = self.standardOut.replace(key, commandReplacementDic[key])
            if self.standardError:
                self.standardError = self.standardError.replace(key, commandReplacementDic[key])

    def completed(self, returned):
        """When a task is completed, check to see if it was the last task for the job to be completed (job completed)."""
        tasksLock.acquire()
        jobStepDone = True
        tasksBeingProcessed.remove(self)
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
        tasksLock.release()
        if jobStepDone:
            self.job.jobStepCompleted()

class Job:
    """A job is an instance of a file in a watch directory (from a config file)."""
    def __init__(self, config, directory, step="exeCommand"):
        self.combinedRet = 0
        self.UUID = uuid.uuid4()
        self.config = config
        self.step = step
        self.directory = directory
        
        replacementDic = archivematicaRD.jobReplacementDic(self, config, directory, step)
      
        #for each key replace all instances of the key in the strings
        for key in replacementDic.iterkeys():
            self.directory = self.directory.replace(key, replacementDic[key])
            self.config.processingDirectory = self.config.processingDirectory.replace(key, replacementDic[key])
            self.config.successDirectory = self.config.successDirectory.replace(key, replacementDic[key])
            self.config.failureDirectory = self.config.failureDirectory.replace(key, replacementDic[key])

   
    def jobStepCompleted(self):
        """When a job step is completed, move to the next step, or if the job is completed, move everthing in the directory to the output directory. """
        #if last step completed
        if self.step == "cleanupSuccessfulCommand"\
        or self.step == "cleanupUnsuccessfulCommand":
            #time.sleep(5) - attempt to fix Resource busy
            #lock to ensure it doesn't start processing the next step, before the entire directory is moved.
            movingDirectoryLock.acquire()
            #move directory to next location, depending on fail status
            destination = ""
            if self.step == "cleanupSuccessfulCommand":
                destination = self.config.successDirectory
            else: #"cleanupUnsuccessfulCommand"
                destination = self.config.failureDirectory
            directory = self.config.processingDirectory + self.UUID.__str__() + "/"
            for f in os.listdir(directory):
                print "rename: " + os.path.join(directory, f) + " TO: " + os.path.join(destination, f)
                os.rename( os.path.join(directory, f), os.path.join(destination, f) )
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
            
    def createTasksForStep(self, command):
        """Creates the tasks for the given command"""
        ret = []
        directory = self.config.processingDirectory + self.UUID.__str__() + "/" + os.path.basename(self.directory) + "/"
        if command.filterDir:
            directory += command.filterSubDir   
        if command.executeOnEachFile:
            ret = self.createTasksForStepInDirectory(command, directory)
        else:
            if os.path.isdir(directory):
                ret.append(Task(self, directory, command))
            else:
                print "error: tried to process file, not directory." + self.directory.__str__()
                jobsQueue.remove(self)
        return ret
    
    def createTasksForStepInDirectory(self, command, directory):
        """for every file in the directory, recursively, create a new task."""
        ret = []
        print "Creating tasks for directory: " + directory
        if os.path.isdir(directory):
            for f in os.listdir(directory):
                print f
                if os.path.isdir(os.path.join(directory, f)):
                    sub = self.createTasksForStepInDirectory(command, os.path.join(directory, f))
                    for task in sub:
                        ret.append(task)
                if command.filterFileEnd or command.filterFileStart:
                    if os.path.isfile(os.path.join(directory, f)):
                        if filterFileEnd and filterFileStart \
                        and f.__str__().endswith(filterFileEnd) \
                        and f.__str__().startswith(filterFileStart):
                            task = Task(self, os.path.join(directory, f).__str__(), command)
                            ret.append(task)
                        elif filterFileEnd and f.__str__().endswith(filterFileEnd):
                            task = Task(self, os.path.join(directory, f).__str__(), command)
                            ret.append(task)
                        elif filterFileStart and f.__str__().startswith(filterFileStart):
                            task = Task(self, os.path.join(directory, f).__str__(), command)
                            ret.append(task)
                else:
                    if os.path.isfile(os.path.join(directory, f)):
                        task = Task(self, os.path.join(directory, f).__str__(), command)
                        ret.append(task)
        else:
            print "error: tried to process file, not directory." + self.directory.__str__()
            jobsQueue.remove(self)
        return ret
            
    def createTasksForCurrentStep(self):
        """Determin the current step, and if it is to be skipped. 
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

class watchDirectory(ProcessEvent):
    """Determin which action to take based on the watch directory. """
    config = None
    def __init__(self, config):
        self.config = config
    def process_IN_CREATE(self, event):
        """ Traditionally, archivematica does not support copying to watch directorys."""
        print "Warning: %s was created. Was something copied into this directory?" %  os.path.join(event.path, event.name)
        
    def process_IN_MOVED_TO(self, event):  
        """Create a Job based on what was moved into the directory and process it."""
        #ensure no directorys are in the process of moving. (so none will be in the middle of moving INTO this directory)
        movingDirectoryLock.acquire()
        movingDirectoryLock.release()    
        
        job = Job(self.config, os.path.join(event.path, event.name))
        if self.config.requiresUserApproval:
            #print "need to get user approval"
            jobsAwaitingApproval.append(job)
            #dashboard Alert - new job needing approval.
            
        else:
            jobsQueue.append(job)
            checkJobQueue()

def loadConfigs():
    """Loads the XML config files, with the directorys to watch, and the associated commmands"""
    configFiles = []
    for dirs, subDirs, files in os.walk(archivematicaVars["moduleConfigDir"]):
        configFiles = files
        break

    for configFile in configFiles:
        if configFile.endswith(".xml"):
            configs.append(modulesClass(archivematicaVars["moduleConfigDir"], configFile))
       
    #need to implement check for duplicate watch directorys.
    
    return configs
        
def loadDirectoryWatchLlist(configs):
    """Start watching all the watch directorys defined in the configs. """
    replacementDic = archivematicaRD.watchFolderRepacementDic()
    for config in configs:
        wm = WatchManager()
                #for each key replace all instances of the key in the strings
        for key in replacementDic.iterkeys():
          config.watchDirectory = config.watchDirectory.replace(key, replacementDic[key])
        notifier = ThreadedNotifier(wm, watchDirectory(config))
        wdd = wm.add_watch(config.watchDirectory, mask, rec=False)
        notifier.start()

class archivematicaMCPServerProtocol(LineReceiver):
    """This is the MCP protocol implemented"""
    maxThreads = 0
    currentThreads = 0
    clientName = ""
    supportedCommands = []
    clientLock = threading.Lock()

    def badProtocol(self, command):
        """The client sent a command this server cannot interpret."""
        print "read(bad protocol): " + command.__str__()
   
    def lineReceived(self, line):
        "As soon as any data is received, write it back."
        command = line.split(protocol["delimiter"])
        if len(command):
            self.protocolDic.get(command[0], archivematicaMCPServerProtocol.badProtocol)(self, command)
        else:
            badProtocol(self, command)

    def connectionMade(self):
        self.write("hello, client!")
        self.factory.clients.append(self)
        
    def connectionLost(self, reason):
        print "Lost client: " + self.clientName
        self.factory.clients.remove(self)
        
    def write(self,line):
        self.transport.write(line + "\r\n")
        print "\twrote: " + line.__str__()
    
    def addToListTaskHandler(self, command):
        """inform the server the client is capable of running a certain type of task"""
        if len(command) == 2:
            self.supportedCommands.append(command[1])
        else:
            badProtocol(self, command)
    
    def taskCompleted(self, command):
        """inform the server a task is completed""" 
        if len(command) == 3:
            self.currentThreads = self.currentThreads - 1
            
            #might be a potential DOS attack.
            ret = string.atoi(command[2])
            
            taskUUID=command[1]
            theTask = None
            for task in tasksBeingProcessed:
                if task.UUID.__str__() == taskUUID:
                    theTask = task
                    break
            if theTask:
                theTask.completed(ret)
                print "task completed: " + theTask.UUID.__str__()
            else:
                self.badProtocol(command)
        else:
            self.badProtocol(command)
    
    def maxTasks(self, command):
        """#tell the server how many threads this client will run""" 
        if len(command) == 2:
            #this may require further checking. So people don't try "TWO" instead of 2
            #self.maxThreads = int(command[1])
            print self.clientName + "-setting max threads to: " + command[1]
            self.maxThreads = string.atoi(command[1])
        else:
            badProtocol(self, command)
    
    def setName(self, command):
        """set the associated computer name with the connection"""
        if len(command) == 2:
            print "setting client name to: " + command[1]
            self.clientName=command[1]
        else:
            badProtocol(self, command)

    #associate the protocol with the associated funciton.        
    protocolDic = {
    protocol["addToListTaskHandler"]:addToListTaskHandler,
    protocol["taskCompleted"]:taskCompleted,
    protocol["maxTasks"]:maxTasks,
    protocol["setName"]:setName
    }


def archivematicaMCPServerListen():
    """ Start listening for archivematica clients to connect."""
    factory.protocol = archivematicaMCPServerProtocol
    factory.clients = []
    reactor.listenTCP(string.atoi(archivematicaVars["MCPArchivematicaServerPort"]),factory)
    reactor.run()
    print "The reactor stopped!!!"

if __name__ == '__main__':
    configs = loadConfigs()
    directoryWatchList = loadDirectoryWatchLlist(configs)
    archivematicaMCPServerListen()
#    Start listening for client connections (new thread) 
#    Start listening for MCPclient Connections.

