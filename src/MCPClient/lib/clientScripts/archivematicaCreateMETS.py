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
from archivematicaFunctions import getTagged
import os
import uuid
import sys
import lxml.etree as etree
import string
from xml.sax.saxutils import quoteattr as xml_quoteattr
from datetime import datetime
from createXmlEventsAssist import createArchivematicaAgent 
from createXmlEventsAssist import createOrganizationAgent

UUIDsDic={}
amdSec=[]

logsDIR = sys.argv[1]
SIPUUID = sys.argv[2]
SIPName = sys.argv[3]
processingDIR = sys.argv[4]



def loadFileUUIDsDic():
    FileUUIDs_fh = open(logsDIR+"FileUUIDs.log", "r")
 
    line = FileUUIDs_fh.readline()
    while line:
        detoxfiles = line.split(" -> ",1)
        if len(detoxfiles) > 1 :
            fileUUID = detoxfiles[0]
            fileName = detoxfiles[1]
            fileName = string.replace(fileName, "\n", "", 1)
            UUIDsDic[fileName] = fileUUID
        line = FileUUIDs_fh.readline()


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

def createDigiprovMD(uuid, filename) :
    digiprovMD = newChild(amdSec, "digiprovMD")
    digiprovMD.set("ID", "digiprov-"+ os.path.basename(filename) + "-" + uuid)
    mdWrap = newChild(digiprovMD,"mdWrap")
    mdWrap.set("MDTYPE", "PREMIS")
    xmlData = newChild(mdWrap, "xmlData")
    premis = etree.SubElement( xmlData, premisBNS + "premis", nsmap=NSMAP, \
        attrib = { "{" + xsiNS + "}schemaLocation" : "info:lc/xmlns/premis-v2 http://www.loc.gov/standards/premis/premis.xsd" })
    premis.set("version", "2.0")
    
    fileMeta = etree.parse(logsDIR + "fileMeta/" + uuid + ".xml").getroot()
    object = getTagged(fileMeta, "object")[0]
    events = getTagged(fileMeta, "events")[0]
    
    premis.append(object)
    premis.append(events)
    agents = etree.SubElement(premis, "agents")
    agents.append(createArchivematicaAgent())
    agents.append(createOrganizationAgent())
    
    
#    objects = newChild(premis, "object")
#    objects.set(xsiBNS + "type", "file")
#    objectIdentifier = newChild(objects, "objectIdentifier")
#    objectIdentifierType = newChild(objectIdentifier, "objectIdentifierType", "UUID")
#    objectIdentifierValue = newChild(objectIdentifier, "objectIdentifierValue", uuid)
#    if filename in DetoxDic:
#        #print DetoxDic[filename] + "\t RENAMED: \t" + filename
#        originalName = newChild(objects, "originalName", DetoxDic[filename])

    #Load Fits
    #mdWrap = newChild(digiprovMD,"mdWrap")
    #mdWrap.set("MDTYPE", "FITS")
    #xmlData = newChild(mdWrap, "xmlData")
    #fits = newChild(xmlData, "fits")
#    fits = etree.SubElement( xmlData, "fits", nsmap=NSMAP, \
#        attrib = { "{" + xsiNS + "}schemaLocation" : "http://hul.harvard.edu/ois/xml/ns/fits/fits_output http://hul.harvard.edu/ois/xml/xsd/fits/fits_output.xsd" })
#    fits.set("version", "0.3.2")
    
#    fitsTree = etree.parse(logsDIR+"FITS-" + uuid + ".xml")
#    fitsRoot = fitsTree.getroot()
#    fits.append(fitsRoot)

def getRelativePath(itempath, processingDIR):
    """
    Instead of pathSTR = itempath.replace(processingDIR + "objects", "objects", 1)
    This was implemented to avoid problems while developing where the symbolic link would resolve while traversing the sip, and cause problems for the replacement.
    /var/archivematica/sharedDirectory/.currentlyProcessing/801e1ffe-6dfd-46cc-822b-e890ed26477b/backup-678a0680-f1be-11df-b321-001b2429801e/
    Error - Log has no UUID for file: /home/joseph/archivematica/src/MCPServer/sharedDirectoryStructure/.currentlyProcessing/801e1ffe-6dfd-46cc-822b-e890ed26477b/backup-678a0680-f1be-11df-b321-001b2429801e/DIP/objects/Archivematica_architecture_7May2010.jpg{/home/joseph/archivematica/src/MCPServer/sharedDirectoryStructure/.currentlyProcessing/801e1ffe-6dfd-46cc-822b-e890ed26477b/backup-678a0680-f1be-11df-b321-001b2429801e/DIP/objects}
    """
    ret = itempath.split(os.path.basename(os.path.dirname(processingDIR)), 1)
    if len(ret) != 2:
        
        print "error: " + ret.__str__()
        quit(3)
    return ret[1].replace("/", "", 1)

#Do /SIP-UUID/
#Force only /SIP-UUID/objects
def createFileSec(path, parentBranch, structMapParent):
    doneFirstRun = True
    pathSTR = path.__str__()
    if pathSTR == processingDIR + "objects/": #IF it's it's the SIP folder, it's OBJECTS
        pathSTR = "objects"
    #pathSTR = string.replace(path.__str__(), "/tmp/" + sys.argv[2] + "/" + sys.argv[3], "objects", 1)
    #if pathSTR + "/" == processingDIR: #if it's the very first run through (recursive function)
    if os.path.basename(pathSTR) == os.path.basename(os.path.dirname(processingDIR)): #if it's the very first run through (recursive function)
        pathSTR = sys.argv[3] + "-" + sys.argv[2]
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
                #pathSTR = itempath.replace(processingDIR + "objects", "objects", 1)
                pathSTR = getRelativePath(itempath, processingDIR)
                if pathSTR in UUIDsDic:
                    myuuid = UUIDsDic[pathSTR]
                else:
                    print "Error - Log has no UUID for file: " + pathSTR + "{" + path.__str__() + "}"
                createDigiprovMD(myuuid, itempath)
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
    os.chdir(processingDIR)
    path = os.getcwd()

    loadFileUUIDsDic()

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
    tree.write(processingDIR + "/METS.xml")

    # Restore original path
    os.chdir(opath)
    
