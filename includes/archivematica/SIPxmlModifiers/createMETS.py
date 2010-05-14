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
# @author Peter Van Garderen <peter@artefactual.com>
# @version svn: $Id$

import xml.etree.ElementTree as etree
from datetime import datetime

root = etree.Element("mets")
root.text = "\n\t"
root.set("xmlns:mets", "http://www.loc.gov/METS/")
root.set("xmlns:premis", "info:lc/xmlns/premis-v2")
root.set("xmlns:dcterms", "http://purl.org/dc/terms/")
root.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
root.set("xsi:schemaLocation", "http://www.loc.gov/METS/ http://www.loc.gov/standards/mets/version18/mets.xsd info:lc/xmlns/premis-v2 http://www.loc.gov/standards/premis/premis.xsd http://purl.org/dc/terms/ http://dublincore.org/schemas/xmls/qdc/2008/02/11/dcterms.xsd")

dmdSecSIP = etree.Element("dmdSec")
dmdSecSIP.text = "\n\t\t"
dmdSecSIP.tail = "\n"
dmdSecSIP.set("ID", "SIP-description")
root.append(dmdSecSIP)

dmdSecMdWrap1 = etree.Element("mdWrap")
dmdSecMdWrap1.text = "\n\t\t"
dmdSecMdWrap1.tail = "\n"
dmdSecSIP.append(dmdSecMdWrap1)

dmdSecXmlData1 = etree.Element("xmlData")
dmdSecXmlData1.text = "\n\t\t"
dmdSecXmlData1.tail = "\n"
dmdSecMdWrap1.append(dmdSecXmlData1)

dublinCore = etree.Element("dublincore")
dublinCore.text = "\n\t\t"
dublinCore.tail = "\n"
dublinCore.set("xmlns:dcterms", "http://purl.org/dc/terms/")
dublinCore.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
dublinCore.set("xsi:schemaLocation", "http://purl.org/dc/terms/ http://dublincore.org/schemas/xmls/qdc/2008/02/11/dcterms.xsd")
dmdSecXmlData1.append(dublinCore)

dcTitle = etree.Element("dcterms:title")
dcTitle.text = " "
dcTitle.tail = "\n\t\t"
dublinCore.append(dcTitle)

dcCreator = etree.Element("dcterms:creator")
dcCreator.text = " "
dcCreator.tail = "\n\t\t"
dublinCore.append(dcCreator)

dcSubject = etree.Element("dcterms:subject")
dcSubject.text = " "
dcSubject.tail = "\n\t\t"
dublinCore.append(dcSubject)

dcDescription = etree.Element("dcterms:description")
dcDescription.text = " "
dcDescription.tail = "\n\t\t"
dublinCore.append(dcDescription)

dcPublisher = etree.Element("dcterms:publisher")
dcPublisher.text = " "
dcPublisher.tail = "\n\t\t"
dublinCore.append(dcPublisher)

dcContributor = etree.Element("dcterms:contributor")
dcContributor.text = " "
dcContributor.tail = "\n\t\t"
dublinCore.append(dcContributor)

dcDate = etree.Element("dcterms:date")
dcDate.text = " "
dcDate.tail = "\n\t\t"
dublinCore.append(dcDate)

dcType = etree.Element("dcterms:type")
dcType.text = " "
dcType.tail = "\n\t\t"
dublinCore.append(dcType)

dcFormat = etree.Element("dcterms:format")
dcFormat.text = " "
dcFormat.tail = "\n\t\t"
dublinCore.append(dcFormat)

dcIdentifier = etree.Element("dcterms:identifier")
dcIdentifier.text = " "
dcIdentifier.tail = "\n\t\t"
dublinCore.append(dcIdentifier)

dcSource = etree.Element("dcterms:source")
dcSource.text = " "
dcSource.tail = "\n\t\t"
dublinCore.append(dcSource)

dcLanguage = etree.Element("dcterms:language")
dcLanguage.text = " "
dcLanguage.tail = "\n\t\t"
dublinCore.append(dcLanguage)

dcRelation = etree.Element("dcterms:relation")
dcRelation.text = " "
dcRelation.tail = "\n\t\t"
dublinCore.append(dcRelation)

dcCoverage = etree.Element("dcterms:coverage")
dcCoverage.text = " "
dcCoverage.tail = "\n\t\t"
dublinCore.append(dcCoverage)

dcRights = etree.Element("dcterms:rights")
dcRights.text = " "
dcRights.tail = "\n\t\t"
dublinCore.append(dcRights)

