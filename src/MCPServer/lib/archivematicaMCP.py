#!/usr/bin/python -OO

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
import threading
import watchDirectory
from jobChain import jobChain
from unitSIP import unitSIP
from unitDIP import unitDIP
from unitFile import unitFile
from unitTransfer import unitTransfer
from pyinotify import ThreadedNotifier
import transferD
import xmlRPCServer

import signal
import os
import pyinotify
# from archivematicaReplacementDics import replacementDics 
# from MCPlogging import *
# from MCPloggingSQL import getUTCDate
import ConfigParser
# from mcpModules.modules import modulesClass
import uuid
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
import databaseFunctions
from externals.singleInstance import singleinstance

global xmlRPCServerServer

config = ConfigParser.SafeConfigParser({'MCPArchivematicaServerInterface': ""})
config.read("/etc/archivematica/MCPServer/serverConfig.conf")

# archivematicaRD = replacementDics(config)

#time to sleep to allow db to be updated with the new location of a SIP
dbWaitSleep = 2

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
limitTaskThreads = config.getint('Protocol', "limitTaskThreads")
limitTaskThreadsSleep = config.getfloat('Protocol', "limitTaskThreadsSleep")
limitGearmanConnectionsSemaphore = threading.Semaphore(value=config.getint('Protocol', "limitGearmanConnections"))
reservedAsTaskProcessingThreads = config.getint('Protocol', "reservedAsTaskProcessingThreads")
debug = False
stopSignalReceived = False

def isUUID(uuid):
    split = uuid.split("-")
    if len(split) != 5 \
    or len(split[0]) != 8 \
    or len(split[1]) != 4 \
    or len(split[2]) != 4 \
    or len(split[3]) != 4 \
    or len(split[4]) != 12 :
        return False
    return True
    
def findOrCreateSipInDB(path, waitSleep=dbWaitSleep):
    UUID = ""
    path = path.replace(config.get('MCPServer', "sharedDirectory"), "%sharedPath%", 1)
    
    #find UUID on end of SIP path
    uuidLen = -36
    if isUUID(path[uuidLen-1:-1]):
        UUID = path[uuidLen-1:-1]

    
    if UUID == "":
        #Find it in the database
        sql = """SELECT sipUUID FROM SIPs WHERE currentPath = '""" + path + "';"
        #if waitSleep != 0:
            #time.sleep(waitSleep) #let db be updated by the microservice that moved it.
        c, sqlLock = databaseInterface.querySQL(sql) 
        row = c.fetchone()
        if not row:
            print "Not opening existing SIP:", UUID, "-", path
        while row != None:
            UUID = row[0]
            print "Opening existing SIP:", UUID, "-", path
            row = c.fetchone()
        sqlLock.release()
                
    
    #Create it
    if UUID == "":
        UUID = databaseFunctions.createSIP(path)
        print "DEBUG creating sip", path, UUID
    return UUID

def createUnitAndJobChain(path, config, terminate=False):
    print "createUnitAndJobChain", path, config
    unit = None
    if os.path.isdir(path):
        if config[3] == "SIP":
            UUID = findOrCreateSipInDB(path)
            unit = unitSIP(path, UUID)
        elif config[3] == "DIP":
            UUID = findOrCreateSipInDB(path)
            unit = unitDIP(path, UUID)
        elif config[3] == "Transfer":
            #UUID = findOrCreateSipInDB(path)
            unit = unitTransfer(path)
    elif os.path.isfile(path):
        return
        UUID = uuid.uuid4()
        unit = unitFile(path, UUID)
    else:
        return
    jobChain(unit, config[1])
    if terminate:
        exit(0)

