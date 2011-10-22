#!/usr/bin/python -OO

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

#!/usr/bin/python -OO

import sys
import os.path
import os
import logging
import subprocess
import shlex
import uuid
import lxml.etree as etree

## This will need to get changed somehow to be more proper
sys.path.append('/usr/lib/archivematica/MCPClient/clientScripts')
from fileAddedToSIP import addFileToSIP
from archivematicaFunctions import appendEventToFile 
from archivematicaFunctions import getTagged
from createXmlEventsAssist import createEvent
from createXmlEventsAssist import createOutcomeInformation
from createXmlEventsAssist import createOrganizationAgent

def xmlCreateRelationship(relationshipType, relationshipSubType, relatedObjectIdentifierValue, relatedEventIdentifierValue, relatedObjectIdentifierType="UUID", relatedEventIdentifierType="UUID"):
    ret = etree.Element("relationship")
    etree.SubElement(ret, "relationshipType").text = relationshipType
    etree.SubElement(ret, "relationshipSubType").text = relationshipSubType
    
    relatedObjectIdentification = etree.SubElement(ret, "relatedObjectIdentification")        
    etree.SubElement(relatedObjectIdentification, "relatedObjectIdentifierType").text = relatedObjectIdentifierType
    etree.SubElement(relatedObjectIdentification, "relatedObjectIdentifierValue").text = relatedObjectIdentifierValue
    relatedEventIdentification = etree.SubElement(ret, "relatedEventIdentification")
    etree.SubElement(relatedEventIdentification, "relatedEventIdentifierType").text = relatedEventIdentifierType
    etree.SubElement(relatedEventIdentification, "relatedEventIdentifierValue").text = relatedEventIdentifierValue
    return ret
    

def xmlNormalize(outputFileUUID, outputFileName, eventDetailText, fileUUID, objectsPath, eventUUID, edate, logsPath, linkingAgentIdentifier=None):
    #Create Normalization event in the original xml document. 
    eventXML = createEvent( eventUUID, "normalization", \
                            eventDetailText=eventDetailText, \
                            eOutcomeInformation = createOutcomeInformation(os.path.basename(outputFileName)), \
                            eventDateTime = edate, \
                            linkingAgentIdentifier = linkingAgentIdentifier)
    appendEventToFile(logsPath, fileUUID, eventXML)
    
    #Create new document using the add file script
    addFileToSIP( objectsPath, logsPath, outputFileName, outputFileUUID, "creation", edate, edate, eventOutcomeDetailNote=outputFileName)
    
    xmlCreateFileAssociation(outputFileUUID, outputFileName, fileUUID, objectsPath, eventUUID, edate, logsPath)
    
def xmlCreateFileAssociation(outputFileUUID, outputFileName, fileUUID, objectsPath, eventUUID, edate, logsPath):
    #print >>sys.stderr, "adding linking information"
    originalFileXML = etree.parse( logsPath + "fileMeta/" + fileUUID + ".xml" ).getroot()
    outputFileXML = etree.parse( logsPath + "fileMeta/" + outputFileUUID + ".xml" ).getroot()

    #open the newly created document and add association
    relationship = xmlCreateRelationship("derivation", "is source of", relatedObjectIdentifierValue=outputFileUUID, relatedEventIdentifierValue=eventUUID)
    object = getTagged(originalFileXML, "object")[0]
    object.append(relationship)

    #print(etree.tostring(originalFileXML, pretty_print=True))
    #print(etree.tostring(relationship, pretty_print=True))
    
    #open the original document, and create the associated entry.
    relationship = xmlCreateRelationship("derivation", "has source", relatedObjectIdentifierValue=fileUUID, relatedEventIdentifierValue=eventUUID)
    object = getTagged(outputFileXML, "object")[0]
    object.append(relationship)

    etree.ElementTree(originalFileXML).write(logsPath + "fileMeta/" + fileUUID + ".xml")
    etree.ElementTree(outputFileXML).write(logsPath + "fileMeta/" + outputFileUUID + ".xml")
    
def xmlCreateFileAssociationBetween(originalFileFullPath, outputFromNormalizationFileFullPath, SIPFullPath, eventDetailText, objects="objects/", outputFileUUID="", eventUUID="", edate=""):
    import uuid
    from datetime import datetime
    
    sys.path.append("/usr/lib/archivematica/archivematicaCommon")
    from archivematicaMCPFileUUID import getUUIDOfFile
    
    
    objectsPath = (SIPFullPath + objects)
    logsPath =  (SIPFullPath + "logs/")
    linkingAgentIdentifier = createOrganizationAgent()
    
    if outputFileUUID == "":
        if eventUUID != "":
            outputFileUUID = eventUUID
        else:
             outputFileUUID = uuid.uuid4().__str__() 
    if eventUUID == "":
        eventUUID = outputFileUUID 
    if edate == "":
        edate =  datetime.utcnow().isoformat('T')
    
    sourceRelative = originalFileFullPath.replace(objectsPath, objects, 1)
    sourceUUID = getUUIDOfFile( logsPath + "FileUUIDs.log", objectsPath, originalFileFullPath, logsPath + "fileMeta/" )
    
    xmlNormalize(outputFileUUID, outputFromNormalizationFileFullPath, eventDetailText, sourceUUID, objectsPath, eventUUID, edate, logsPath, linkingAgentIdentifier=None)
   

testxmlNormalize="""
# Main program
if __name__ == '__main__':
    outputFileUUID = sys.argv[1]
    outputFileName = sys.argv[2]
    fileUUID = sys.argv[3] 
    objectsPath = sys.argv[4] 
    eventUUID = sys.argv[5] 
    edate = sys.argv[6] 
    logsPath = sys.argv[7]
    command =  sys.argv[8]
    xmlNormalize(outputFileUUID, outputFileName, command, fileUUID, objectsPath, eventUUID, edate, logsPath)
"""

#testxmlCreateFileAssociationBetween = 
if __name__ == '__main__':
    originalFileFullPath = sys.argv[1]
    outputFromNormalizationFileFullPath = sys.argv[2]
    SIPFullPath = sys.argv[3] 
    eventDetailText = sys.argv[4] 
    xmlCreateFileAssociationBetween(originalFileFullPath, outputFromNormalizationFileFullPath, SIPFullPath, eventDetailText)


#if __name__ == '__main__':
    #exec testxmlCreateFileAssociationBetween
    
    