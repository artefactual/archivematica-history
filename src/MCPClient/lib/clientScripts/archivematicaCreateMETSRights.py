#!/usr/bin/python -OO
#
# This file is part of Archivematica.
#
# Copyright 2010-2011 Artefactual Systems Inc. <http://artefactual.com>
#
# Archivematica is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
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

import os
import uuid
import sys
import lxml.etree as etree
import string
import MySQLdb
from xml.sax.saxutils import quoteattr
from datetime import datetime
#from archivematicaCreateMETS2 import escape
sys.path.append("/usr/lib/archivematica/archivematicaCommon")
import databaseInterface
from archivematicaFunctions import escape


def archivematicaGetRights(metadataAppliesToList, fileUUID):
    """[(fileUUID, fileUUIDTYPE), (sipUUID, sipUUIDTYPE), (transferUUID, transferUUIDType)]"""
    ret = []
    for metadataAppliesToidentifier, metadataAppliesToType in metadataAppliesToList:
        list = "RightsStatement.pk, rightsStatementIdentifier, rightsStatementIdentifierType, rightsStatementIdentifierValue, rightsBasis, copyrightStatus, copyrightJurisdiction, copyrightStatusDeterminationDate, licenseIdentifier, licenseIdentifier, licenseTerms"
        key = list.split(", ")
        sql = """SELECT %s FROM RightsStatement LEFT JOIN RightsStatementCopyright ON RightsStatementCopyright.fkRightsStatement = RightsStatement.pk LEFT JOIN RightsStatementLicense ON RightsStatementLicense.fkRightsStatement = RightsStatement.pk WHERE metadataAppliesToidentifier = '%s' AND metadataAppliesToType = %s;""" % (list, metadataAppliesToidentifier, metadataAppliesToType)
        rows = databaseInterface.queryAllSQL(sql)
        if not rows:
            continue
        else:
            for row in rows:
                valueDic= {}
                rightsStatement = etree.Element("rightsStatement")
                rightsStatement.set(xsiBNS+"schemaLocation", premisNS + " http://www.loc.gov/standards/premis/v2/premis-v2-1.xsd")
                rightsStatement.set("version", "2.1")
                ret.append(rightsStatement)
                for i in range(len(key)):
                    valueDic[key[i]] = row[i]
                rightsStatementIdentifier = etree.SubElement(rightsStatement, "rightsStatementIdentifier")
                etree.SubElement(rightsStatementIdentifier, "rightsStatementIdentiferType").text = valueDic["rightsStatementIdentifierType"]
                etree.SubElement(rightsStatementIdentifier, "rightsStatementIdentifierValue").text = valueDic["rightsStatementIdentifierValue"]
                etree.SubElement(rightsStatement, "rightsBasis").text = valueDic["rightsBasis"]
                
                #copright information
                if valueDic["copyrightStatus"] != None and valueDic["copyrightStatus"] != "":
                    coprightInformation = etree.SubElement(rightsStatement, "coprightInformation")
                    etree.SubElement(coprightInformation, "copyrightStatus").text = valueDic["copyrightStatus"]
                    etree.SubElement(coprightInformation, "copyrightJurisdiction").text = valueDic["copyrightJurisdiction"]
                    etree.SubElement(coprightInformation, "copyrightStatusDeterminationDate").text = valueDic["copyrightStatusDeterminationDate"]
                    #TODO 4.1.3.4 copyrightNote (O, R)
                    #copyrightNote Repeatable
                
                # licenseInformation
                licenseInformation = etree.SubElement(rightsStatement, "licenseInformation")
                licenseIdentifier = etree.SubElement(licenseInformation, "licenseIdentifier")
                etree.SubElement(licenseIdentifier, "licenseIdentifierType").text = "http://code.google.com/p/archivematica/issues/detail?id=704 comment 13"#valueDic["licenseIdentifierType"]
                etree.SubElement(licenseIdentifier, "licenseIdentifierValue").text = valueDic["licenseIdentifier"]
                etree.SubElement(licenseInformation, "licenseTerms").text = valueDic["licenseTerms"]
                #TODO licenseNote (O, R)
                #4.1.4.3 licenseNote (O, R)
             
                #4.1.5 statuteInformation (O, R)
                getstatuteInformation(valueDic["RightsStatement.pk"], rightsStatement)
                
                #4.1.6 rightsGranted (O, R)
                getrightsGranted(valueDic["RightsStatement.pk"], rightsStatement)
                
                #4.1.7 linkingObjectIdentifier (O, R)
                linkingObjectIdentifier = etree.SubElement(rightsStatement, "linkingObjectIdentifier")
                etree.SubElement(linkingObjectIdentifier, "linkingObjectIdentifierType").text = "UUID"
                etree.SubElement(linkingObjectIdentifier, "linkingObjectIdentifierValue").text = fileUUID 
                
                
                #4.1.8 linkingAgentIdentifier (O, R)
                sql = """SELECT agentIdentifierType, agentIdentifierValue, agentName, agentType FROM Agents;"""
                c, sqlLock = databaseInterface.querySQL(sql)
                row = c.fetchone()
                while row != None:
                    linkingAgentIdentifier = etree.SubElement(rightsStatement, "linkingAgentIdentifier")
                    etree.SubElement(linkingAgentIdentifier, "linkingAgentIdentifierType").text = row[0]
                    etree.SubElement(linkingAgentIdentifier, "linkingAgentIdentifierValue").text = row[1]
                    row = c.fetchone()
                sqlLock.release()
            break
    return ret

