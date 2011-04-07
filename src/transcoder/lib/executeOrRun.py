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
# @subpackage transcoder
# @author Joseph Perry <joseph@artefactual.com>
# @version svn: $Id$

import subprocess
import shlex
import time
import uuid
import os
import sys

def launchSubProcess(command):
    #print "[Executing]", command
    #return 0,"stdouts out out out", "Error error out of cheese"

    interval = 0
    increaseInterval = 0.1
    maxInterval = 2
    maxProcessingTime = 88888888888888888888888888
    stdError = ""
    stdOut = ""
    
    try:
        p = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.PIPE)    
        while not p.poll():
            time.sleep(interval)
            so, se = p.communicate() 
            #append the output to stderror and stdout
            if so:
                stdOut = stdOut + so
            if se:
                stdError = stdError + se
            
            
            if interval < maxInterval:
                interval += increaseInterval
        
            if "processing time" > maxProcessingTime:
                #kill
                #exit code = 1000
                #append text to standard error.
                break
        retcode = p.returncode
    except OSError, ose:
        print >>sys.stderr, "Execution failed:", ose
        return -1, "Config Error!", ose.__str__()
    except :
        print  >>sys.stderr, "Execution failed:", command
        return -1, "Execution failed:", command
    return retcode, stdOut, stdError

        

def createAndRunScript(text):
    #output the text to a /tmp/ file
    scriptPath = "/tmp/" + uuid.uuid4().__str__()
    FILE = os.open(scriptPath, os.O_WRONLY | os.O_CREAT, 0770)
    os.write(FILE, text)
    os.close(FILE)
 
    #run it
    ret = launchSubProcess(scriptPath)
    
    #remove the temp file
    
    return ret 



def executeOrRun(type, text):
    if type == "command":
        return launchSubProcess(text)
    if type == "bashScript":
        text = "#!/bin/bash\n" + text
        return createAndRunScript(text)
    if type == "pythonScript":
        text = "#!/usr/bin/python\n" + text
        return createAndRunScript(text)
        