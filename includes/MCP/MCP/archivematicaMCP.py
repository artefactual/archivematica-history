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

# @package Archivematica
# @subpackage Ingest
# @author Joseph Perry <joseph@artefactual.com>
# @version svn: $Id$

import os
import pyinotify
from archivematicaLoadConfig import loadConfig
from modules.modules import modulesClass
from pyinotify import WatchManager
from pyinotify import Notifier
from pyinotify import ThreadedNotifier
from pyinotify import EventsCodes
from pyinotify import ProcessEvent
import uuid
import threading
import string
import math
from twisted.internet import reactor
from twisted.internet import protocol as twistedProtocol
from twisted.protocols.basic import LineReceiver

archivmaticaVars = loadConfig("/home/joseph/archivematica/includes/archivematicaEtc/archivematicaConfig.conf")

#protocol = loadConfig(archivmaticaVars["archivematicaProtocol"])
protocol = loadConfig("/home/joseph/archivematica/includes/archivematicaEtc/archivematicaProtocol")

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
movingFolderLock = threading.Lock()
factory = twistedProtocol.ServerFactory()


def taskCompleted():
    print "not implemented"
    #lock to ensure not marking a job completed before it's fully created


def taskCompletedParser():
    print "not impletmented"

def checkJobQueue():
    print "CHECKING JOB QUEUE:"
    for job in jobsQueue:
        print "  " + job.UUID.__str__() + "\t" + job.config.identifier + "\t" + job.folder.__str__() + "\t" + job.step
        #lock it so it's not flagged as completed before it's fully created.
        job.createTasksForCurrentStep()  
    processTaskQueue()

def processTaskQueue():
    tasksLock.acquire()
    for task in tasksQueue:
        for client in factory.clients:
            client.clientLock.acquire()
            if client.currentThreads < client.maxThreads:
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
            client.clientLock.release()
    tasksLock.release()    
   

class Task():
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
        
        
        commandReplacementDic = { \
        "%jobUUID%": job.UUID.__str__(), \
        "%taskUUID%": self.UUID.__str__(), \
        "%relativeLocation%": target.replace(job.config.watchFolder, "%relativeSIPLocation%"), \
        "%relativeSIPLocation%": "%sharedPath%%processingFolder%" + job.UUID.__str__() + "/", \
        "%processingFolder%": job.config.processingFolder.replace(archivmaticaVars["sharedFolder"], "")\
        
        }
        
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
    def __init__(self, config, folder, step="exeCommand"):
        self.combinedRet = 0
        self.UUID = uuid.uuid4()
        self.config = config
        self.step = step
        self.folder = folder
        
        replacementDic = { \
        "%watchedFoldersPath%": archivmaticaVars["watchedFoldersPath"], \
        "%processingFolder%": archivmaticaVars["processingFolder"] \
        }
      
        #for each key replace all instances of the key in the strings
        for key in replacementDic.iterkeys():
          self.folder = self.folder.replace(key, replacementDic[key])
          self.config.processingFolder = self.config.processingFolder.replace(key, replacementDic[key])
        
    def queueJobStep(self):
        print "run Job"
    
    def jobStepCompleted(self):
        #if last step completed
        if False:
            #lock to ensure it doesn't start processing the next step, before the entire folder is moved.
            movingFolderLock.acquire()
            #move folder to next location, depending on fail status
            
            movingFolderLock.release()
            #remove this job from the jobsQueue
            jobsBeingProcessed.remove(self)
        else:
            print "Queue Next step"

    def createTasksForStep(self, command):
        ret = []
        if command.executeOnEachFile:
            #for every file in the folder, recursively, create a new task.
            if os.path.isdir(self.folder):
                for f in os.listdir(self.folder):
                    if os.path.isfile(os.path.join(self.folder, f)):
                        task = Task(self, os.path.join(self.folder, f).__str__(), command)
                        ret.append(task)
            else:
                print "error: tried to process file, not folder." + self.folder.__str__()
                jobsQueue.remove(self)
                
        else:
            if os.path.isdir(self.folder):
                ret.append(Task(self, self.folder, command))
            else:
                print "error: tried to process file, not folder." + self.folder.__str__()
                jobsQueue.remove(self)            

        return ret
            
    def createTasksForCurrentStep(self):
        if self.step == "exeCommand":
            if not self.config.exeCommand.skip:
                tasks = self.createTasksForStep(self.config.exeCommand)
                tasksLock.acquire()
                for task in tasks:
                    tasksQueue.append(task)
                tasksLock.release()
                processTaskQueue()
            else:
                self.step = "verificationCommand"
                createTasksForCurrentStep(self)
        elif job.step == "verificationCommand":
            if not self.config.verificationCommand.skip:
                tasks = createTasksForStep(self, self.config.verificationCommand)
                tasksLock.acquire()
                for task in tasks:
                    tasksQueue.append(task)
                tasksLock.release()
                processTaskQueue()
            else:
                if self.combinedRet:
                    self.step = "cleanupUnsuccessfulCommand"
                else:
                    self.step = "cleanupSuccessfulCommand"
                createTasksForCurrentStep(self)
        elif job.step == "cleanupSuccessfulCommand":
            if not self.config.cleanupSuccessfulCommand.skip:
                tasks = createTasksForStep(self, self.config.cleanupSuccessfulCommand)
                tasksLock.acquire()
                for task in tasks:
                    tasksQueue.append(task)
                tasksLock.release()
                processTaskQueue()
            else:
                print "NOT IMPLEMENTED YET - job done()"
        elif job.step == "cleanupUnsuccessfulCommand":
            if not self.config.cleanupUnsuccessfulCommand.skip:
                tasks = createTasksForStep(self, self.config.cleanupUnsuccessfulCommand)
                tasksLock.acquire()
                for task in tasks:
                    tasksQueue.append(task)
                tasksLock.release()
                processTaskQueue()
            else:
                print "NOT IMPLEMENTED YET - job done()"
        else:
            print "Job in bad step: " + self.step.__str__()

    def completed(self):
        jobsBeingProcessed.remove(self)
        if self.combinedRet:
            print "move it to error folder"
        else:
            print "move to completed folder"
        
        


