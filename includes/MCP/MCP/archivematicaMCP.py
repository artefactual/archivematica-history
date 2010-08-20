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
from twisted.internet import reactor
from twisted.internet import protocol
from twisted.protocols.basic import LineReceiver

archivmaticaVars = loadConfig("/home/joseph/archivematica/includes/archivematicaEtc/archivematicaConfig.conf")
#depends on OS whether you need one line or other. I think Events.Codes is older.
#mask = pyinotify.IN_CREATE | pyinotify.IN_MOVED_TO  #watched events
mask = EventsCodes.IN_CREATE | EventsCodes.IN_MOVED_TO  #watched events
configs = []
jobsAwaitingApproval = []
jobsQueue = [] #jobs shouldn't remain here long (a few seconds max) before they are turned into tasks
jobsBeingProcessed = []
tasksQueue = []
tasksLock =  = threading.Lock()
movingFolderLock = threading.Lock()
factory = protocol.ServerFactory()

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


def assignTasks():
    print "not implemented yet"
    #compare tasks with nodes available.
        #if tasks can process node, proceed to do so.

def processTaskQueue():
    tasksLock.aquire()
        for task in tasksQueue:
            print "not implemented yet"
    tasksLock.release()    
    

class Task():
    def __init__(job, target, command):
        self.UUID = uuid.uuid4()
        self.job = job
        self.command = command
        self.parameters = parameters
        self.description = command.descriptionWhileExecuting
        self.target = target
        
        commandReplacementDic = { \
        "%jobUUID%": job.UUID.__str__(), \
        "%taskUUID%": self.UUID.__str__(), \
        "%relativeLocation%": = "%sharedPath%%processingFolder%" + job.UUID.__str__() + "/", \
        "%processingFolder%":= job.config.processingFolder.replace(archivmaticaVars["sharedFolder"], "") \
        }
        
        #for each key replace all instances of the key in the command string
        for key in commandReplacementDic.iterkeys():
          #self.command = self.command.replace(key, replacementDic[key])
          self.description = self.description.replace(key, replacementDic[key])

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
    
    def createTasksForCurrentStep(self):
        if self.step == "exeCommand":
            if not self.job.config.exeCommand.skip:
                tasks = createTasksForStep(self, self.job.config.exeCommand)
                tasksLock.aquire()
                for task in tasks:
                    print "append tasks to queue"
                tasksLock.release()
                processTaskQueue()
            else:
                self.step = "verificationCommand"
                createTasksForCurrentStep(self)
        elif job.step == "verificationCommand":
            if not self.job.config.verificationCommand.skip:
                tasks = createTasksForStep(self, self.job.config.verificationCommand)
                tasksLock.aquire()
                for task in tasks:
                    print "append tasks to queue"
                tasksLock.release()
                processTaskQueue()
            else:
                if job.:
                    self.step = "cleanupUnsuccessfulCommand"
                else:
                    self.step = "cleanupSuccessfulCommand"
                createTasksForCurrentStep(self)
        elif job.step == "cleanupSuccessfulCommand":
            if not self.job.config.cleanupSuccessfulCommand.skip:
                tasks = createTasksForStep(self, self.job.config.cleanupSuccessfulCommand)
                tasksLock.aquire()
                for task in tasks:
                    print "append tasks to queue"
                tasksLock.release()
                processTaskQueue()
            else:
                print "NOT IMPLEMENTED YET - job done()"
        elif job.step == "cleanupUnsuccessfulCommand":
            if not self.job.config.cleanupUnsuccessfulCommand.skip:
                tasks = createTasksForStep(self, self.job.config.cleanupUnsuccessfulCommand)
                tasksLock.aquire()
                for task in tasks:
                    print "append tasks to queue"
                tasksLock.release()
                processTaskQueue()
            else:
                print "NOT IMPLEMENTED YET - job done()"

    def createTasksForStep(self, command):
        ret = []
        if command.executeOnEachFile:
            #for every file in the folder, recursively, create a new task.
            if os.path.isdir(self.folder):
                for f in os.listdir(self.folder):
                    if os.path.isfile(os.path.join(self.folder, f)):
                        ret.append(Task(self, os.path.join(self.folder, f), command))
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
    """This is just about the simplest possible protocol"""
    maxThreads = 0
    clientName = ""
    
    def lineReceived(self, line):
        "As soon as any data is received, write it back."
        print "read: " + line.__str__()
        self.write(line)

    def connectionMade(self):
        self.write("hello, client!\r\n")
        self.factory.clients.append(self)
        
    def connectionLost(self, reason):
        print "Lost a client!"
        self.factory.clients.remove(self)
        
    def write(self,line):
        self.transport.write(line + "\r\n")
        print "wrote: " + line.__str__()

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