def createUnitAndJobChainThreaded(path, config):
    #createUnitAndJobChain(path, config)
    #return
    try:   
        print "DEBGUG alert watch path: ", path
        t = threading.Thread(target=createUnitAndJobChain, args=(path, config), kwargs={"terminate":True})
        t.daemon = True
        while(limitTaskThreads <= threading.activeCount() + reservedAsTaskProcessingThreads ):
            if stopSignalReceived:
                print "Signal was received; stopping createUnitAndJobChainThreaded(path, config)"
                exit(0)
            print threading.activeCount().__str__()
            print "DEBUG createUnitAndJobChainThreaded waiting on thread count", threading.activeCount()
            time.sleep(4)
        t.start() 
    except Exception as inst:
            print "DEBUG EXCEPTION!"
            print type(inst)     # the exception instance
            print inst.args 

def watchDirectories():
    rows = []
    sql = """SELECT watchedDirectoryPath, chain, onlyActOnDirectories, description FROM WatchedDirectories LEFT OUTER JOIN WatchedDirectoriesExpectedTypes ON WatchedDirectories.expectedType = WatchedDirectoriesExpectedTypes.pk"""
    c, sqlLock = databaseInterface.querySQL(sql) 
    row = c.fetchone()
    while row != None:
        rows.append(row)
        row = c.fetchone()
    sqlLock.release()
    
    for row in rows:
        print row
        directory = row[0].replace("%watchDirectoryPath%", config.get('MCPServer', "watchDirectoryPath"), 1)
        if not os.path.isdir(directory):
            os.makedirs(directory)
        for item in os.listdir(directory):
            if item == ".svn":
                continue
            path = os.path.join(directory, item)
            if os.path.isdir(path):
                path = path + "/"
            createUnitAndJobChain(path, row)
        watchDirectory.archivematicaWatchDirectory(directory,row, createUnitAndJobChainThreaded)
    
#if __name__ == '__main__':
#    signal.signal(signal.SIGTERM, signal_handler)
#    signal.signal(signal.SIGINT, signal_handler)

#configs = loadConfigs()
#directoryWatchList = loadDirectoryWatchLlist(configs)
#archivematicaMCPServerListen()

    
def signal_handler(signalReceived, frame):
    print signalReceived, frame
    global stopSignalReceived 
    stopSignalReceived = True
    threads = threading.enumerate()
    for thread in threads:
        if False and isinstance(thread, threading.Thread):
            try:
                print "not stopping: ", type(thread), thread
            except Exception as inst:
                print "DEBUG EXCEPTION!"
                print type(inst)     # the exception instance
                print inst.args
        elif isinstance(thread, pyinotify.ThreadedNotifier):
            print "stopping: ", type(thread), thread
            try:
                thread.stop()
            except Exception as inst:
                print "DEBUG EXCEPTION!"
                print type(inst)     # the exception instance
                print inst.args 
        else:
            print "not stopping: ", type(thread), thread
    sys.stdout.flush()
    sys.stderr.flush()
    sys.exit(0)
    exit(0)

def debugMonitor():
    while True:
        print "<DEBUG>"
        print "\tThreadCount: ", threading.activeCount()
        print "\tDate Time: ", databaseInterface.getUTCDate()
        if databaseInterface.sqlLock.acquire(False):
            databaseInterface.sqlLock.release()
            print "\tSQL Lock: Unlocked"
        else:
            print "\tSQL Lock: Locked"
        print "</DEBUG>"
        time.sleep(10)
        
def flushOutputs():
    while True:
        sys.stdout.flush()
        sys.stderr.flush()
        time.sleep(5)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    si = singleinstance(config.get('MCPServer', "singleInstancePIDFile"))
    if si.alreadyrunning():
        print >>sys.stderr, "Another instance is already running. Exiting."
        sys.exit(1)
    elif False: #testing single instance stuff
        while 1:
            print "psudo run"
            time.sleep(3)
        
    if True:
        import getpass
        print "user: ", getpass.getuser()
        os.setuid(333)
    if True:
        t = threading.Thread(target=debugMonitor)
        t.daemon = True
        t.start() 
    if True:
        t = threading.Thread(target=flushOutputs)
        t.daemon = True
        t.start() 
    
    watchDirectories()    
    transferD.main()
    xmlRPCServer.startXMLRPCServer()
    