class watchFolder(ProcessEvent):
    config = None
    def __init__(self, config):
        self.config = config
    def process_IN_CREATE(self, event):
        print "Warning: %s was created. Was something copied into this folder?" %  os.path.join(event.path, event.name)
        
    def process_IN_MOVED_TO(self, event):  
        #ensure no folders are in the process of moving. (so none will be in the middle of moving INTO this folder)
        movingFolderLock.acquire()
        movingFolderLock.release()    
        
        job = Job(self.config, os.path.join(event.path, event.name))
        if self.config.requiresUserApproval:
            #print "need to get user approval"
            jobsAwaitingApproval.append(job)
            #dashboard Alert - new job needing approval.
            
        else:
            jobsQueue.append(job)
            checkJobQueue()

def loadConfigs():
    configFiles = []
    for dirs, subDirs, files in os.walk(archivmaticaVars["moduleConfigDir"]):
        configFiles = files
        break

    for configFile in configFiles:
        if configFile.endswith(".xml"):
            configs.append(modulesClass(archivmaticaVars["moduleConfigDir"], configFile))
       
    #need to implement check for duplicate watch folders.
    
    return configs
        
def loadFolderWatchLlist(configs):
    for config in configs:
        wm = WatchManager()
        notifier = ThreadedNotifier(wm, watchFolder(config))
        wdd = wm.add_watch(config.watchFolder, mask, rec=False)
        notifier.start()

class archivematicaMCPServerProtocol(LineReceiver):
    """This is the archivematica protocol implemented"""
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
        print "connection made  -_-  " 
        print self
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
        
    protocolDic = {
    protocol["addToListTaskHandler"]:addToListTaskHandler,
    protocol["taskCompleted"]:taskCompleted,
    protocol["maxTasks"]:maxTasks,
    protocol["setName"]:setName
    }


def archivematicaMCPServerListen():
    factory.protocol = archivematicaMCPServerProtocol
    factory.clients = []
    reactor.listenTCP(string.atoi(archivmaticaVars["MCPArchivematicaServerPort"]),factory)
    reactor.run()


if __name__ == '__main__':
    configs = loadConfigs()
    folderWatchList = loadFolderWatchLlist(configs)
    archivematicaMCPServerListen()
#    Start listening for client connections (new thread) 
#    Start listening for MCPclient Connections.

