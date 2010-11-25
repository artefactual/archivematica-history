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

#!/usr/bin/python

from archivematicaFreeSpaceChecker import checkSpace
from archivematicaLoadConfig import loadConfig
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


#Delete the normalized file if free space below x number of bytes
spaceThreshold="10240"
archivmaticaVars=loadConfig("/etc/transcoder/transcoderConfig.conf")

#CONFIGURE THE FOLLOWING DIRECTORIES
accessFileDirectory = ""
fileDirectory = ""

#CONFIGURE THE FOLLOWING APPLICATION PATHS
#formatPoliciesPath = "/mnt/userver910/archivematica2/includes/archivematica/formatPolicies"
formatPoliciesPath = archivmaticaVars["formatPoliciesPath"]
convertPath = archivmaticaVars["convertPath"]
ffmpegPath = archivmaticaVars["ffmpegPath"]
theoraPath = archivmaticaVars["theoraPath"]
unoconvPath = archivmaticaVars["unoconvPath"]
#xenaPath = archivmaticaVars["xenaPath"]
transcoderScriptsDir = archivmaticaVars["transcoderScriptsDir"]

#SET THE DEFAULT COMMAND
defaultCommand = "echo No default normalization tool defined."

#this script is passed fileIn, uuid
fileIn = sys.argv[1]
fileUUID = sys.argv[2]
accesspath = sys.argv[3]
xmlStuff = sys.argv[4] #yes/no
edate = ""
eid = ""
objectsPath = ""
logsPath = ""
if xmlStuff == "yes":
    edate = sys.argv[5]
    eid = sys.argv[6]
    objectsPath = sys.argv[7]
    logsPath = sys.argv[8]    

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
    

def xmlNormalize(outputFileUUID, outputFileName, command, fileUUID=fileUUID, objectsPath=objectsPath, eventUUID=eid, edate=edate, logsPath=logsPath):
    #Create Normalization event in the original xml document.
    eventDetailText =  "program=\"" + command.split(" ", 1)[0] + "\"; command=\"" + command + "\""  
    eventXML = createEvent( eventUUID, "Normalization", \
                            eventDetailText, \
                            eOutcomeInformation = createOutcomeInformation(os.path.basename(outputFileName)), \
                            eventDateTime = edate)
    appendEventToFile(logsPath, fileUUID, eventXML)
    
    #Create new document using the add file script
    addFileToSIP( objectsPath, logsPath, outputFileName, outputFileUUID, "file created - Normalized", edate, edate)
    #addFileToSIP( objectsDirectory, logsDirectory, filePath, fileUUID, eIDValue, date, objects="objects/" ):
    
    
    xmlCreateFileAssociation(outputFileUUID, outputFileName)
    
def xmlCreateFileAssociation(outputFileUUID, outputFileName, fileUUID=fileUUID, objectsPath=objectsPath, eventUUID=eid, edate=edate, logsPath=logsPath):
    print >>sys.stderr, "adding linking information"
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

#get file name and extension
s = fileIn
#get indexes for python string array
#index of next char after last /
x1 = s.rfind('/')+1
#index of last .
x2 = s.rfind('.')
#index of next char after last .
x2mod = x2+1
#length of s
sLen = len(s)

fileTitle = s[x1:x2]
fileExtension = s[x2mod:sLen]
fileDirectory = s[:x1]
fileFullName = fileDirectory + fileTitle + "." + fileExtension

print >>sys.stderr, "\nNORMALIZING: " + fileTitle + "." + fileExtension + " {" + fileUUID + "}"

def findDirectory(root, tag=None, text=None):
    ret = []
    if (not tag) and (not text):
    #return all
        for element in root:
            ret.append(element)
    else:
        if tag:
            if not text:
                #match the tag
                for element in root:
                  if element.tag == tag:
                    ret.append(element)
            else:
                #match tag and text
                for element in root:
                  if element.tag == tag and element.text == text:
                    ret.append(element)
        else:
            #match the text
            for element in root:
                if element.text == text:
                  ret.append(element)
    return ret

def fillAttrib(attrib, var, fileExtension):
    tree = etree.parse(formatPoliciesPath + "/" + fileExtension.upper() + ".xml")
    root = tree.getroot()
#  print(etree.tostring(root))
 
    varsxml = findDirectory(root, "inherit")
    if varsxml[0].text :
        return fillAttrib( attrib, var, varsxml[0].text )
    
    varsxml = findDirectory(root, attrib)
    for varxml in varsxml:
        var.append(varxml.text)
#  print var

inherit = []
accessFormat = []
preservationFormat = []
accessConversionCommand = []
preservationConversionCommand =  []

def executeCommand(command, newUUID=""):
    #Replace replacement strings
    replacementDic = { \
    "%convertPath%": convertPath, \
    "%ffmpegPath%": ffmpegPath, \
    "%theoraPath%": theoraPath, \
    "%unoconvPath%": unoconvPath, \
    "%fileExtension%": fileExtension, \
    "%fileFullName%": fileFullName, \
    "%accessFileDirectory%": accesspath, \
    "%preservationFileDirectory%": fileDirectory + newUUID, \
    "%fileDirectory%": fileDirectory,\
    "%fileTitle%": fileTitle, \
    "%normalizationScriptsDir%": transcoderScriptsDir, \
    "%transcoderScriptsDir%": transcoderScriptsDir, \
    "%accessFormat%": accessFormat[0].lower(), \
    "%preservationFormat%": preservationFormat[0].lower() }
    
    #for each key replace all instances of the key in the command string
    for key in replacementDic.iterkeys():
        command = command.replace ( key, replacementDic[key] )

    #execute command
    try:
        if command != []:
            print >>sys.stderr, "processing: " + command.__str__()
            retcode = subprocess.call( shlex.split(command) )
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

