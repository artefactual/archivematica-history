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
import sys
import shlex
import subprocess
import os
from archivematicaFunctions import archivematicaRenameFile
from createXmlEventsAssist import createEvent 
from createXmlEventsAssist import createOutcomeInformation
from createXmlEventsAssist import createLinkingAgentIdentifier
sys.path.append("/usr/lib/archivematica/archivematicaCommon")
from archivematicaMCPFileUUID import findUUIDFromFileUUIDxml

#import lxml.etree as etree

DetoxDic={}
UUIDsDic={}
 
def loadFileUUIDsDic(logsDir, objectsDirectory):
    FileUUIDs_fh = open(logsDir+"FileUUIDs.log", "r")
 
    line = FileUUIDs_fh.readline()
    while line:
        detoxfiles = line.split("  ->  ",1)
        if len(detoxfiles) > 1 :
            fileUUID = detoxfiles[0]
            fileName = detoxfiles[1]
            fileName = fileName.replace("\n", "", 1)
            UUIDsDic[fileName] = fileUUID
        line = FileUUIDs_fh.readline()
    
    for w in os.walk(objectsDirectory):
        op, directories, files = w
        for p in files:
            path = os.path.join(op, p)
            path = path.__str__().replace(objectsDirectory, "objects/")
            if not path in UUIDsDic:
                UUIDsDic[path] = findUUIDFromFileUUIDxml(logsDir+"FileUUIDs.log", path, logsDir+"fileMeta/", updateSIPUUIDfile=True)
        
if __name__ == '__main__':
    """This prints the contents for an Archivematica Clamscan Event xml file"""
    objectsDirectory = sys.argv[1]
    logsDir =  sys.argv[2]
    date = sys.argv[3]
    taskUUID = sys.argv[4]

    loadFileUUIDsDic(logsDir, objectsDirectory)
    #def executeCommand(taskUUID, requiresOutputLock = "no", sInput = "", sOutput = "", sError = "", execute = "", arguments = "", serverConnection = None):
    command = "sanitizeNames \"" + objectsDirectory + "\""
    lines = []
    commandVersion = "sanitizeNames -V"
    version = ""
    try:
        p = subprocess.Popen(shlex.split(command), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	
        #p.wait()
        output = p.communicate()
        retcode = p.returncode
        
        #print output

        #it executes check for errors
        if retcode != 0:
            print >>sys.stderr, "error code:" + retcode.__str__()
            print output[1]# sError
            quit(retcode)
        lines = output[0].split("\n")
        
        #GET VERSION
        p = subprocess.Popen(shlex.split(commandVersion), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
        #p.wait()
        output = p.communicate()
        retcode = p.returncode
        
        #it executes check for errors
        if retcode != 0:
            print >>sys.stderr, "Error getting version; error code:" + retcode.__str__()
            print output[1]# sError
            quit(retcode)
        version = output[0].replace("\n", "")
    except OSError, ose:
        print >>sys.stderr, "Execution failed:", ose
        quit(2)

    eventDetailText= "program=\"sanitizeNames\"; version=\"" + version + "\""
    for line in lines:
        detoxfiles = line.split(" -> ")
        if len(detoxfiles) > 1 :
            oldfile = detoxfiles[0].split('\n',1)[0]
            newfile = detoxfiles[1]
            #print "line: ", line
            if os.path.isfile(newfile):
                oldfile = oldfile.replace(objectsDirectory, "objects/", 1)
                newfile = newfile.replace(objectsDirectory, "objects/", 1)
                print >>sys.stderr, repr(oldfile)
                print >>sys.stderr, repr(newfile)
                
                if oldfile in UUIDsDic:
                    fileUUID = UUIDsDic[oldfile]
                else:
                    fileUUID = findUUIDFromFileUUIDxml(logsDir+"FileUUIDs.log", oldfile, logsDir+"fileMeta/", updateSIPUUIDfile=True)
                
                #print "fileUUID2: ", fileUUID
                
                eventOutcomeDetailNote = "Original name=\"" + oldfile + "\"; cleaned up name=\"" + newfile + "\""
                eventOutcomeDetailNote = eventOutcomeDetailNote.decode('utf-8')
                event = createEvent( taskUUID, "name cleanup", eventDateTime=date, eventDetailText=eventDetailText, \
                                     eOutcomeInformation=createOutcomeInformation(eventOutcomeDetailNote=eventOutcomeDetailNote, 
                                                                                  eventOutcomeText="prohibited characters removed"))
                #print etree.tostring(event, pretty_print=True) 
                archivematicaRenameFile(logsDir, fileUUID, newfile, event)
            elif os.path.isdir(newfile):
                oldfile = oldfile.replace(objectsDirectory, "objects/", 1) + "/"
                newfile = newfile.replace(objectsDirectory, "objects/", 1) + "/"
                #print UUIDsDic.iteritems().__str__()
                addToUUIDsDic = {}
                for file, fileUUID in UUIDsDic.iteritems():
                    if file.startswith(oldfile):    
                        #print "fileUUID1: ", fileUUID           
                        intermediateFileName = file.replace(oldfile, newfile, 1)
                        eventOutcomeDetailNote = "Original name=\"" + file + "\"; cleaned up name=\"" + intermediateFileName + "\""
                        eventOutcomeDetailNote = eventOutcomeDetailNote.decode('utf-8')
                        event = createEvent( taskUUID, "name cleanup", eventDateTime=date, eventDetailText=eventDetailText, \
                                             eOutcomeInformation=createOutcomeInformation(eventOutcomeDetailNote=eventOutcomeDetailNote, 
                                                                                          eventOutcomeText="prohibited characters removed"))
                        #print etree.tostring(event, pretty_print=True) 
                        archivematicaRenameFile(logsDir, fileUUID, intermediateFileName, event)
                        addToUUIDsDic[intermediateFileName] = fileUUID
                UUIDsDic.update(addToUUIDsDic)

