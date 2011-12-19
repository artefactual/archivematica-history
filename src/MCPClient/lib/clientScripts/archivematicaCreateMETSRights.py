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


def archivematicaGetRights(metadataAppliesToList):
    """[(fileUUID, fileUUIDTYPE), (sipUUID, sipUUIDTYPE), (transferUUID, transferUUIDType)]"""
    ret = []
    for metadataAppliesToidentifier, metadataAppliesToType in metadataAppliesToList:
        list = "pk, rightsStatementIdentifier, rightsStatementIdentifierType, rightsStatementIdentifierValue, rightsBasis, copyrightInformation, copyrightStatus, copyrightJurisdiction, copyrightStatusDeterminationDate, licenseInformation LONGTEXT, licenseIdentifier, licenseIdentifierType, licenseIdentifierValue, licenseTerms"
        key = list.split(", ")
        sql = """SELECT %s FROM RightsStatement WHERE metadataAppliesToidentifier = '%s' AND metadataAppliesToType = '%s';""" % (list, metadataAppliesToidentifier, metadataAppliesToType)
        databaseInterface.
        if not rows:
            continue
        else:
            for row in rows:
                valueDic= {}
                rightsStatement = etree.Element("rightsStatement")
                ret.append(rightsStatement)
                for i in range(len(key)):
                    valueDic[key[i]] = row[i]
                rightsStatementIdentifier = etree.SubElement(rightsStatement, "rightsStatementIdentifier")
                etree.SubElement(rightsStatementIdentifier, "rightsStatementIdentiferType").text = valueDic["rightsStatementIdentiferType"]
                etree.SubElement(rightsStatementIdentifier, "rightsStatementIdentifierValue").text = valueDic["rightsStatementIdentifierValue"]

                etree.SubElement(rightsStatement, "rightsBasis").text = valueDic["rightsBasis"]
                "rightsBasis, copyrightInformation, copyrightStatus, copyrightJurisdiction, copyrightStatusDeterminationDate, licenseInformation LONGTEXT, licenseIdentifier, licenseIdentifierType, licenseIdentifierValue, licenseTerms"
            break
    return ret