dcAlternative = etree.Element("dcterms:alternative")
dcAlternative.text = " "
dcAlternative.tail = "\n\t\t"
dublinCore.append(dcAlternative)

dcTOC = etree.Element("dcterms:tableOfContents")
dcTOC.text = " "
dcTOC.tail = "\n\t\t"
dublinCore.append(dcTOC)

dcAbstract = etree.Element("dcterms:abstract")
dcAbstract.text = " "
dcAbstract.tail = "\n\t\t"
dublinCore.append(dcAbstract)

dcCreated = etree.Element("dcterms:created")
dcCreated.text = " "
dcCreated.tail = "\n\t\t"
dublinCore.append(dcCreated)

dcValid = etree.Element("dcterms:valid")
dcValid.text = " "
dcValid.tail = "\n\t\t"
dublinCore.append(dcValid)

dcAvailable = etree.Element("dcterms:available")
dcAvailable.text = " "
dcAvailable.tail = "\n\t\t"
dublinCore.append(dcAvailable)

dcIssued = etree.Element("dcterms:issued")
dcIssued.text = " "
dcIssued.tail = "\n\t\t"
dublinCore.append(dcIssued)

dcModified = etree.Element("dcterms:modified")
dcModified.text = " "
dcModified.tail = "\n\t\t"
dublinCore.append(dcModified)

dcDateAccepted = etree.Element("dcterms:dateAccepted")
dcDateAccepted.text = " "
dcDateAccepted.tail = "\n\t\t"
dublinCore.append(dcDateAccepted)

dcDateCopyrighted = etree.Element("dcterms:dateCopyrighted")
dcDateCopyrighted.text = " "
dcDateCopyrighted.tail = "\n\t\t"
dublinCore.append(dcDateCopyrighted)

dcDateSubmitted = etree.Element("dcterms:dateSubmitted")
dcDateSubmitted.text = " "
dcDateSubmitted.tail = "\n\t\t"
dublinCore.append(dcDateSubmitted)

dcExtent = etree.Element("dcterms:extent")
dcExtent.text = " "
dcExtent.tail = "\n\t\t"
dublinCore.append(dcExtent)

dcMedium = etree.Element("dcterms:medium")
dcMedium.text = " "
dcMedium.tail = "\n\t\t"
dublinCore.append(dcMedium)

dcIsVersionOf = etree.Element("dcterms:isVersionOf")
dcIsVersionOf.text = " "
dcIsVersionOf.tail = "\n\t\t"
dublinCore.append(dcIsVersionOf)

dcHasVersion = etree.Element("dcterms:hasVersion")
dcHasVersion.text = " "
dcHasVersion.tail = "\n\t\t"
dublinCore.append(dcHasVersion)

dcIsReplacedBy = etree.Element("dcterms:isReplacedBy")
dcIsReplacedBy.text = " "
dcIsReplacedBy.tail = "\n\t\t"
dublinCore.append(dcIsReplacedBy)

dcReplaces = etree.Element("dcterms:replaces")
dcReplaces.text = " "
dcReplaces.tail = "\n\t\t"
dublinCore.append(dcReplaces)

dcIsRequiredBy = etree.Element("dcterms:isRequiredBy")
dcIsRequiredBy.text = " "
dcIsRequiredBy.tail = "\n\t\t"
dublinCore.append(dcIsRequiredBy)

dcRequires = etree.Element("dcterms:requires")
dcRequires.text = " "
dcRequires.tail = "\n\t\t"
dublinCore.append(dcRequires)

dcIsPartOf = etree.Element("dcterms:isPartOf")
dcIsPartOf.text = " "
dcIsPartOf.tail = "\n\t\t"
dublinCore.append(dcIsPartOf)

dcHasPart = etree.Element("dcterms:hasPart")
dcHasPart.text = " "
dcHasPart.tail = "\n\t\t"
dublinCore.append(dcHasPart)

dcIsReferencedBy = etree.Element("dcterms:isReferencedBy")
dcIsReferencedBy.text = " "
dcIsReferencedBy.tail = "\n\t\t"
dublinCore.append(dcIsReferencedBy)

dcReferences = etree.Element("dcterms:references")
dcReferences.text = " "
dcReferences.tail = "\n\t\t"
dublinCore.append(dcReferences)

dcIsFormatOf = etree.Element("dcterms:isFormatOf")
dcIsFormatOf.text = " "
dcIsFormatOf.tail = "\n\t\t"
dublinCore.append(dcIsFormatOf)

dcConformsTo = etree.Element("dcterms:conformsTo")
dcConformsTo.text = " "
dcConformsTo.tail = "\n\t\t"
dublinCore.append(dcConformsTo)

