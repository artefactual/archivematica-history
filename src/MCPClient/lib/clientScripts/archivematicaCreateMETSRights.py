#!/usr/bin/python -OO
#
# This file is part of Archivematica.
#
# Copyright 2010-2012 Artefactual Systems Inc. <http://artefactual.com>
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
import uuid
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
        list = "RightsStatement.pk, rightsStatementIdentifierType, rightsStatementIdentifierType, rightsStatementIdentifierValue, rightsBasis, copyrightStatus, copyrightJurisdiction, copyrightStatusDeterminationDate, licenseIdentifierType, licenseIdentifierValue, licenseTerms, rightsNotes, copyrightApplicableStartDate, copyrightApplicableEndDate, licenseApplicableStartDate, licenseApplicableEndDate"
        key = list.split(", ")
        sql = """SELECT %s FROM RightsStatement LEFT JOIN RightsStatementCopyright ON RightsStatementCopyright.fkRightsStatement = RightsStatement.pk LEFT JOIN RightsStatementLicense ON RightsStatementLicense.fkRightsStatement = RightsStatement.pk WHERE metadataAppliesToidentifier = '%s' AND metadataAppliesToType = %s;""" % (list, metadataAppliesToidentifier, metadataAppliesToType)
        rows = databaseInterface.queryAllSQL(sql)
        if not rows:
            continue
        else:
            for row in rows:
                valueDic= {}
                rightsStatement = etree.Element("rightsStatement", nsmap={None: premisNS})
                rightsStatement.set(xsiBNS+"schemaLocation", premisNS + " http://www.loc.gov/standards/premis/v2/premis-v2-2.xsd")
                #rightsStatement.set("version", "2.1") #cvc-complex-type.3.2.2: Attribute 'version' is not allowed to appear in element 'rightsStatement'.
                ret.append(rightsStatement)
                for i in range(len(key)):
                    valueDic[key[i]] = row[i]
                
                rightsStatementIdentifier = etree.SubElement(rightsStatement, "rightsStatementIdentifier")
                if valueDic["rightsStatementIdentifierValue"]:
                    etree.SubElement(rightsStatementIdentifier, "rightsStatementIdentifierType").text = valueDic["rightsStatementIdentifierType"]
                    etree.SubElement(rightsStatementIdentifier, "rightsStatementIdentifierValue").text = valueDic["rightsStatementIdentifierValue"]
                else:
                    etree.SubElement(rightsStatementIdentifier, "rightsStatementIdentifierType").text = "UUID"
                    etree.SubElement(rightsStatementIdentifier, "rightsStatementIdentifierValue").text = uuid.uuid4().__str__()
                etree.SubElement(rightsStatement, "rightsBasis").text = valueDic["rightsBasis"]
                
                #copright information
                if valueDic["rightsBasis"].lower() in ["copyright"]:
                    copyrightInformation = etree.SubElement(rightsStatement, "copyrightInformation")
                    etree.SubElement(copyrightInformation, "copyrightStatus").text = valueDic["copyrightStatus"]
                    etree.SubElement(copyrightInformation, "copyrightJurisdiction").text = valueDic["copyrightJurisdiction"]
                    etree.SubElement(copyrightInformation, "copyrightStatusDeterminationDate").text = formatDate(valueDic["copyrightStatusDeterminationDate"])
                    #copyrightNote Repeatable
                    sql = "SELECT copyrightNote FROM RightsStatementCopyrightNote WHERE fkRightsStatement = %d;" % (valueDic["RightsStatement.pk"])
                    rows2 = databaseInterface.queryAllSQL(sql)
                    for row2 in rows2:
                        etree.SubElement(copyrightInformation, "copyrightNote").text =  row2[0]
                        
                    #RightsStatementCopyrightDocumentationIdentifier
                    getDocumentationIdentifier(valueDic["RightsStatement.pk"], copyrightInformation)

                    copyrightApplicableDates = etree.SubElement(copyrightInformation, "copyrightApplicableDates")
                    if valueDic["copyrightApplicableStartDate"]:
                        etree.SubElement(copyrightApplicableDates, "startDate").text = formatDate(valueDic["copyrightApplicableStartDate"])
                    if valueDic["copyrightApplicableEndDate"]:
                        etree.SubElement(copyrightApplicableDates, "endDate").endDate = formatDate(valueDic["copyrightApplicableEndDate"])
                
                elif valueDic["rightsBasis"].lower() in ["license"]:
                    licenseInformation = etree.SubElement(rightsStatement, "licenseInformation")
                    
                    licenseDocumentIdentifier = etree.SubElement(licenseInformation, "licenseIdentifier")
                    etree.SubElement(licenseDocumentIdentifier, "licenseIdentifierType").text = valueDic["licenseIdentifierType"]
                    etree.SubElement(licenseDocumentIdentifier, "licenseIdentifierValue").text = valueDic["licenseIdentifierValue"]
                    #etree.SubElement(licenseDocumentIdentifier, "copyrightDocumentationRole").text = "unsupported?"
                    
                    etree.SubElement(licenseInformation, "licenseTerms").text = valueDic["licenseTerms"]
                    
                    sql = "SELECT licenseNote FROM RightsStatementLicenseNote WHERE fkRightsStatement = %d;" % (valueDic["RightsStatement.pk"])
                    rows2 = databaseInterface.queryAllSQL(sql)
                    for row2 in rows2:
                        etree.SubElement(licenseInformation, "licenseNote").text =  row2[0]
                        
                    licenseApplicableDates = etree.SubElement(licenseInformation, "licenseApplicableDates")
                    if valueDic["licenseApplicableStartDate"]:
                        etree.SubElement(licenseApplicableDates, "startDate").text = formatDate(valueDic["licenseApplicableStartDate"])
                    if valueDic["licenseApplicableEndDate"]:
                        etree.SubElement(licenseApplicableDates, "endDate").endDate = formatDate(valueDic["licenseApplicableEndDate"])
                    
                    
                    
                    

                elif valueDic["rightsBasis"].lower() in ["donor agreement", "policy"]:
                    otherRightsInformation = etree.SubElement(rightsStatement, "otherRightsInformation")
                    #RightsStatementotherRightsDocumentationIdentifier
                    getDocumentationIdentifier(valueDic["RightsStatement.pk"], otherRightsInformation)

                    otherRightsApplicableDates = etree.SubElement(otherRightsInformation, "otherRightsApplicableDates")
                    if valueDic["copyrightApplicableStartDate"]:
                        etree.SubElement(otherRightsApplicableDates, "startDate").text = formatDate(valueDic["copyrightApplicableStartDate"])
                    if valueDic["copyrightApplicableEndDate"]:
                        etree.SubElement(otherRightsApplicableDates, "endDate").endDate = formatDate(valueDic["copyrightApplicableEndDate"])

                    #otherRightsNote Repeatable
                    sql = "SELECT copyrightNote FROM RightsStatementCopyrightNote WHERE fkRightsStatement = %d;" % (valueDic["RightsStatement.pk"])
                    rows2 = databaseInterface.queryAllSQL(sql)
                    for row2 in rows2:
                        etree.SubElement(otherRightsInformation, "otherRightsNote").text =  row2[0]

                elif valueDic["rightsBasis"].lower() in ["statute"]:
                    print "not implemented yet"        
                                    
                        
                    
                # licenseInformation
                #if valueDic["rightsBasis"].lower() in ["allow"]:
                #licenseInformation = etree.SubElement(rightsStatement, "licenseInformation")
                #licenseIdentifier = etree.SubElement(licenseInformation, "licenseIdentifier")
                #etree.SubElement(licenseIdentifier, "licenseIdentifierType").text = valueDic["licenseIdentifierType"]
                #etree.SubElement(licenseIdentifier, "licenseIdentifierValue").text = valueDic["licenseIdentifierValue"]
                #etree.SubElement(licenseInformation, "licenseTerms").text = valueDic["licenseTerms"]
                
                #4.1.4.3 licenseNote (O, R)
                #sql = "SELECT licenseNote FROM RightsStatementLicenseNote WHERE fkRightsStatement = %d;" % (valueDic["RightsStatement.pk"])
                #rows2 = databaseInterface.queryAllSQL(sql)
                #for row2 in rows2:
                #    etree.SubElement(licenseInformation, "licenseNote").text =  row2[0]

                #4.1.5 statuteInformation (O, R)
                getstatuteInformation(valueDic["RightsStatement.pk"], rightsStatement)

                #4.1.6 rightsGranted (O, R)
                getrightsGranted(valueDic["RightsStatement.pk"], rightsStatement, valueDic["rightsNotes"])

                #4.1.7 linkingObjectIdentifier (O, R)
                linkingObjectIdentifier = etree.SubElement(rightsStatement, "linkingObjectIdentifier")
                etree.SubElement(linkingObjectIdentifier, "linkingObjectIdentifierType").text = "UUID"
                etree.SubElement(linkingObjectIdentifier, "linkingObjectIdentifierValue").text = fileUUID


                #4.1.8 linkingAgentIdentifier (O, R)
                #sql = """SELECT agentIdentifierType, agentIdentifierValue, agentName, agentType FROM Agents;"""
                #c, sqlLock = databaseInterface.querySQL(sql)
                #row = c.fetchone()
                #while row != None:
                #    linkingAgentIdentifier = etree.SubElement(rightsStatement, "linkingAgentIdentifier")
                #    etree.SubElement(linkingAgentIdentifier, "linkingAgentIdentifierType").text = row[0]
                #    etree.SubElement(linkingAgentIdentifier, "linkingAgentIdentifierValue").text = row[1]
                #    row = c.fetchone()
                #sqlLock.release()
            if False: # Issue 873:
                break
    return ret