def getstatuteInformation(pk, parent):
    sql = "SELECT pk, statuteJurisdiction, statuteCitation, statuteInformationDeterminationDate FROM RightsStatementStatuteInformation WHERE fkRightsStatement = %d" % (pk)
    rows = databaseInterface.queryAllSQL(sql)
    for row in rows:
        statuteInformation = etree.SubElement(parent, "statuteInformation")
        etree.SubElement(statuteInformation, "statuteJurisdiction").text = row[1]
        etree.SubElement(statuteInformation, "statuteCitation").text = row[2]
        etree.SubElement(statuteInformation, "statuteInformationDeterminationDate").text = row[3]
        
        #TODO 4.1.5.4 statuteNote (O, R) row[0]

def getrightsGranted(pk, parent):
    sql = "SELECT pk, act, startDate, endDate, restriction FROM RightsStatementRightsGranted WHERE fkRightsStatement = %d" % (pk)
    #TODO : restriction is a repeatable field.
    rows = databaseInterface.queryAllSQL(sql)
    for row in rows:
        rightsGranted = etree.SubElement(parent, "rightsGranted")
        #TODO : restriction is a repeatable field.
        etree.SubElement(rightsGranted, "act").text = row[1]
        etree.SubElement(rightsGranted, "restriction").text = row[4]
        etree.SubElement(rightsGranted, "termOfGrant").text = "Issue 859:     termOfGrant is a required field"
        etree.SubElement(rightsGranted, "startDate").text = row[2]
        etree.SubElement(rightsGranted, "endDate").text = row[3]
        
        #TODO 4.1.6.4 rightsGrantedNote (O, R)
        

if __name__ == '__main__':
    root = etree.Element( "mets", \
    nsmap = {None: metsNS, "xlink": xlinkNS}, \
    attrib = { "{" + xsiNS + "}schemaLocation" : "http://www.loc.gov/METS/ http://www.loc.gov/standards/mets/mets.xsd" } )

    #cd /tmp/$UUID;
    opath = os.getcwd()
    os.chdir(basePath)
    path = basePath

    #if includeAmdSec:
    #    amdSec = newChild(root, "amdSec")

    fileSec = etree.Element("fileSec")
    #fileSec.tail = "\n"
    root.append(fileSec)

    sipFileGrp = etree.SubElement(fileSec, "fileGrp")
    sipFileGrp.set("USE", "original")

    structMap = newChild(root, "structMap")
    structMap.set("TYPE", "physical")
    structMapDiv = newChild(structMap, "div")

    createFileSec(path, sipFileGrp, structMapDiv)

    tree = etree.ElementTree(root)
    tree.write(XMLFile, pretty_print=True, xml_declaration=True)

    # Restore original path
    os.chdir(opath)
