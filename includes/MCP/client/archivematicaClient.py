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

archivmaticaVars = loadConfig("/home/joseph/archivematica/includes/archivematicaEtc/archivematicaConfig.conf")
supportedModules = loadConfig(archivmaticaVars["archivematicaClientModules"])
protocol = loadConfig(archivmaticaVars["archivematicaProtocol"])

def executeCommand(command,sInput="", sOutput="", sError="" ):
  #Replace replacement strings
    """  replacementDic = { \
      "%convertPath%": convertPath, \
      "%ffmpegPath%": ffmpegPath, \
      "%theoraPath%": theoraPath, \
      "%unoconvPath%": unoconvPath, \
      "%xenaPath%": xenaPath, \
      "%fileExtension%": fileExtension, \
      "%fileFullName%": fileFullName, \
      "%accessFileDirectory%": accesspath, \
      "%preservationFileDirectory%": fileDirectory, \
      "%fileDirectory%": fileDirectory,\
      "%fileTitle%": fileTitle, \
      "%normalizationScriptsDir%": normalizationScriptsDir, \
      "%accessFormat%": accessFormat[0].lower(), \
      "%preservationFormat%": preservationFormat[0].lower() }
      
      #for each key replace all instances of the key in the command string
      for key in replacementDic.iterkeys():
        command = command.replace ( key, replacementDic[key] )
    """

    #execute command
    try:
      if command != []:
        print >>sys.stderr, "processing: " + command.__str__()
        #retcode = subprocess.call( shlex.split(command) )
        p = subprocess.Popen(shlex.split(command), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print p.pid
        p.wait()
        ret = p.communicate(input=None)
        print "returned:"
        print ret
        retcode = p.returncode
        
        #it executes check for errors
        if retcode != 0:
          print >>sys.stderr, "error code:" + retcode.__str__()
        else:
          print >>sys.stderr, "processing completed"
          return 0
      else:
        print >>sys.stderr, "no conversion for type: " 
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
    def lineReceived(self, line):
        "As soon as any data is received, write it back."
        print "read: " + line.__str__()
    
    def write(self, line):
        self.transport.write( line + "\r\n")
        print "wrote: " + line.__str__()
    
    def clientConnectionLost(self, connector, reason):
        print "Connection lost - goodbye!"
        reactor.stop()

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
    print "above is a blocking call. This is never executed."
    while True:
        time.sleep(2)
        f.protocol.write("Keep alive!")
  
  
