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
# @version svn: $Id$
from archivematicaXMLNamesSpace import *
import lxml.etree as etree
from xml.sax.saxutils import quoteattr as xml_quoteattr
import os
import sys
import MySQLdb
sys.path.append("/usr/lib/archivematica/archivematicaCommon")
import databaseInterface

from optparse import OptionParser
parser = OptionParser()
parser.add_option("-s",  "--baseDirectoryPath", action="store", dest="baseDirectoryPath", default="")
parser.add_option("-b",  "--baseDirectoryPathString", action="store", dest="baseDirectoryPathString", default="SIPDirectory") #transferDirectory/
parser.add_option("-f",  "--fileGroupIdentifier", action="store", dest="fileGroupIdentifier", default="") #transferUUID/sipUUID
parser.add_option("-t",  "--fileGroupType", action="store", dest="fileGroupType", default="sipUUID") #
parser.add_option("-x",  "--xmlFile", action="store", dest="xmlFile", default="")
parser.add_option("-a",  "--amdSec", action="store_true", dest="amdSec", default=False)
(opts, args) = parser.parse_args()


baseDirectoryPath = opts.baseDirectoryPath
XMLFile = opts.xmlFile
includeAmdSec = opts.amdSec
baseDirectoryPathString = "%%%s%%" % (opts.baseDirectoryPathString)
fileGroupIdentifier = opts.fileGroupIdentifier
fileGroupType = opts.fileGroupType
includeAmdSec=False #opts.amdSec #TODO

#Global Variables
globalMets = root = etree.Element( "mets", \
    nsmap = NSMAP, \
    attrib = { "{" + xsiNS + "}schemaLocation" : "http://www.loc.gov/METS/ http://www.loc.gov/standards/mets/version18/mets.xsd info:lc/xmlns/premis-v2 http://www.loc.gov/standards/premis/premis.xsd http://purl.org/dc/terms/ http://dublincore.org/schemas/xmls/qdc/2008/02/11/dcterms.xsd" } )

globalFileGrps = {}
globalFileGrpsUses = ["original", "preservation", "service", "access", "license", "plaintext"]
for use in globalFileGrpsUses:
    grp = etree.Element(use)
    grp.set("USE", use) 
    globalFileGrps[use] = grp 
 
##counters
#globalCounter = 0
global globalErrorCount
globalErrorCount = 0
global amdSecs
amdSecs = []
global dmdSecs
dmdSecs = []
globalDmdSecCounter = 0
globalAmdSecCounter = 0
globalTechMDCounter = 0
globalRightsMDCounter = 0
globalDigiprovMDCounter = 0



#GROUPID="G1" -> GROUPID="Group-%object's UUID%"
##group of the object and it's related access, license




#move to common
def newChild(parent, tag, text=None, tailText=None, sets=[]):
    child = etree.Element(tag)
    parent.append(child)
    child.text = text
    if tailText:
        child.tail = tailText
    for set in sets:
        key, value = set
        child.set(key, value)
    return child



    


