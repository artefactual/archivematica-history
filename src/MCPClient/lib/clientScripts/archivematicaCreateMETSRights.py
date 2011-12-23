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
import sys
import lxml.etree as etree
sys.path.append("/usr/lib/archivematica/archivematicaCommon")
import databaseInterface
from sharedVariablesAcrossModules import sharedVariablesAcrossModules
from archivematicaFunctions import escape


def formatDate(date):
    """hack fix for 0.8, easy dashboard insertion ISO 8061 -> edtfSimpleType"""
    if date:
        date = date.replace("/", "-")
    return date
      

def archivematicaGetRights(metadataAppliesToList, fileUUID):
    """[(fileUUID, fileUUIDTYPE), (sipUUID, sipUUIDTYPE), (transferUUID, transferUUIDType)]"""
    ret = []
    for metadataAppliesToidentifier, metadataAppliesToType in metadataAppliesToList:
        list = "RightsStatement.pk, rightsStatementIdentifierType, rightsStatementIdentifierType, rightsStatementIdentifierValue, rightsBasis, copyrightStatus, copyrightJurisdiction, copyrightStatusDeterminationDate, licenseIdentifierType, licenseIdentifierValue, licenseTerms"
        key = list.split(", ")
        sql = """SELECT %s FROM RightsStatement LEFT JOIN RightsStatementCopyright ON RightsStatementCopyright.fkRightsStatement = RightsStatement.pk LEFT JOIN RightsStatementLicense ON RightsStatementLicense.fkRightsStatement = RightsStatement.pk WHERE metadataAppliesToidentifier = '%s' AND metadataAppliesToType = %s;""" % (list, metadataAppliesToidentifier, metadataAppliesToType)
        rows = databaseInterface.queryAllSQL(sql)
        if not rows:
            continue
        else:
            for row in rows:
                valueDic= {}
                rightsStatement = etree.Element("rightsStatement", nsmap={None: premisNS})
                rightsStatement.set(xsiBNS+"schemaLocation", premisNS + " http://www.loc.gov/standards/premis/v2/premis-v2-1.xsd")
                #rightsStatement.set("version", "2.1") #cvc-complex-type.3.2.2: Attribute 'version' is not allowed to appear in element 'rightsStatement'. 
                ret.append(rightsStatement)
                for i in range(len(key)):
                    valueDic[key[i]] = row[i]
                rightsStatementIdentifier = etree.SubElement(rightsStatement, "rightsStatementIdentifier")
                etree.SubElement(rightsStatementIdentifier, "rightsStatementIdentifierType").text = valueDic["rightsStatementIdentifierType"]
                etree.SubElement(rightsStatementIdentifier, "rightsStatementIdentifierValue").text = valueDic["rightsStatementIdentifierValue"]
                etree.SubElement(rightsStatement, "rightsBasis").text = valueDic["rightsBasis"]
                
                #copright information
                if valueDic["copyrightStatus"] != None and valueDic["copyrightStatus"] != "":
                    copyrightInformation = etree.SubElement(rightsStatement, "copyrightInformation")
                    etree.SubElement(copyrightInformation, "copyrightStatus").text = valueDic["copyrightStatus"]
                    etree.SubElement(copyrightInformation, "copyrightJurisdiction").text = valueDic["copyrightJurisdiction"]
                    etree.SubElement(copyrightInformation, "copyrightStatusDeterminationDate").text = formatDate(valueDic["copyrightStatusDeterminationDate"])
                    #TODO 4.1.3.4 copyrightNote (O, R)
                    #copyrightNote Repeatable
                
                # licenseInformation
                licenseInformation = etree.SubElement(rightsStatement, "licenseInformation")
                licenseIdentifier = etree.SubElement(licenseInformation, "licenseIdentifier")
                etree.SubElement(licenseIdentifier, "licenseIdentifierType").text = valueDic["licenseIdentifierType"]
                etree.SubElement(licenseIdentifier, "licenseIdentifierValue").text = valueDic["licenseIdentifierValue"]
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
        etree.SubElement(statuteInformation, "statuteInformationDeterminationDate").text = formatDate(row[3])
        
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
        termOfGrant = etree.SubElement(rightsGranted, "termOfGrant")
        etree.SubElement(termOfGrant, "startDate").text = formatDate(row[2])
        if not row[2]:  
            sharedVariablesAcrossModules.globalErrorCount +=1
            print >>sys.stderr, "The value '' of element 'startDate' is not valid. "
        if row[3]:
            etree.SubElement(termOfGrant, "endDate").text = formatDate(row[3])
        
        #TODO 4.1.6.4 rightsGrantedNote (O, R)
