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
from pyinotify import WatchManager, Notifier, ThreadedNotifier, EventsCodes, ProcessEvent

archivmaticaVars = loadConfig("/home/joseph/sharedOnUServer/to build/archivematica/includes/archivematicaEtc/archivematicaConfig.conf")
mask = pyinotify.IN_CREATE | pyinotify.IN_MOVED_TO  #watched events
configs = []
#List of clients
#List of jobs to queue
#List of active jobs [UUID, folder to move when done.]

jobsAwaitingApproval = []
jobsQueue = []

def checkJobQueue():
    print "CHECING JOB QUEUE:"
    for job in jobsQueue:
        print "  " + job.config.identifier + "\t" + job.folder.__str__() + "\t" + job.step

class Job:
    def __init__(self, config, folder, step="exeCommand"):
        #    self.UUID = UUID()
        self.config = config
        self.step = step
        self.folder = folder
    

    

class watchFolder(ProcessEvent):
    config = None
    def __init__(self, config):
        self.config = config
    def process_IN_CREATE(self, event):
        print "Warning: %s was created. Was something copied into this folder?" %  os.path.join(event.path, event.name)
        
    def process_IN_MOVED_TO(self, event):      
        job = Job(self.config, os.path.join(event.path, event.name))
        if self.config.requiresUserApproval:
            #print "need to get user approval"
            jobsAwaitingApproval.append(job)
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


"""
def MCPclient()
        request info:
            give info
        approveJob:
            add job to que
            
def clientConnect(client UUID, client nice name, connect back info)
    getIP/connection info
    connect back to client.(to issues commands to client)
    return configDic
    #connection terminates
    
def processQue
    While(1):
        take que task
        send task to available client, with taskCompleted() ret, and JobUUID., relative path the files can be found (relative to shared folder.
        
def taskCompleted(jobUUID):
    make note in the logs
    if the 

"""

if __name__ == '__main__':
    configs = loadConfigs()
    folderWatchList = loadFolderWatchLlist(configs)
#    Start listening for client connections (new thread) 
#    Start listening for MCPclient Connections.
    
#    JOB UUID - operating on the entire SIP folder
#    Task - A job can contain many tasks- a task is per file
    
