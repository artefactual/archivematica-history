#!/usr/bin/python
#
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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.    See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Archivematica.    If not, see <http://www.gnu.org/licenses/>.

# @package Archivematica
# @subpackage Ingest
# @author Joseph Perry <joseph@artefactual.com>
# @author Peter Van Garderen <peter@artefactual.com>
# @version svn: $Id$

from archivematicaXMLNamesSpace import *

import os
import uuid
import sys
import lxml.etree as etree
import string
import MySQLdb
from xml.sax.saxutils import quoteattr as xml_quoteattr
from datetime import datetime
from createXmlEventsAssist import createArchivematicaAgent 
from createXmlEventsAssist import createOrganizationAgent
sys.path.append("/usr/lib/archivematica/archivematicaCommon")
import databaseInterface
from archivematicaFunctions import getTagged

UUIDsDic={}
amdSec=[]

SIPUUID = sys.argv[1]
SIPDirectory = sys.argv[2]
XMLFile = sys.argv[3]

def newChild(parent, tag, text=None, tailText=None):
    child = etree.Element(tag)
    parent.append(child)
    child.text = text
    if not parent.text:
        parent.text = "\n"
    if tailText:
        child.tail = tailText
    else :
        child.tail = "\n"     
    return child

def createDigiprovMD(uuid, filename, fileUUID) :
    digiprovMD = newChild(amdSec, "digiprovMD")
    digiprovMD.set("ID", "digiprov-"+ os.path.basename(filename) + "-" + uuid)
    mdWrap = newChild(digiprovMD,"mdWrap")
    mdWrap.set("MDTYPE", "PREMIS")
    xmlData = newChild(mdWrap, "xmlData")
    premis = etree.SubElement( xmlData, premisBNS + "premis", nsmap=NSMAP, \
        attrib = { "{" + xsiNS + "}schemaLocation" : "info:lc/xmlns/premis-v2 http://www.loc.gov/standards/premis/premis.xsd" })
    premis.set("version", "2.0")
    
        
    #OBJECT
    object = etree.SubElement(premis, "object")
    
    objectIdentifier = etree.SubElement(object, "objectIdentifier")
    etree.SubElement(objectIdentifier, "objectIdentifierType").text = "UUID"
    etree.SubElement(objectIdentifier, "objectIdentifierValue").text = uuid
    
    etree.SubElement(object, "objectCategory").text = "file"
    
    objectCharacteristics = etree.SubElement(object, "objectCharacteristics")
    etree.SubElement(objectCharacteristics, "compositionLevel").text = "0"
    
    fixity = etree.SubElement(object, "fixity")
    etree.SubElement(fixity, "messageDigestAlgorithm").text = "sha256"
    etree.SubElement(fixity, "messageDigest").text = "TODO - message digest"
    
    etree.SubElement(object, "size").text = "TODO - file size in bytes"
    
    sql = "SELECT * FROM FilesIDs WHERE fileUUID = '" + fileUUID + "';"
    c, sqlLock = databaseInterface.querySQL(sql) 
    row = c.fetchone()
    if not row:
        format = etree.SubElement(object, "format")
        formatDesignation = etree.SubElement(format, "formatDesignation")
        etree.SubElement(formatDesignation, "formatName").text = "Unknown"
    while row != None:
        print row
        format = etree.SubElement(object, "format")
        #fileUUID = row[0] 
        
        formatDesignation = etree.SubElement(format, "formatDesignation")
        etree.SubElement(formatDesignation, "formatName").text = row[1]
        etree.SubElement(formatDesignation, "formatVersion").text = row[2] 

        formatRegistry = etree.SubElement(format, "formatRegistry")
        etree.SubElement(formatRegistry, "formatRegistryName").text = row[3]
        etree.SubElement(formatRegistry, "formatRegistryKey").text = row[4]
        row = c.fetchone()
    sqlLock.release()
    
    objectCharacteristicsExtension = etree.SubElement(premis, "objectCharacteristicsExtension")
    
    sql = "SELECT FilesFits.FITSxml FROM FilesFits WHERE fileUUID = '" + fileUUID + "';"
    c, sqlLock = databaseInterface.querySQL(sql) 
    row = c.fetchone()
    if not row:
        print >>sys.stderr, "Error no fits."
    while row != None:
        fits = etree.fromstring(row[0])
        objectCharacteristicsExtension.append(fits)
        row = c.fetchone()
    sqlLock.release()
    
    sql = "SELECT Files.originalLoacation FROM Files WHERE Files.fileUUID = '" + fileUUID + "';"
    c, sqlLock = databaseInterface.querySQL(sql) 
    row = c.fetchone()
    if not row:
        print >>sys.stderr, "Error no fits."
    while row != None:
        etree.SubElement(object, "originalName").text = row[0]
        row = c.fetchone()
    sqlLock.release()
    
    sql = "SELECT * FROM Derivations WHERE sourceFileUUID = '" + fileUUID + "';"
    c, sqlLock = databaseInterface.querySQL(sql) 
    row = c.fetchone()
    while row != None:
        relationship = etree.SubElement(object, "relationship")
        etree.SubElement(object, "relationshipType").text = "derivation"
        etree.SubElement(object, "relationshipSubType").text = "is source of"
        
        relatedObjectIdentification = etree.SubElement(relationship, "relatedObjectIdentification")
        etree.SubElement(relatedObjectIdentification, "relatedObjectIdentification").text = "UUID"
        etree.SubElement(relatedObjectIdentification, "relatedObjectIdentifierValue").text = row[2]
        
        relatedEventIdentification = etree.SubElement(relationship, "relatedEventIdentification")
        etree.SubElement(relatedEventIdentification, "relatedObjectIdentification").text = "UUID"
        etree.SubElement(relatedEventIdentification, "relatedObjectIdentifierValue").text = row[3]

        row = c.fetchone()
    sqlLock.release()

    sql = "SELECT * FROM Derivations WHERE derivedFileUUID = '" + fileUUID + "';"
    c, sqlLock = databaseInterface.querySQL(sql) 
    row = c.fetchone()
    while row != None:
        relationship = etree.SubElement(object, "relationship")
        etree.SubElement(object, "relationshipType").text = "derivation"
        etree.SubElement(object, "relationshipSubType").text = "has source"
        
        relatedObjectIdentification = etree.SubElement(relationship, "relatedObjectIdentification")
        etree.SubElement(relatedObjectIdentification, "relatedObjectIdentification").text = "UUID"
        etree.SubElement(relatedObjectIdentification, "relatedObjectIdentifierValue").text = row[1]
        
        relatedEventIdentification = etree.SubElement(relationship, "relatedEventIdentification")
        etree.SubElement(relatedEventIdentification, "relatedObjectIdentification").text = "UUID"
        etree.SubElement(relatedEventIdentification, "relatedObjectIdentifierValue").text = row[3]

        row = c.fetchone()
    sqlLock.release()

    
    #EVENTS
    #premis.append(events)
    events = etree.SubElement(premis, "events")
    #| pk  | fileUUID | eventIdentifierUUID | eventType | eventDateTime | eventDetail | eventOutcome | eventOutcomeDetailNote | linkingAgentIdentifier |
    sql = "SELECT * FROM Events WHERE fileUUID = '" + fileUUID + "';"
    c, sqlLock = databaseInterface.querySQL(sql) 
    row = c.fetchone()
    while row != None:
        event = etree.SubElement(events, "event")
        
        eventIdentifier = etree.SubElement(event, "eventIdentifier")
        etree.SubElement(eventIdentifier, "eventIdentifierType").text = "UUID"
        etree.SubElement(eventIdentifier, "eventIdentifierValue").text = row[2] 
        
        etree.SubElement(event, "eventType").text = row[3]
        etree.SubElement(event, "eventDateTime").text = row[4]
        etree.SubElement(event, "eventDetail").text = row[5]
        
        eventOutcomeInformation  = etree.SubElement(event, "eventOutcomeInformation")
        etree.SubElement(eventOutcomeInformation, "eventOutcome").text = row[6]
        eventOutcomeDetail = etree.SubElement(eventOutcomeInformation, "eventOutcomeDetail")
        etree.SubElement(eventOutcomeDetail, "eventOutcomeDetailNote").text = row[7]
        
        linkingAgentIdentifier = etree.SubElement(event, "linkingAgentIdentifier")
        etree.SubElement(linkingAgentIdentifier, "linkingAgentIdentifierType").text = "repository code"
        etree.SubElement(linkingAgentIdentifier, "linkingAgentIdentifierType").text = "TODO"
        row = c.fetchone()
    sqlLock.release()
   
    
    #AGENTS
    agents = etree.SubElement(premis, "agents")
    agents.append(createArchivematicaAgent())
    agents.append(createOrganizationAgent())
    
 