#DMID="dmdSec_01" for an object goes in here
#<file ID="file1-UUID" GROUPID="G1" DMID="dmdSec_02" ADMID="amdSec_01">
def createFileSec(directoryPath, structMapDiv):
    delayed = []
    for item in os.listdir(directoryPath):
        itemdirectoryPath = os.path.join(directoryPath, item)
        if os.path.isdir(itemdirectoryPath):
            delayed.append(item)
                    
        elif os.path.isfile(itemdirectoryPath):
            #myuuid = uuid.uuid4()
            myuuid=""
            #directoryPathSTR = itemdirectoryPath.replace(baseDirectoryPath + "objects", "objects", 1)
            directoryPathSTR = itemdirectoryPath.replace(baseDirectoryPath, baseDirectoryPathString, 1)
            
            sql = """SELECT fileUUID, fileGrpUse FROM Files WHERE removedTime = 0 AND %s = '%s' AND Files.currentLocation = '%s';""" % (fileGroupType, fileGroupIdentifier, MySQLdb.escape_string(directoryPathSTR))
            c, sqlLock = databaseInterface.querySQL(sql) 
            row = c.fetchone()
            if row == None:
                print >>sys.stderr, "No uuid for file: \"", directoryPathSTR, "\""
                global globalErrorCount
                globalErrorCount += 1
                sqlLock.release()
                continue
            while row != None:
                myuuid = row[0]
                use = row[1]
                row = c.fetchone()
            sqlLock.release()
            
            filename = ''.join(xml_quoteattr(item).split("\"")[1:-1])
            directoryPathSTR = itemdirectoryPath.replace(baseDirectoryPath, "", 1)
            #print filename, directoryPathSTR 
            
            
            
            FILEID="%s-%s" % (item, myuuid)
            
                
            #<fptr FILEID="file1-UUID"/>
            newChild(structMapDiv, "fptr", sets=[("FILEID",FILEID)])
            
            GROUPID=""
            if use =="original":
                GROUPID = "Group-%s" % (myuuid) 
            if GROUPID=="":
                print >>sys.stderr, "No groupID for file: \"", directoryPathSTR, "\""
                globalErrorCount += 1
            
            if use in globalFileGrps:
                file = """<file ID="file1-UUID" GROUPID="G1" ADMID="amdSec_01">
<Flocat xlink:href="objects/file1-UUID" locType="other" otherLocType="system"/>
</file>"""
                
                file = newChild(globalFileGrps[use], "file", sets=[("FILEID",FILEID), ("GROUPID",GROUPID)])
                #<Flocat xlink:href="objects/file1-UUID" locType="other" otherLocType="system"/>
                Flocat = newChild(file, "Flocat", sets=[(xlinkBNS +"href",directoryPathSTR), ("locType","other"), ("otherLocType", "system")])
                if includeAmdSec:
                    AMD, AMDID = createDigiprovMD(myuuid, itemdirectoryPath, myuuid)
                    file.set("AMDID", AMDID)
                
            else:
                print >>sys.stderr, "Invalid use: \"", use, "\""
                globalErrorCount += 1
            
            
            #fileI = etree.SubElement( structMapDiv, xlinkBNS + "fits", nsmap=NSMAP)
    
            
            #filename = replace /tmp/"UUID" with /objects/
    
            #fileI.set("ID", "file-" + item.__str__() + "-"    + myuuid.__str__())
            #fileI.set("ADMID", "digiprov-" + item.__str__() + "-"    + myuuid.__str__())            
    
            #Flocat = newChild(fileI, "Flocat")
            #Flocat.set(xlinkBNS + "href", directoryPathSTR )
            #Flocat.set("locType", "other")
            #Flocat.set("otherLocType", "system")
    
            # structMap file
            #div = newChild(structMapDiv, "div")
            #fptr = newChild(div, "fptr")
            #fptr.set("FILEID","file-" + item.__str__() + "-" + myuuid.__str__())
    for item in delayed:
        itemdirectoryPath = os.path.join(directoryPath, item)
        createFileSec(itemdirectoryPath, newChild(structMapDiv, "div", sets=[("TYPE","directory"), ("LABEL",item)]))
            
            
if __name__ == '__main__':
    
    if not baseDirectoryPath.endswith('/'):
        baseDirectoryPath += '/'
    structMap = etree.Element("structMap")
    structMap.set("TYPE", "physical")
    structMapDiv = newChild(structMap, "div", sets=[("TYPE","directory"), ("LABEL","%s-%s" % (os.path.basename(baseDirectoryPath[:-1]), fileGroupIdentifier))])
    #dmdSec, dmdSecID = createDMDSec(SIP)
    structMapDiv = newChild(structMapDiv, "div", sets=[("TYPE","directory"), ("LABEL","objects"), ("DMID","TODO !!! dmdSec_01") ])
    createFileSec(os.path.join(baseDirectoryPath, "objects"), structMapDiv)
    
    
    fileSec = etree.Element( "fileSec")
    for group in globalFileGrpsUses: #globalFileGrps.itervalues():
        grp = globalFileGrps[group]
        if len(grp) > 0:
            fileSec.append(grp)
    
    root = etree.Element( "mets", \
    nsmap = NSMAP, \
    attrib = { "{" + xsiNS + "}schemaLocation" : "http://www.loc.gov/METS/ http://www.loc.gov/standards/mets/version18/mets.xsd info:lc/xmlns/premis-v2 http://www.loc.gov/standards/premis/premis.xsd http://purl.org/dc/terms/ http://dublincore.org/schemas/xmls/qdc/2008/02/11/dcterms.xsd" } )
    
    root.append(fileSec)
    root.append(structMap)
    print etree.tostring(root, pretty_print=True)
            
    #<div TYPE="directory" LABEL="AIP1-UUID">
    #<div TYPE="directory" LABEL="objects" DMID="dmdSec_01">
    #Recursive function for creating structmap and fileSec
    tree = etree.ElementTree(root)
    tree.write(XMLFile)
    exit(globalErrorCount) 