"""
-- rightsStatement (O, R)
DROP TABLE IF EXISTS RightsStatement;
CREATE TABLE RightsStatement (
    pk INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    rightsStatementIdentifier LONGTEXT NOT NULL,
    rightsStatementIdentifierType LONGTEXT NOT NULL,
    rightsStatementIdentifierValue LONGTEXT NOT NULL,
    rightsBasis LONGTEXT NOT NULL,
    copyrightInformation LONGTEXT,
    copyrightStatus LONGTEXT NOT NULL,
    copyrightJurisdiction LONGTEXT NOT NULL,
    copyrightStatusDeterminationDate LONGTEXT,
    licenseInformation LONGTEXT,
    licenseIdentifier LONGTEXT,
    licenseIdentifierType LONGTEXT NOT NULL,
    licenseIdentifierValue LONGTEXT NOT NULL,
    licenseTerms LONGTEXT
);



/*
Entity semantic units
4.1
rightsStatement (O, R)
4.1.1 rightsStatementIdentifier (M, NR)
4.1.1.1 rightsStatementIdentifierType (M, NR)
4.1.1.2 rightsStatementIdentifierValue (M, NR)
4.1.2 rightsBasis (M, NR)
4.1.3 copyrightInformation (O, NR)
4.1.3.1 copyrightStatus (M, NR)
4.1.3.2 copyrightJurisdiction (M, NR)
4.1.3.3 copyrightStatusDeterminationDate (O, NR)
4.1.3.4 copyrightNote (O, R)
4.1.4 licenseInformation (O, NR)
4.1.4.1 licenseIdentifier (O, NR)
4.1.4.1.1 licenseIdentifierType (M, NR)
4.1.4.1.2 licenseIdentifierValue (M, NR)
4.1.4.2 licenseTerms (O, NR)
4.1.4.3 licenseNote (O, R)
4.1.5 statuteInformation (O, R)
4.1.5.1 statuteJurisdiction (M, NR)
Data Dictionary for Preservation Metadata: PREMIS version 2.1
165
THE PREMIS DATA DICTIONARY
4.2
166
4.1.5.2 statuteCitation (M, NR)
4.1.5.3 statuteInformationDeterminationDate (O, NR)
4.1.5.4 statuteNote (O, R)
4.1.6 rightsGranted (O, R)
4.1.6.1 act (M, NR)
4.1.6.2 restriction (O, R)
4.1.6.3 termOfGrant (M, NR)
4.1.6.3.1 startDate (M, NR)
4.1.6.3.2 endDate (O, NR)
4.1.6.4 rightsGrantedNote (O, R)
4.1.7 linkingObjectIdentifier (O, R)
4.1.7.1 linkingObjectIdentifierType (M, NR)
4.1.7.2 linkingObjectIdentifierValue (M, NR)
4.1.7.3 linkingObjectRole (O, R)
4.1.8 linkingAgentIdentifier (O, R)
4.1.8.1 linkingAgentIdentifierType (M, NR)
4.1.8.2 linkingAgentIdentifierValue (M, NR)
4.1.8.3 linkingAgentRole (O, R)
rightsExtension (O, R)




<premis>
  <rights>
    <rightsStatement>
      <rightsStatementIdentifier>
        <rightsStatementIdentiferType>UUID</rightsStatementIdentiferType>
        <rightsStatementIdentifierValue>14cbad80-70nd-4f46-887f-k1gv7f9f30h6</rightsStatementIdentifierValue>
      </rightsStatementIdentifier>
      <rightsBasis>License</rightsBasis>
      <copyrightInformation>
        <copyrightStatus></copyrightStatus>
        <copyrightJurisdiction></copyrightJurisdiction>
        <copyrightStatusDeterminationDate></copyrightStatusDeterminationDate>
        <copyrightNote></copyrightNote>
      </copyrightInformation>
      <licenseInformation>
        <licenseIdentifier>
          <licenseIdentifierType>UUID</licenseIdentifierType>
          <licenseIdentifierValue>d3e828fb-e6f1-40b6-a3c5-839773b35755</licenseIdentifierValue>
        </licenseIdentifier>
        <licenseTerms>This file is licensed under the Creative Commons Attribution-Share Alike 3.0 Unported license</licenseTerms>
        <licenseNote></licenseNote>
      </licenseInformation>
      <statuteInformation>
        <statuteJurisdiction></statuteJurisdiction>
        <statuteCitation></statuteCitation>
        <statuteInformationDeterminationDate></statuteInformationDeterminationDate>
        <statuteNote></statuteNote>
      </statuteInformation>
      <rightsGranted>
        <act>Disseminate</act>
        <restriction>Allow</restriction>
        <termOfGrant>
          <startDate>2011-09-16</startDate>
          <endDate>open</endDate>
        </termOfGrant>
        <rightsGrantedNote>Attribution required</rightsGrantedNote>
      </rightsGranted>
        <linkingObjectIdentifier>
        <linkingObjectIdentifierType>UUID</linkingObjectIdentifierType>
        <linkingObjectIdentifierValue>52cbad80-70fd-4f46-887f-a1be7f9f30e0</linkingObjectIdentifierValue>
      </linkingObjectIdentifier>
      <linkingAgentIdentifier> *Repeatable
        <linkingAgentIdentifierType></linkingAgentIdentifierType>
        <linkingAgentIdentifierValue></linkingAgentIdentifierValue>
        <linkingAgentRole></linkingAgentRole>
      </linkingAgentIdentifier>
    </rightsStatement>
  </rights>
</premis>
*/

DROP TABLE IF EXISTS ArchivematicaRightsStatement;
CREATE TABLE ArchivematicaRightsStatement (
    pk              INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    metadataAppliesToType  INT,
    Foreign Key (metadataAppliesToType) references MetadataAppliesToTypes(pk),
    metadataAppliesToidentifier      VARCHAR(50),
    fkRightsStatement INT UNSIGNED,
    Foreign Key (fkRightsStatement) references RightsStatement(pk)
);

-- rightsExtension (O, R) ??? --

-- 4.1.3.4 copyrightNote (O, R)
DROP TABLE IF EXISTS RightsStatementCopyrightNote;
CREATE TABLE RightsStatementCopyrightNote (
    pk INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    fkRightsStatement INT UNSIGNED,
    Foreign Key (fkRightsStatement) references RightsStatement(pk),
    copyrightNote LONGTEXT NOT NULL
);

-- 4.1.4.3 licenseNote (O, R)
DROP TABLE IF EXISTS RightsStatementLicenseNote;
CREATE TABLE RightsStatementLicenseNote (
    pk INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    fkRightsStatement INT UNSIGNED,
    Foreign Key (fkRightsStatement) references RightsStatement(pk),
    licenseNote LONGTEXT NOT NULL
);


-- 4.1.5 statuteInformation (O, R)
DROP TABLE IF EXISTS RightsStatementStatuteInformation;
CREATE TABLE RightsStatementStatuteInformation (
    pk INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    fkRightsStatement INT UNSIGNED,
    Foreign Key (fkRightsStatement) references RightsStatement(pk),
    statuteJurisdiction LONGTEXT NOT NULL,
    statuteCitation LONGTEXT NOT NULL,
    statuteInformationDeterminationDate LONGTEXT

);

-- 4.1.5.4 statuteNote (O, R)
DROP TABLE IF EXISTS RightsStatementStatuteInformationStatuteNote;
CREATE TABLE RightsStatementStatuteInformationStatuteNote (
    pk INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    fkRightsStatementStatuteInformation INT UNSIGNED,
    Foreign Key (fkRightsStatementStatuteInformation) references RightsStatementStatuteInformation(pk),
    statuteNote LONGTEXT NOT NULL
);


/*
USING - ArchivematicaRightsStatement TABLE
-- 4.1.7 linkingObjectIdentifier (O, R)
DROP TABLE IF EXISTS RightsStatementLinkingObjectIdentifier;
CREATE TABLE RightsStatementLinkingObjectIdentifier (
    pk INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    fkRightsStatement INT UNSIGNED,
    Foreign Key (fkRightsStatement) references RightsStatement(pk),
    linkingObjectIdentifierType LONGTEXT NOT NULL,
    linkingObjectIdentifierValue LONGTEXT NOT NULL
);

-- 4.1.7.? LinkingObjectRole (O, R)
DROP TABLE IF EXISTS RightsStatementLinkingObjectIdentifierLinkingObjectRole;
CREATE TABLE RightsStatementLinkingObjectIdentifierLinkingObjectRole (
    pk INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    fkRightsStatementLinkingObjectIdentifier INT UNSIGNED,
    Foreign Key (fkRightsStatementLinkingObjectIdentifier) references RightsStatementLinkingObjectIdentifier(pk),
    LinkingObjectRole LONGTEXT NOT NULL
);
*/

-- linkingAgentIdentifier (O, R)
DROP TABLE IF EXISTS RightsStatementLinkingAgentIdentifier;
CREATE TABLE RightsStatementLinkingAgentIdentifier (
    pk INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    fkRightsStatement INT UNSIGNED,
    Foreign Key (fkRightsStatement) references RightsStatement(pk),
    linkingAgentIdentifierType LONGTEXT NOT NULL,
    linkingAgentIdentifierValue LONGTEXT NOT NULL
);

-- 4.1.8.3 linkingAgentRole (O, R)
DROP TABLE IF EXISTS RightsStatementLinkingAgentIdentifierLinkingAgentRole;
CREATE TABLE RightsStatementLinkingAgentIdentifierLinkingAgentRole (
    pk INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    fkRightsStatementLinkingAgentIdentifier INT UNSIGNED,
    Foreign Key (fkRightsStatementLinkingAgentIdentifier) references RightsStatementLinkingAgentIdentifier(pk),
    linkingAgentRole LONGTEXT NOT NULL
);

-- 4.1.6 rightsGranted (O, R)
DROP TABLE IF EXISTS RightsStatementRightsGranted;
CREATE TABLE RightsStatementRightsGranted (
    pk INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    fkRightsStatement INT UNSIGNED,
    Foreign Key (fkRightsStatement) references RightsStatement(pk),
    act LONGTEXT NOT NULL,
    termOfGrant LONGTEXT NOT NULL,
    startDate LONGTEXT NOT NULL,
    endDate LONGTEXT
);

-- 4.1.6.2 restriction (O, R)
DROP TABLE IF EXISTS RightsStatementRightsGrantedRestriction;
CREATE TABLE RightsStatementRightsGrantedRestriction (
    pk INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    fkRightsStatementRightsGranted INT UNSIGNED,
    Foreign Key (fkRightsStatementRightsGranted) references RightsStatementRightsGranted(pk),
    restriction LONGTEXT
);
-- 4.1.6.4 rightsGrantedNote (O, R)
DROP TABLE IF EXISTS RightsStatementRightsGrantedRestriction;
CREATE TABLE RightsStatementRightsGrantedRestriction (
    pk INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    fkRightsStatementRightsGranted INT UNSIGNED,
    Foreign Key (fkRightsStatementRightsGranted) references RightsStatementRightsGranted(pk),
    rightsGrantedNote LONGTEXT
);"""


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