#Do /SIP-UUID/
#Force only /SIP-UUID/objects
doneFirstRun = False
def createFileSec(path, parentBranch, structMapParent):
    print >>sys.stderr, "createFileSec: ", path, parentBranch, structMapParent
    doneFirstRun = True
    pathSTR = path.__str__()
    pathSTR = path.__str__()
    if pathSTR == SIPDirectory + "objects/": #IF it's it's the SIP folder, it's OBJECTS
        pathSTR = "objects"
    #pathSTR = string.replace(path.__str__(), "/tmp/" + sys.argv[2] + "/" + sys.argv[3], "objects", 1)
    #if pathSTR + "/" == SIPDirectory: #if it's the very first run through (recursive function)
    if path == SIPDirectory: #if it's the very first run through (recursive function)
        pathSTR = os.path.basename(os.path.dirname(SIPDirectory))
        structMapParent.set("DMDID", "SIP-description")
        
        currentBranch = newChild(parentBranch, "fileGrp")
        currentBranch.set("USE", "directory")
        # structMap directory
        div = newChild(structMapParent, "div")
        createFileSec(os.path.join(path, "objects/"), currentBranch, div)
        doneFirstRun = False
    filename = os.path.basename(pathSTR)
    parentBranch.set("ID", filename)
    structMapParent.set("LABEL", filename)
    structMapParent.set("TYPE", "directory")
    
    if doneFirstRun:
        for item in os.listdir(path):
            itempath = os.path.join(path, item)
            if os.path.isdir(itempath):
                currentBranch = newChild(parentBranch, "fileGrp")
                currentBranch.set("USE", "directory")
                # structMap directory
                div = newChild(structMapParent, "div")

                createFileSec(os.path.join(path, item), currentBranch, div)        
            elif os.path.isfile(itempath):
                #myuuid = uuid.uuid4()
                myuuid=""
                #pathSTR = itempath.replace(SIPDirectory + "objects", "objects", 1)
                pathSTR = itempath.replace(SIPDirectory, "%SIPDirectory%", 1)
                
                sql = """SELECT fileUUID FROM Files WHERE removedTime = 0 AND sipUUID = '""" + SIPUUID + """' AND Files.currentLocation = '""" + MySQLdb.escape_string(pathSTR) + """';"""
                c, sqlLock = databaseInterface.querySQL(sql) 
                row = c.fetchone()
                if row == None:
                    print >>sys.stderr, "No uuid for file: \"", pathSTR, "\""
                while row != None:
                    myuuid = row[0]
                    row = c.fetchone()
                sqlLock.release()
                

                createDigiprovMD(myuuid, itempath, myuuid)
                #TODO ^
                pathSTR = itempath.replace(SIPDirectory, "", 1)
                
                fileI = etree.SubElement( parentBranch, xlinkBNS + "fits", nsmap=NSMAP)

                filename = ''.join(xml_quoteattr(item).split("\"")[1:-1])
                #filename = replace /tmp/"UUID" with /objects/

                fileI.set("ID", "file-" + item.__str__() + "-"    + myuuid.__str__())
                fileI.set("ADMID", "digiprov-" + item.__str__() + "-"    + myuuid.__str__())            

                Flocat = newChild(fileI, "Flocat")
                Flocat.set(xlinkBNS + "href", pathSTR )
                Flocat.set("locType", "other")
                Flocat.set("otherLocType", "system")

                # structMap file
                div = newChild(structMapParent, "div")
                fptr = newChild(div, "fptr")
                fptr.set("FILEID","file-" + item.__str__() + "-" + myuuid.__str__())
         