dcSpatial = etree.Element("dcterms:spatial")
dcSpatial.text = " "
dcSpatial.tail = "\n\t\t"
dublinCore.append(dcSpatial)

dcTemporal = etree.Element("dcterms:temporal")
dcTemporal.text = " "
dcTemporal.tail = "\n\t\t"
dublinCore.append(dcTemporal)

dcAudience = etree.Element("dcterms:audience")
dcAudience.text = " "
dcAudience.tail = "\n\t\t"
dublinCore.append(dcAudience)

dcAccrualMethod = etree.Element("dcterms:accrualMethod")
dcAccrualMethod.text = " "
dcAccrualMethod.tail = "\n\t\t"
dublinCore.append(dcAccrualMethod)

dcAccrualPeriodicity = etree.Element("dcterms:accrualPeriodicity")
dcAccrualPeriodicity.text = " "
dcAccrualPeriodicity.tail = "\n\t\t"
dublinCore.append(dcAccrualPeriodicity)

dcAccrualPolicy = etree.Element("dcterms:accrualPolicy")
dcAccrualPolicy.text = " "
dcAccrualPolicy.tail = "\n\t\t"
dublinCore.append(dcAccrualPolicy)

dcInstructionalMethod = etree.Element("dcterms:instructionalMethod")
dcInstructionalMethod.text = " "
dcInstructionalMethod.tail = "\n\t\t"
dublinCore.append(dcInstructionalMethod)

dcProvenance = etree.Element("dcterms:Provenance")
dcProvenance.text = " "
dcProvenance.tail = "\n\t\t"
dublinCore.append(dcProvenance)

dcRightsHolder = etree.Element("dcterms:rightsHolder")
dcRightsHolder.text = " "
dcRightsHolder.tail = "\n\t\t"
dublinCore.append(dcRightsHolder)

dcMediator = etree.Element("dcterms:mediator")
dcMediator.text = " "
dcMediator.tail = "\n\t\t"
dublinCore.append(dcMediator)

dcEducationLevel = etree.Element("dcterms:educationLevel")
dcEducationLevel.text = " "
dcEducationLevel.tail = "\n\t\t"
dublinCore.append(dcEducationLevel)

dcAccessRights = etree.Element("dcterms:accessRights")
dcAccessRights.text = " "
dcAccessRights.tail = "\n\t\t"
dublinCore.append(dcAccessRights)

dcLicense = etree.Element("dcterms:license")
dcLicense.text = " "
dcLicense.tail = "\n\t\t"
dublinCore.append(dcLicense)

dcBibliographicCitation = etree.Element("dcterms:bibliographicCitation")
dcBibliographicCitation.text = " "
dcBibliographicCitation.tail = "\n\t\t"
dublinCore.append(dcBibliographicCitation)

amdSec = etree.Element("amdSec")
amdSec.text = "\n\t\t"
amdSec.tail = "\n"
root.append(amdSec)

digiprovMD = etree.Element("digiprovMD")
digiprovMD.text = "\n\t\t"
digiprovMD.tail = "\n"
amdSec.append(digiprovMD)

fileSec = etree.Element("fileSec")
fileSec.text = "\n\t\t"
fileSec.tail = "\n"
root.append(fileSec)

structMap = etree.Element("structMap")
structMap.text = "\n\t\t"
structMap.tail = "\n"
structMap.set("TYPE", "Physical")
root.append(structMap)

structMapDiv1 = etree.Element("div")
structMapDiv1.text = "\n\t\t"
structMapDiv1.tail = "\n"
#TODO: add SIP $UUID as ID value
structMapDiv1.set("ID", "TODO: SIP $UUID")
#TODO: add SIP Directory Name as LABEL value
structMapDiv1.set("LABEL", "TODO: SIP directory name")
structMapDiv1.set("TYPE", "SIP Contents")
structMapDiv1.set("DMDID", "SIP-description")
structMap.append(structMapDiv1)

#TODO:add these two elements for each file in the directory
# <-- begin loop
structMapDiv2 = etree.Element("div")
structMapDiv2.text = "\n\t\t"
structMapDiv2.tail = "\n"
structMapDiv1.set("TYPE", "Object")
structMapDiv1.append(structMapDiv2)

structMapFptr = etree.Element("fptr")
structMapFptr.text = "\n\t\t"
structMapFptr.tail = "\n"
#TODO: add File $UUID as FILEID value
structMapFptr.set("FILEID", "TODO: file $UUID")
structMapDiv2.append(structMapFptr)
# end loop -->






tree = etree.ElementTree(root)
tree.write("METS.xml")
