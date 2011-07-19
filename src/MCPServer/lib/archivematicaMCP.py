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
# It loads configurations from the database.
#




#clear; sudo -u archivematica /usr/bin/twistd --rundir=/home/joseph/archivematica/src/MCPServerSandbox/share/lib -l /tmp/mcpLog.html  --pidfile /tmp/mcppid.txt -ny /home/joseph/archivematica/src/MCPServerSandbox/share/lib/archivematicaMCP.py > /tmp/upstart2.html 2>&1; ps aux | grep 333

import watchDirectory
from jobChain import jobChain
from unitSIP import unitSIP
from unitFile import unitFile
from pyinotify import ThreadedNotifier

import signal
import os
import pyinotify
# from archivematicaReplacementDics import replacementDics 
# from MCPlogging import *
# from MCPloggingSQL import getUTCDate
import ConfigParser
# from mcpModules.modules import modulesClass
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
sys.path.append("/usr/lib/archivematica/archivematicaCommon")
import databaseInterface



config = ConfigParser.SafeConfigParser({'MCPArchivematicaServerInterface': ""})
config.read("/etc/archivematica/MCPServer/serverConfig.conf")
# archivematicaRD = replacementDics(config)


configs = []
jobsAwaitingApproval = []
jobsQueue = [] #jobs shouldn't remain here long (a few seconds max) before they are turned into tasks (jobs being processed)
jobsBeingProcessed = []
tasksQueue = []
tasksBeingProcessed = []
tasksLock = threading.Lock()
movingDirectoryLock = threading.Lock()
jobsLock = threading.Lock()
watchedDirectories = []
limitGearmanConnectionsSemaphore = threading.Semaphore(value=config.getint('Protocol', "limitGearmanConnections"))


    
def findOrCreateSipInDB(path):
    UUID = uuid.uuid4().__str__()
    separator = "', '"
    sql = """INSERT INTO SIP (sipUUID, currentPath)
        VALUES ('""" + UUID + separator + path + "');"
    databaseInterface.runSQL(sql)
    return UUID

def createUnitAndJobChain(path, config):
    print path, config
    unit = None
    if os.path.isdir(path):
        UUID = findOrCreateSipInDB(path)
        unit = unitSIP(path, UUID)
    elif os.path.isfile(path):
        return
        UUID = uuid.uuid4()
        unit = unitFile(path, UUID)
    else:
        return
    jobChain(unit, config[1])
    
    

def watchDirectories():
    sql = """SELECT watchedDirectoryPath, chain, onlyActOnDirectories FROM WatchedDirectories"""
    c, sqlLock = databaseInterface.querySQL(sql) 
    row = c.fetchone()
    while row != None:
        print row
        watchDirectory.archivematicaWatchDirectory(row[0],row, createUnitAndJobChain)
        row = c.fetchone()
    sqlLock.release()

#if __name__ == '__main__':
#    signal.signal(signal.SIGTERM, signal_handler)
#    signal.signal(signal.SIGINT, signal_handler)

#configs = loadConfigs()
#directoryWatchList = loadDirectoryWatchLlist(configs)
#archivematicaMCPServerListen()
if __name__ == '__main__':
    watchDirectories()