if __name__ == '__main__':
    root = etree.Element( "mets", \
    nsmap = NSMAP, \
    attrib = { "{" + xsiNS + "}schemaLocation" : "http://www.loc.gov/METS/ http://www.loc.gov/standards/mets/version18/mets.xsd info:lc/xmlns/premis-v2 http://www.loc.gov/standards/premis/premis.xsd http://purl.org/dc/terms/ http://dublincore.org/schemas/xmls/qdc/2008/02/11/dcterms.xsd" } )

    #cd /tmp/$UUID; 
    opath = os.getcwd()
    os.chdir(SIPDirectory)
    path = SIPDirectory

    amdSec = newChild(root, "amdSec")

    fileSec = etree.Element("fileSec")
    fileSec.tail = "\n"
    root.append(fileSec)

    sipFileGrp = etree.Element("fileGrp")
    sipFileGrp.tail = "\n"
    sipFileGrp.set("ID", sys.argv[2].__str__())
    sipFileGrp.set("USE", "Objects package")
    fileSec.append(sipFileGrp)

    structMap = newChild(root, "structMap")
    structMapDiv = newChild(structMap, "div")
    
    createFileSec(path, sipFileGrp, structMapDiv)

    tree = etree.ElementTree(root)
    tree.write(XMLFile)

    # Restore original path
    os.chdir(opath)
    
