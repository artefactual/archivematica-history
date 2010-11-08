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
import lxml.etree as etree
import uuid
import subprocess
import os
from archivematicaFunctions import getTagged
from createXmlEventsAssist import createEvent 
from createXmlEventsAssist import createOutcomeInformation
from createXmlEventsAssist import createLinkingAgentIdentifier

def includeFits(fits, xmlFile, date, eventUUID):

    eventDetailText = "program=\"File Identification Toolset\""
    
    ##eventOutcome = createOutcomeInformation( eventOutcomeDetailNote = uuid)
    #TO DO... Gleam the event outcome information from the output
    event = createEvent( eventUUID, "FITS", eventDateTime=date, eventDetailText=eventDetailText)

    
    tree = etree.parse( xmlFile )
    root = tree.getroot()

    events = getTagged(root, "events")[0]
    events.append(event)
    
    objectCharacteristics = getTagged(getTagged(root, "object")[0], "objectCharacteristics")[0]
    objectCharacteristicsExtension = etree.SubElement(objectCharacteristics, "objectCharacteristicsExtension")
    objectCharacteristicsExtension.append(fits)
    
    tree = etree.ElementTree(root)
    tree.write(xmlFile)

if __name__ == '__main__':
    
    target = sys.argv[1]
    XMLfile = sys.argv[2]
    date = sys.argv[3]
    eventUUID = sys.argv[4]
    
    tempFile="/tmp/" + uuid.uuid4().__str__()
    
    #def executeCommand(taskUUID, requiresOutputLock = "no", sInput = "", sOutput = "", sError = "", execute = "", arguments = "", serverConnection = None):
    command = "fits.sh -i \"" + target + "\" -o \"" + tempFile + "\"" 
    #print "command: " + command
    try:
        p = subprocess.Popen(shlex.split(command), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	
        p.wait()
        output = p.communicate()
        retcode = p.returncode

        #it executes check for errors
        if retcode != 0:
            print >>sys.stderr, "error code:" + retcode.__str__()
            print output[1]# sError
            #return retcode
            quit(retcode)
        
        tree = etree.parse(tempFile)
        fits = tree.getroot()
        os.remove(tempFile)
        #fits = etree.XML(output[0])
        includeFits(fits, XMLfile, date, eventUUID)
    
    except OSError, ose:
        print >>sys.stderr, "Execution failed:", ose
        #return 1
        exit(1)
        
