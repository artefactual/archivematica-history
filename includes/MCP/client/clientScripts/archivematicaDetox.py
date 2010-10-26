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
import os
from archivematicaFunctions import archivematicaRenameFile
from createXmlEventsAssist import createEvent 
from createXmlEventsAssist import createOutcomeInformation
from createXmlEventsAssist import createLinkingAgentIdentifier

DetoxDic={}
UUIDsDic={}
 
def loadFileUUIDsDic(logsDir):
    FileUUIDs_fh = open(logsDir+"FileUUIDs.log", "r")
 
    line = FileUUIDs_fh.readline()
    while line:
        detoxfiles = line.split(" -> ",1)
        if len(detoxfiles) > 1 :
            fileUUID = detoxfiles[0]
            fileName = detoxfiles[1]
            fileName = fileName.replace("\n", "", 1)
            UUIDsDic[fileName] = fileUUID
        line = FileUUIDs_fh.readline()
        
if __name__ == '__main__':
    """This prints the contents for an Archivematica Clamscan Event xml file"""
    objectsDirectory = sys.argv[1]
    logsDir =  sys.argv[2]
    date = sys.argv[3]

    loadFileUUIDsDic(logsDir)
    #def executeCommand(taskUUID, requiresOutputLock = "no", sInput = "", sOutput = "", sError = "", execute = "", arguments = "", serverConnection = None):
    command = "detox -rv \"" + objectsDirectory + "\""
    lines = []
    try:
        p = subprocess.Popen(shlex.split(command), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	
        p.wait()
        output = p.communicate()
        retcode = p.returncode
        
        #print output

        #it executes check for errors
        if retcode != 0:
            print >>sys.stderr, "error code:" + retcode.__str__()
            print output[1]# sError
            quit(retcode)
        lines = output[0].split("\n")
    except OSError, ose:
        print >>sys.stderr, "Execution failed:", ose
        quit(2)

    for line in lines:
        detoxfiles = line.split(" -> ")
        if len(detoxfiles) > 1 :
            oldfile = detoxfiles[0].split('\n',1)[0]
            newfile = detoxfiles[1]
            if os.path.isfile(newfile):
                oldfile = oldfile.replace(objectsDirectory, "objects", 1)
                newfile = newfile.replace(objectsDirectory, "objects", 1)
                fileUUID = UUIDsDic[oldfile]
                
                eIDValue = "detox-" + fileUUID
                createOutcomeInformation( eventOutcomeDetailNote = newfile)
                event = createEvent( eIDValue, "name cleanup", eventDateTime=date)
                archivematicaRenameFile(logsDir, fileUUID, newfile, event)