def getDocumentationIdentifier(pk, parent):
    sql = "SELECT pk, copyrightDocumentationIdentifierType, copyrightDocumentationIdentifierValue, copyrightDocumentationIdentifierRole FROM RightsStatementCopyrightDocumentationIdentifier WHERE fkRightsStatement = %d" % (pk)
    rows = databaseInterface.queryAllSQL(sql)
    for row in rows:
        statuteInformation = etree.SubElement(parent, "copyrightDocumentationIdentifier")
        etree.SubElement(statuteInformation, "copyrightDocumentationIdentifierType").text = row[1]
        etree.SubElement(statuteInformation, "copyrightDocumentationIdentifierValue").text = row[2]
        etree.SubElement(statuteInformation, "copyrightDocumentationRole").text = row[3]


def getstatuteInformation(pk, parent):
    sql = "SELECT pk, statuteJurisdiction, statuteCitation, statuteInformationDeterminationDate FROM RightsStatementStatuteInformation WHERE fkRightsStatement = %d" % (pk)
    rows = databaseInterface.queryAllSQL(sql)
    for row in rows:
        statuteInformation = etree.SubElement(parent, "statuteInformation")
        etree.SubElement(statuteInformation, "statuteJurisdiction").text = row[1]
        etree.SubElement(statuteInformation, "statuteCitation").text = row[2]
        etree.SubElement(statuteInformation, "statuteInformationDeterminationDate").text = formatDate(row[3])

        #statuteNote Repeatable
        sql = "SELECT statuteNote FROM RightsStatementStatuteInformationNote WHERE fkRightsStatement = %d;" % (row[0])
        rows2 = databaseInterface.queryAllSQL(sql)
        for row2 in rows2:
            etree.SubElement(statuteInformation, "statuteNote").text =  row2[0]

