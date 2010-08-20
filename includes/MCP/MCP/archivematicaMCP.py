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
from archivematicaLoadConfig import loadConfig
from modules.modules import modulesClass
import pyinotify
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

archivmaticaVars = loadConfig("/home/joseph/sharedOnUServer/to build/archivematica/includes/archivematicaEtc/archivematicaConfig.conf")
mask = pyinotify.IN_CREATE | pyinotify.IN_MOVED_TO  #watched events
configs = []
jobsAwaitingApproval = []
jobsQueue = []
jobsBeingProcessed = []
movingFolderLock = threading.Lock()

def checkJobQueue():
    print "CHECING JOB QUEUE:"
    for job in jobsQueue:
        print "  " + job.UUID.__str__() + "\t" + job.config.identifier + "\t" + job.folder.__str__() + "\t" + job.step

def assignTasks():
    print "not implemented yet"
    #compare tasks with nodes available.
        #if tasks can process node, proceed to do so.

class Job:
    def __init__(self, config, folder, step="exeCommand"):
        self.UUID = uuid.uuid4()
        self.config = config
        self.step = step
        self.folder = folder
        
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
    
    def lineReceived(self, line):
        "As soon as any data is received, write it back."
        print "read: " + line.__str__()
        self.write(line)

    def connectionMade(self):
        self.write("hello, client!")
    
    def write(self,line):
        self.transport.write(line)
        print "wrote: " + line.__str__()

def archivematicaMCPServerListen():
    factory = protocol.ServerFactory()
    factory.protocol = archivematicaMCPServerProtocol
    reactor.listenTCP(string.atoi(archivmaticaVars["MCPArchivematicaServerPort"]),factory)
    reactor.run()


if __name__ == '__main__':
    configs = loadConfigs()
    folderWatchList = loadFolderWatchLlist(configs)
    archivematicaMCPServerListen()
#    Start listening for client connections (new thread) 
#    Start listening for MCPclient Connections.

