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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Archivematica.  If not, see <http://www.gnu.org/licenses/>.

# @package Archivematica
# @subpackage Ingest
# @author Joseph Perry <joseph@artefactual.com>
# @version svn: $Id$

import sys
import shlex
import subprocess
import time
from archivematicaLoadConfig import loadConfig
from twisted.internet import reactor
from twisted.internet import protocol as twistedProtocol
from twisted.protocols.basic import LineReceiver

archivmaticaVars = loadConfig()
supportedModules = loadConfig(archivmaticaVars["archivematicaClientModules"])
protocol = loadConfig(archivmaticaVars["archivematicaProtocol"])

def writeToFile(output, fileName):
    if fileName and output:
        print "writing to: " + fileName
        try:
            f = open(fileName, 'a')
            f.write(output.__str__())
            f.close()
        except OSError, ose:
            print >>sys.stderr, "output Error", ose
    else:
        print "No output file specified"

def executeCommand(taskUUID, sInput = "", sOutput = "", sError = "", execute = "", arguments = ""):
    #Replace replacement strings
    command = supportedModules[execute] 
    replacementDic = { 
        "%sharedPath%":archivmaticaVars["sharedDirectory"], \
        "%clientScriptsDirectory%":archivmaticaVars["clientScriptsDirectory"]
    }  
    #for each key replace all instances of the key in the command string
    for key in replacementDic.iterkeys():
        command = command.replace ( key, replacementDic[key] )
        arguments = arguments.replace ( key, replacementDic[key] )
        sInput = sInput.replace ( key, replacementDic[key] )
        sOutput = sOutput.replace ( key, replacementDic[key] )
        sError = sError.replace ( key, replacementDic[key] )
    #execute command
    try:
      if execute != "" and command != "":
        command += " " + arguments
        print >>sys.stderr, "processing: " + command.__str__()
        #retcode = subprocess.call( shlex.split(command) )
        p = subprocess.Popen(shlex.split(command), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	
        p.wait()
        output = p.communicate(input=sInput)
        print "returned:"
        print output
        
        writeToFile(output[0], sOutput)
        writeToFile(output[1], sError)
        
        retcode = p.returncode
        
        #it executes check for errors
        if retcode != 0:
          print >>sys.stderr, "error code:" + retcode.__str__()
          return retcode
        else:
          print >>sys.stderr, "processing completed"
          return 0
      else:
        print >>sys.stderr, "server tried to run a blank command: " 
        return 1
    #catch OS errors
    except OSError, ose:
      print >>sys.stderr, "Execution failed:", ose
      return 1

class archivematicaMCPClientProtocol(LineReceiver):
    """This is just about the simplest possible protocol"""

    def connectionMade(self):
        self.write(protocol["setName"] + protocol["delimiter"] + archivmaticaVars["clientName"])
        for module in supportedModules:
            self.write(protocol["addToListTaskHandler"] + protocol["delimiter"] + module)
        self.write(protocol["maxTasks"] + protocol["delimiter"] + archivmaticaVars["maxThreads"])
    
    def write(self, line):
        self.transport.write( line + "\r\n")
        print "wrote: " + line.__str__()
    
    def clientConnectionLost(self, connector, reason):
        print "Connection lost - goodbye!"
        reactor.stop()
        
    def badProtocol(self, command):
        """The client sent a command this server cannot interpret."""
        print "read(bad protocol): " + command.__str__()
   
    def lineReceived(self, line):
        "As soon as any data is received, write it back."
        command = line.split(protocol["delimiter"])
        if len(command):
            self.protocolDic.get(command[0], archivematicaMCPClientProtocol.badProtocol)(self, command)
        else:
            badProtocol(self, command)

    def sendTaskResult(self, command, result):
        if len(command) > 1:
            send = protocol["taskCompleted"]
            send += protocol["delimiter"]
            send += command[1]
            send += protocol["delimiter"]
            send += result.__str__()
            self.write(send)
        else:
            print >>sys.stderr, "this should never be executed."   
    
    def performTask(self, command):
        if len(command) == 7:
            ret = executeCommand(command[1], command[2], command[3], command[4], command[5], command[6])
            self.sendTaskResult(command, ret)
        else:
            badProtocol(self, command)
            self.sendTaskResult(command, 1)
            
    protocolDic = {
    protocol["performTask"]:performTask
    }

class archivematicaMCPClientProtocolFactory(twistedProtocol.ClientFactory):
    protocol = archivematicaMCPClientProtocol

    def clientConnectionFailed(self, connector, reason):
        print "Connection failed - goodbye!"
        reactor.stop()
    
    def clientConnectionLost(self, connector, reason):
        print "Connection lost - goodbye!"
        reactor.stop()


# this only runs if the module was *not* imported
if __name__ == '__main__':
    f = archivematicaMCPClientProtocolFactory()
    t = reactor.connectTCP("localhost", 8002, f)
    reactor.run()
    print "above is a blocking call. This is executed once client disconnects"
  
  
