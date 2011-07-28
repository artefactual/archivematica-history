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
from socket import gethostname
import gearman
import threading
import cPickle
sys.path.append("/usr/lib/archivematica/archivematicaCommon")
from executeOrRunSubProcess import executeOrRun

config = ConfigParser.SafeConfigParser({'MCPArchivematicaServerInterface': ""})
config.read("/etc/archivematica/MCPClient/clientConfig.conf")

replacementDic = { 
    "%sharedPath%":config.get('MCPClient', "sharedDirectoryMounted"), \
    "%clientScriptsDirectory%":config.get('MCPClient', "clientScriptsDirectory")
}
supportedModules = {}

def loadSupportedModules(file):    
    supportedModulesConfig = ConfigParser.RawConfigParser()
    supportedModulesConfig.read(file)
    for key, value in supportedModulesConfig.items('supportedCommands'):
        supportedModules[key] = value + " "
       
def executeCommand(gearman_worker, gearman_job):
    try:
        print gearman_worker
        print gearman_job
        print cPickle.loads(gearman_job.data)
        execute = gearman_job.task
        data = cPickle.loads(gearman_job.data)
        arguments = data["arguments"]
        sInput = ""
        
        if execute not in supportedModules:
            output = ["Error!", "Error! - Tried to run and unsupported command." ]
            exitCode = -1
            return cPickle.dumps({"exitCode" : exitCode, "stdOut": output[0], "stdError": output[1]})
        command = supportedModules[execute] 
      
        #Replace replacement strings
        for key in replacementDic.iterkeys():
            command = command.replace ( key, replacementDic[key] )
            arguments = arguments.replace ( key, replacementDic[key] )
        
        key = "%taskUUID%"
        value = gearman_job.unique.__str__()
        arguments = arguments.replace ( key, value )
        
        #execute command
    
        command += " " + arguments
        print >>sys.stderr, "processing: {" + gearman_job.unique + "}" + command.__str__()
        exitCode, stdOut, stdError = executeOrRun("command", command, sInput, printing=False)
        return cPickle.dumps({"exitCode" : exitCode, "stdOut": stdOut, "stdError": stdError})
    #catch OS errors
    except OSError, ose:
        print >>sys.stderr, "Execution failed:", ose
        output = ["Config Error!", ose.__str__() ]
        exitCode = 1
        return cPickle.dumps({"exitCode" : exitCode, "stdOut": output[0], "stdError": output[1]})
    except:
        print sys.exc_info().__str__()
        print "Unexpected error:", sys.exc_info()[0]
        output = ["", sys.exc_info().__str__()]
        return cPickle.dumps({"exitCode" : -1, "stdOut": output[0], "stdError": output[1]})
        

def startThread(threadNumber=0):
    gm_worker = gearman.GearmanWorker(['localhost:4730'])
    hostID = gethostname() + "_" + threadNumber.__str__() 
    gm_worker.set_client_id(hostID)
    for key in supportedModules.iterkeys():
        print "registering:", '"' + key + '"'
        gm_worker.register_task(key, executeCommand)
    gm_worker.work()
    

def startThreads(t):
    for i in range(t):
        t = threading.Thread(target=startThread, args=(i, ))
        t.start()

if __name__ == '__main__':
    loadSupportedModules(config.get('MCPClient', "archivematicaClientModules"))
    startThreads(1)
    tl = threading.Lock()
    tl.acquire()
    tl.acquire()
  