def getrightsGranted(pk, parent, rightsGrantedNote=""):
    sql = "SELECT pk, act, startDate, endDate, restriction FROM RightsStatementRightsGranted WHERE fkRightsStatement = %d" % (pk)
    rows = databaseInterface.queryAllSQL(sql)
    for row in rows:
        rightsGranted = etree.SubElement(parent, "rightsGranted")
        restriction = row[4]
        #TODO : Issue 860:    rights granted restriction is a repeatable field.
        #http://code.google.com/p/archivematica/issues/detail?id=860
        etree.SubElement(rightsGranted, "act").text = row[1]
        etree.SubElement(rightsGranted, "restriction").text = restriction
        if restriction.lower() in ["allow"]:
            termOfGrant = etree.SubElement(rightsGranted, "termOfGrant")
        elif restriction.lower() in ["disallow", "conditional"]:
            termOfGrant = etree.SubElement(rightsGranted, "termOfRestriction")
        else:
            print >>sys.stderr, "The value of element restriction must be: 'Allow', 'Dissallow', or 'Conditional'"
            sharedVariablesAcrossModules.globalErrorCount +=1
            continue
        etree.SubElement(termOfGrant, "startDate").text = formatDate(row[2])
        if not row[2]:
            sharedVariablesAcrossModules.globalErrorCount +=1
            print >>sys.stderr, "The value '' of element 'startDate' is not valid. "
        if row[3]:
            etree.SubElement(termOfGrant, "endDate").text = formatDate(row[3])
        # cvc-datatype-valid.1.2.3: 'open' is not a valid value of union type 'edtfSimpleType'.
        #else:
        #    etree.SubElement(termOfGrant, "endDate").text = "open"
        if rightsGrantedNote:
            etree.SubElement(rightsGranted, "rightsGrantedNote").text =  rightsGrantedNote
        #4.1.6.4 rightsGrantedNote (O, R)
        sql = "SELECT rightsGrantedNote FROM RightsStatementRightsGrantedNote WHERE fkRightsStatementRightsGranted = %d;" % (row[0])
        rows2 = databaseInterface.queryAllSQL(sql)
        for row2 in rows2:
            etree.SubElement(rightsGranted, "rightsGrantedNote").text =  row2[0]
