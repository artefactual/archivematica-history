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
import os
import pyinotify
import threading
from pyinotify import WatchManager
from pyinotify import Notifier
from pyinotify import ThreadedNotifier
from pyinotify import EventsCodes
from pyinotify import ProcessEvent

from archivematicaMCP import config
from archivematicaMCP import movingDirectoryLock

#depends on OS whether you need one line or other. I think Events.Codes is older.
mask = pyinotify.IN_CREATE | pyinotify.IN_MOVED_TO  #watched events
maskForCopied = pyinotify.IN_CREATE | pyinotify.IN_MODIFY
#mask = EventsCodes.IN_CREATE | EventsCodes.IN_MOVED_TO  #watched events

#Used to monitor directories copied to the MCP, to act when they are done copying.
class archivematicaWatchDirectoryTimer():
    def __init__(self, watchDirectoryProcessEvent, event, watchManager, path, delay=config.getint('MCPServer', "MCPWaitForCopyToCompleteSeconds")):
        self.watchDirectoryProcessEvent = watchDirectoryProcessEvent
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
        self.watchDirectoryProcessEvent.process_IN_MOVED_TO(self.event)

#Used to monitor directories copied to the MCP, to see when they are done copying.
class directoryCreated(ProcessEvent):
    """Determine which action to take based on the watch directory. """
    def __init__(self, watchDirectoryProcessEvent, event, watchManager, path, timer=None):
        self.timer = timer
        if self.timer == None:
            self.timer = archivematicaWatchDirectoryTimer(watchDirectoryProcessEvent, event, watchManager, path) # self to rm, wd and event to activate Processing.
            
    def process_IN_CREATE(self, event):
        self.process_IN_MODIFY(event)
        
    def process_IN_MODIFY(self, event):
        self.timer.resetDelay()


#This class holds the relation betwen watched directories, and their configs.
#This is a one to one relationship.
class watchDirectoryProcessEvent(ProcessEvent):
    """Determine which action to take based on the watch directory. """
    config = None
    def __init__(self, config, callBackFunction):
        self.config = config
        self.callBackFunction = callBackFunction
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
        path = os.path.join(event.path, event.name)
        if os.path.isdir(path):
            path = path + "/"    
        
        self.callBackFunction(path, self.config)
            

class archivematicaWatchDirectory:
    def __init__(self, directory, variables, callBackFunction):
        #directory = directory.replace("%watchDirectoryPath%", config.get('MCPServer', "watchDirectoryPath"), 1)
        if not os.path.isdir(directory):
            os.makedirs(directory)
        print "watching directory: ", directory
        wm = WatchManager()
        notifier = ThreadedNotifier(wm, watchDirectoryProcessEvent(variables, callBackFunction))
        wdd = wm.add_watch(directory, mask, rec=False)
        notifier.start()