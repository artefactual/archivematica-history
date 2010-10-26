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
import uuid
import hashlib
import lxml.etree as etree
from createXmlEventsAssist import createEvent 
from createXmlEventsAssist import createOutcomeInformation
from createXmlEventsAssist import createLinkingAgentIdentifier


#etree.Element("root", interesting="totally")
#SubElement(root, "child").text = "Child 1"

#<arguments> "%relativeLocation%" "%fileUUID%" "%taskUUID%" "%date%" "%SIPLogsDirectory%"FILEEvents/</arguments>


#Borrowed from http://stackoverflow.com/questions/1131220/get-md5-hash-of-a-files-without-open-it-in-python
def md5_for_file(fileName, block_size=2**20):   
    f = open(fileName)
    md5 = hashlib.md5()
    while True:
        data = f.read(block_size)
        if not data:
            break
        md5.update(data)
    #return md5.digest()
    return md5.hexdigest()


def addFileToSIP( objectsDirectory, logsDirectory, filePath, fileUUID, eIDValue, date ):
    """This creates an Archivematica Quarantine Event xml file"""
    relativeFilePath = filePath.replace(objectsDirectory, "objects/", 1)
        
    #generate MD5
    md5Checksum = md5_for_file(filePath)
    
    #create Event to explain file origin.   
    eIDValue = "ingested-" + fileUUID
    ingestEvent = createEvent(eIDValue, "ingest", eventDateTime=date, eventDetailText=relativeFilePath)
    
    eIDValue = "checksumed-" + fileUUID
    eOutcomeInformation = createOutcomeInformation(md5Checksum.__str__())
    checksumEvent = createEvent( eIDValue, "Archivematica checksum created", eventDateTime=date, eOutcomeInformation=eOutcomeInformation)
    
    root = etree.Element("file")
    etree.SubElement(root, "originalFileName").text = relativeFilePath
    etree.SubElement(root, "currentFileName").text = relativeFilePath
    etree.SubElement(root, "fileUUID").text = fileUUID
    etree.SubElement(root, "checksum").text = md5Checksum

    
    events = etree.SubElement(root, "events")
    events.append(ingestEvent)
    events.append(checksumEvent)
    #print >>sys.stderr, "fileUUID -> relativeFilePath"
    tree = etree.ElementTree(root)
    outputFile = logsDirectory + "fileMeta/" + fileUUID + ".xml"
    print "outputFile: " + outputFile
    tree.write(outputFile)

if __name__ == '__main__':
    objectsDirectory = sys.argv[1]
    logsDirectory = sys.argv[2]
    filePath = sys.argv[3]
    fileUUID = sys.argv[4]
    eIDValue = sys.argv[5]
    date = sys.argv[6]
    
    addFileToSIP(objectsDirectory, logsDirectory, filePath, fileUUID, eIDValue, date)