try:
    fillAttrib("inherit", inherit, fileExtension)
    fillAttrib("accessFormat", accessFormat, fileExtension)
    fillAttrib("preservationFormat", preservationFormat, fileExtension)
    fillAttrib("accessConversionCommand", accessConversionCommand, fileExtension)
    fillAttrib("preservationConversionCommand", preservationConversionCommand, fileExtension)



except OSError, ose:
    print >>sys.stderr, "No normalization", ose
except IOError, ose:
    #NO config file for this extension
    
    #reset variables, to be sure
    inherit = []
    accessFormat = []
    preservationFormat = []
    accessConversionCommand = []
    preservationConversionCommand =  []
    
    #add default command to preservationConversionCommand
    preservationConversionCommand.append(defaultCommand)

if len(accessFormat) == 0:  
    accessFormat.append("NONE")
else:
    if accessFormat[0]:
        accessFormat[0] = accessFormat[0].lower()
    else:
        accessFormat[0] = "NONE"

if len(preservationFormat) == 0:  
    preservationFormat.append("NONE")
else:
    if preservationFormat[0]:
        preservationFormat[0] = preservationFormat[0].lower()
    else:
        preservationFormat[0] = "NONE"
    
#file not exist - no preservation format/malformed conf specified for .fileExtension

#if the file is not in access format
if len(accessConversionCommand) > 0 :
    result = 1
    index = 0
    while(result and len(accessConversionCommand) > index):
        if(len(accessFormat) > 0 and accessFormat[0] and accessFormat[0].upper() == fileExtension.upper()):
            result = 0
            accessConversionCommand[0] = "cp %fileFullName% %accessFileDirectory%."
            print >>sys.stderr, "Already in access format. No need to normalize."
        if accessConversionCommand[index]:
            result = executeCommand(accessConversionCommand[index])
            
            #is the destination folder out of space (also may cause a normalization error).
            if checkSpace(accesspath, spaceThreshold):
              Format="NONE"
              if (accessFormat[0].upper() == Format or accessFormat[0].upper() == fileExtension.upper()):
                if accesspath != fileDirectory:
                  os.remove(accesspath + fileTitle + "." + fileExtension)
              else:
                os.remove(accesspath + fileTitle + "." + accessFormat[0].lower())
              print >>sys.stderr, "ERROR: Archivematica detected low space on the access normalization destination drive, and removed the normalized file. This should be considered a hard drive space error."
              quit(2)        
        else:
            print >>sys.stderr, "Skipping Access Normalization: No command"
            accessConversionCommand[index] = "cp %fileFullName% %accessFileDirectory%."
            result = executeCommand(accessConversionCommand[index])
        index += 1
    if result:
        print >>sys.stderr, "!!! ACCESS NORMALIZATION FAILED !!!"
        quit(result)
else:
    accessConversionCommand.append("cp \"%fileFullName%\" \"%accessFileDirectory%.\"")
    result = executeCommand(accessConversionCommand[0])
    print >>sys.stderr, "No access normalization performed."
    if result:
        print >>sys.stderr, "!!! ACCESS NORMALIZATION FAILED !!!"
        quit(result)

#if the file is not in preservation format
if len(preservationConversionCommand) > 0:
    result = 1
    index = 0
    while(result and len(preservationConversionCommand) > index):
        if(len(preservationFormat) > 0 and preservationFormat[0] and preservationFormat[0].upper() == fileExtension.upper()):
            result = 0
            print >>sys.stderr, "Already in preservation format. No need to normalize."
            continue
        if preservationConversionCommand[index]:
            outputFileUUID = uuid.uuid4().__str__()
            result = executeCommand(preservationConversionCommand[index], outputFileUUID)
            
            #is the destination folder out of space (also may cause a normalization error).
            if checkSpace(fileDirectory, spaceThreshold): #+/ ?
                Format="NONE"
                if (preservationFormat[0].upper() == Format or preservationFormat[0].upper() == fileExtension.upper()):
                    if fileDirectory != fileDirectory:#update when not transcoding to file path
                        os.remove(fileDirectory + fileTitle + "." + fileExtension)
                else:
                    os.remove(fileDirectory + fileTitle + "." + preservationFormat[0].lower())
                    print >>sys.stderr, "ERROR: Archivematica detected low space on the access normalization destination drive, and removed the normalized file. This should be considered a hard drive space error."
                    quit(2)
                    
            #XML
            if xmlStuff and preservationConversionCommand[index] != defaultCommand:
                xmlNormalize(outputFileUUID, fileDirectory + outputFileUUID + fileTitle + "." + preservationFormat[0].lower(), preservationConversionCommand[index]) #    {normalized; not normalized}
        else:
            print >>sys.stderr, "Skipping Preservation Normalization: No command"
            result = 0 
        index += 1

        #fileDirectory will need to change eventually to something directly related to normalization path.
        
    if result:
        print >>sys.stderr, "!!! PRESERVATION NORMALIZATION FAILED !!!"
        quit(result)
        
else:
    print >>sys.stderr, "No preservation normalization performed."
#check to see if the file was created





