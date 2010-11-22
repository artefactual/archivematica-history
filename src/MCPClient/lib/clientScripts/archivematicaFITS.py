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



def formatValidationFITSAssist(fits):
    prefix = ""
    formatValidation = None
    
    tools = getTagged(getTagged(fits, "toolOutput")[0], "tool")
    for tool in tools:
        if tool.get("name") == "Jhove":
            formatValidation = tool
            break
    
    repInfo = getTagged(formatValidation, "repInfo")[0]
    
    #<eventDetail>program="DROID"; version="3.0"</eventDetail>
    eventDetailText =   "program=\"" + formatValidation.get("name") \
                        + "\"; version=\"" + formatValidation.get("version") + "\""
                        

    #<status>Well-Formed and valid</status>
    status = getTagged( repInfo, prefix + "status")[0].text
    eventOutcomeText = "fail"
    if status == "Well-Formed and valid":
        eventOutcomeText = "pass"
        
    #<eventOutcomeDetailNote> format="Windows Bitmap"; version="3.0"; result="Well-formed and valid" </eventOutcomeDetailNote>
    format = getTagged(repInfo, prefix + "format")[0].text
    versionXML = getTagged(repInfo, prefix + "version")
    version = "" 
    if len(versionXML):
        version = versionXML[0].text  
    eventOutcomeDetailNote = "format=\"" + format
    if version:
        eventOutcomeDetailNote += "\"; version=\"" + version
    eventOutcomeDetailNote += "\"; result=\"" + status + "\"" 
    
    return tuple([eventDetailText, eventOutcomeText, eventOutcomeDetailNote]) #tuple([1, 2, 3]) returns (1, 2, 3).    
    

def formatIdentificationFITSAssist(fits):
    prefix = "{http://www.nationalarchives.gov.uk/pronom/FileCollection}"
    formatIdentification = None
    
    tools = getTagged(getTagged(fits, "toolOutput")[0], "tool")
    for tool in tools:
        if tool.get("name") == "Droid":
            formatIdentification = tool
            break
    #<eventDetail>program="DROID"; version="3.0"</eventDetail>
    eventDetailText =   "program=\"" + formatIdentification.get("name") \
                        + "\"; version=\"" + formatIdentification.get("version") + "\""
                        
    #<eventOutcome>positive</eventOutcome>
    
    fileCollection = getTagged(formatIdentification, prefix + "FileCollection")[0] 
    IdentificationFile = getTagged(fileCollection, prefix + "IdentificationFile")[0]
    eventOutcomeText =  IdentificationFile.get( "IdentQuality")
    
    #<eventOutcomeDetailNote>fmt/116</eventOutcomeDetailNote>
    eventOutcomeDetailNote = getTagged(getTagged(IdentificationFile, prefix + "FileFormatHit")[0], prefix + "PUID")[0].text
    
    return tuple([eventDetailText, eventOutcomeText, eventOutcomeDetailNote]) #tuple([1, 2, 3]) returns (1, 2, 3).


def includeFits(fits, xmlFile, date, eventUUID):
    ##eventOutcome = createOutcomeInformation( eventOutcomeDetailNote = uuid)
    #TO DO... Gleam the event outcome information from the output
    
    #print etree.tostring(fits, pretty_print=True)
    
    eventDetailText, eventOutcomeText, eventOutcomeDetailNote = formatIdentificationFITSAssist(fits)
    outcomeInformation = createOutcomeInformation( eventOutcomeDetailNote, eventOutcomeText)
    formatIdentificationEvent = createEvent( eventUUID, "format identification", \
                                             eventDateTime=date, \
                                             eventDetailText=eventDetailText, \
                                             eOutcomeInformation=outcomeInformation)
    
    eventDetailText, eventOutcomeText, eventOutcomeDetailNote = formatValidationFITSAssist(fits)
    outcomeInformation = createOutcomeInformation( eventOutcomeDetailNote, eventOutcomeText)
    formatValidationEvent = createEvent( eventUUID, "format validation", \
                                             eventDateTime=date, \
                                             eventDetailText=eventDetailText, \
                                             eOutcomeInformation=outcomeInformation)
    
    tree = etree.parse( xmlFile )
    root = tree.getroot()

    events = getTagged(root, "events")[0]
    events.append(formatIdentificationEvent)
    events.append(formatValidationEvent)
    
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
        
