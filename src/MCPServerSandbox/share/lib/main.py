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




#clear; sudo -u archivematica /usr/bin/twistd --rundir=/home/joseph/archivematica/src/MCPServerSandbox/share/lib -l /tmp/mcpLog.html  --pidfile /tmp/mcppid.txt -ny /home/joseph/archivematica/src/MCPServerSandbox/share/lib/main.py > /tmp/upstart2.html 2>&1; ps aux | grep 333
import databaseInterface
import watchDirectory
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
# archivematicaRD = replacementDics(config)


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


def createUnitAndJobChain(path, config):
    print path, config


def watchDirectories():
    sql = """SELECT watchedDirectoryPath, chain, onlyActOnDirectories FROM WatchedDirectories"""
    c, sqlLock = databaseInterface.querySQL(sql) 
    row = c.fetchone()
    while row != None:
        print row
        watchDirectory.archivematicaWatchDirectory(row[0],row, createUnitAndJobChain)
        row = c.fetchone()
    sqlLock.release()

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
        watchDirectories()
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