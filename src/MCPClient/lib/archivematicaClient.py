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
# @subpackage Ingest
# @author Joseph Perry <joseph@artefactual.com>
# @version svn: $Id$

#~DOC~
#
# --- This is the MCP Client---
#It connects to the MCP server, and informs the server of the tasks it can perform.
#The server can send a command (matching one of the tasks) for the client to perform.
#The client will perform that task, and return the exit code and output to the server.
import sys
import shlex
import subprocess
import time
import threading
import string
import ConfigParser
from archivematicaLoadConfig import loadConfig
from twisted.internet import reactor
from twisted.internet import protocol as twistedProtocol
from twisted.protocols.basic import LineReceiver
from socket import gethostname
from twisted.application import service
from twisted.application import internet
sys.path.append("/usr/lib/archivematica/archivematicaCommon")
from executeOrRun import executeOrRun

config = ConfigParser.SafeConfigParser({'MCPArchivematicaServerInterface': ""})
config.read("/etc/archivematica/MCPClient/clientConfig.conf")

supportedModules = {}

def loadSupportedModules(file):    
    supportedModulesConfig = ConfigParser.RawConfigParser()
    supportedModulesConfig.read(file)
    for key, value in supportedModulesConfig.items('supportedCommands'):
        supportedModules[key] = value + " "
       
def executeCommand(taskUUID, sInput = "", execute = "", arguments = "", serverConnection = None):  
    #Replace replacement strings
    if execute not in supportedModules:
        return -5, "", "Tried To Run An Unsupported Command"
    command = supportedModules[execute] 
    replacementDic = { 
        "%sharedPath%":config.get('MCPClient', "sharedDirectoryMounted"), \
        "%clientScriptsDirectory%":config.get('MCPClient', "clientScriptsDirectory")
    }  
    #for each key replace all instances of the key in the command string
    for key in replacementDic.iterkeys():
        command = command.replace ( key, replacementDic[key] )
        arguments = arguments.replace ( key, replacementDic[key] )
        sInput = sInput.replace ( key, replacementDic[key] )
    #execute command
    try:
        if execute != "" and command != "":
            command += " " + arguments
            print >>sys.stderr, "processing: {" + taskUUID + "}" + command.__str__()
            return executeOrRun("command", command, sInput, printing=False)
        else:
            print >>sys.stderr, "server tried to run a blank command! " 
            return 1, "", "server tried to run a blank command! "
    #catch OS errors
    except OSError, ose:
        print >>sys.stderr, "Execution failed:", ose
        output = ["Config Error!", ose.__str__() ]
        retcode = 1
        return retcode, output[0], output[1]

class archivematicaMCPClientProtocol(LineReceiver):
    """Archivematica Client Protocol"""
    sendLock = threading.Lock()
    
    def connectionMade(self):
        self.write(config.get('Protocol', "setName") + config.get('Protocol', "delimiter") + gethostname())
        for module in supportedModules:
            self.write(config.get('Protocol', "addToListTaskHandler") + config.get('Protocol', "delimiter") + module)
        self.write(config.get('Protocol', "maxTasks") + config.get('Protocol', "delimiter") + config.get('MCPClient', "maxThreads"))
    
    def write(self,line):
        self.sendLock.acquire() 
        reactor.callFromThread(self.transport.write, line + "\r\n")
        self.sendLock.release()
        print "\twrote: " + line.__str__()
    
    def clientConnectionLost(self, connector, reason):
        print "Connection lost - goodbye!"
        reactor.stop()
        
    def badProtocol(self, command):
        """The client sent a command this server cannot interpret."""
        print "read(bad protocol): " + command.__str__()
   
    def lineReceived(self, line):
        "As soon as any data is received, write it back."
        command = line.split(config.get('Protocol', "delimiter"))
        if len(command):
            t = threading.Thread(target=self.protocolDic.get(command[0], archivematicaMCPClientProtocol.badProtocol),\
            args=(self, command, ))
            t.start()
        else:
            badProtocol(self, command)

    def sendTaskResult(self, command, result):
        if len(command) > 1:
            send = config.get('Protocol', "taskCompleted")
            send += config.get('Protocol', "delimiter")
            send += command[1]
            send += config.get('Protocol', "delimiter")
            send += result[0].__str__()
            send += config.get('Protocol', "delimiter")
            send += result[1].__str__()
            send += config.get('Protocol', "delimiter")
            send += result[2].__str__()
            self.write(send)
        else:
            print >>sys.stderr, "this should never be executed."   
    
    def performTask(self, command):
        if len(command) == 5:
            ret = executeCommand(command[1], command[2], command[3], command[4], self)
            print "returned: {" + command[1] + "}" + ret.__str__()
            self.sendTaskResult(command, ret)
                
        else:
            badProtocol(self, command)
            self.sendTaskResult(command, 1)

    def keepAlive(self, command):    
        if len(command) == 1:
            print "Got keep alive. Keeping connection open."
        else:
            badProtocol(self, command)

    protocolDic = {
    config.get('Protocol', "performTask"):performTask, \
    config.get('Protocol', "keepAlive"):keepAlive
    }

class archivematicaMCPClientProtocolFactory(twistedProtocol.ClientFactory):
    protocol = archivematicaMCPClientProtocol

    def clientConnectionFailed(self, connector, reason):
        print "Connection failed - goodbye!"
        if reactor._started:
            reactor.stop()
    
    def clientConnectionLost(self, connector, reason):
        print "Connection lost - goodbye!"
        if reactor._started:
            reactor.stop()


#if __name__ == '__main__':
loadSupportedModules(config.get('MCPClient', "archivematicaClientModules"))
application = service.Application("archivematicaMCPClient")
f = archivematicaMCPClientProtocolFactory()
MCPClientService = internet.TCPClient(config.get('MCPClient', "MCPArchivematicaServer"), string.atoi(config.get('MCPClient', "MCPArchivematicaServerPort")), f)
MCPClientService.setServiceParent(application)

print "Connecting To: " + config.get('MCPClient', "MCPArchivematicaServer") + ":" + config.get('MCPClient', "MCPArchivematicaServerPort")
  
  
