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

from archivematicaLoadConfig import loadConfig
import lxml.etree as etree
from datetime import datetime
from archivematicaXMLNamesSpace import *

dublinCore = etree.Element( "dublincore", \
    nsmap = NSMAP, \
    attrib = { "{" + xsiNS + "}schemaLocation" : "http://purl.org/dc/terms/ http://dublincore.org/schemas/xmls/qdc/2008/02/11/dcterms.xsd" }) 
dublinCore.text = "\n\t"
dublinCore.tail = "\n"

dcTitle = etree.Element(dcterms + "title", nsmap=NSMAP) 
dcTitle.text = " "
dcTitle.tail = "\n\t"
dublinCore.append(dcTitle)

dcCreator = etree.Element(dcterms + "creator", nsmap=NSMAP) 
dcCreator.text = " "
dcCreator.tail = "\n\t"
dublinCore.append(dcCreator)

dcSubject = etree.Element(dcterms + "subject", nsmap=NSMAP) 
dcSubject.text = " "
dcSubject.tail = "\n\t"
dublinCore.append(dcSubject)

dcDescription = etree.Element(dcterms + "description", nsmap=NSMAP) 
dcDescription.text = " "
dcDescription.tail = "\n\t"
dublinCore.append(dcDescription)

dcPublisher = etree.Element(dcterms + "publisher", nsmap=NSMAP) 
dcPublisher.text = " "
dcPublisher.tail = "\n\t"
dublinCore.append(dcPublisher)

dcContributor = etree.Element(dcterms + "contributor", nsmap=NSMAP) 
dcContributor.text = " "
dcContributor.tail = "\n\t"
dublinCore.append(dcContributor)

dcDate = etree.Element(dcterms + "date", nsmap=NSMAP) 
dcDate.text = " "
dcDate.tail = "\n\t"
dublinCore.append(dcDate)

dcType = etree.Element(dcterms + "type", nsmap=NSMAP) 
dcType.text = " "
dcType.tail = "\n\t"
dublinCore.append(dcType)

dcFormat = etree.Element(dcterms + "format", nsmap=NSMAP) 
dcFormat.text = " "
dcFormat.tail = "\n\t"
dublinCore.append(dcFormat)

dcIdentifier = etree.Element(dcterms + "identifier", nsmap=NSMAP) 
dcIdentifier.text = " "
dcIdentifier.tail = "\n\t"
dublinCore.append(dcIdentifier)

dcSource = etree.Element(dcterms + "source", nsmap=NSMAP) 
dcSource.text = " "
dcSource.tail = "\n\t"
dublinCore.append(dcSource)

dcLanguage = etree.Element(dcterms + "language", nsmap=NSMAP) 
dcLanguage.text = " "
dcLanguage.tail = "\n\t"
dublinCore.append(dcLanguage)

dcRelation = etree.Element(dcterms + "relation", nsmap=NSMAP) 
dcRelation.text = " "
dcRelation.tail = "\n\t"
dublinCore.append(dcRelation)

dcCoverage = etree.Element(dcterms + "coverage", nsmap=NSMAP) 
dcCoverage.text = " "
dcCoverage.tail = "\n\t"
dublinCore.append(dcCoverage)

dcRights = etree.Element(dcterms + "rights", nsmap=NSMAP) 
dcRights.text = " "
dcRights.tail = "\n\t"
dublinCore.append(dcRights)

dcAlternative = etree.Element(dcterms + "alternative", nsmap=NSMAP) 
dcAlternative.text = " "
dcAlternative.tail = "\n\t"
dublinCore.append(dcAlternative)

dcTOC = etree.Element(dcterms + "tableOfContents", nsmap=NSMAP) 
dcTOC.text = " "
dcTOC.tail = "\n\t"
dublinCore.append(dcTOC)

dcAbstract = etree.Element(dcterms + "abstract", nsmap=NSMAP) 
dcAbstract.text = " "
dcAbstract.tail = "\n\t"
dublinCore.append(dcAbstract)

dcCreated = etree.Element(dcterms + "created", nsmap=NSMAP) 
dcCreated.text = " "
dcCreated.tail = "\n\t"
dublinCore.append(dcCreated)

dcValid = etree.Element(dcterms + "valid", nsmap=NSMAP) 
dcValid.text = " "
dcValid.tail = "\n\t"
dublinCore.append(dcValid)

dcAvailable = etree.Element(dcterms + "available", nsmap=NSMAP) 
dcAvailable.text = " "
dcAvailable.tail = "\n\t"
dublinCore.append(dcAvailable)

dcIssued = etree.Element(dcterms + "issued", nsmap=NSMAP) 
dcIssued.text = " "
dcIssued.tail = "\n\t"
dublinCore.append(dcIssued)

dcModified = etree.Element(dcterms + "modified", nsmap=NSMAP) 
dcModified.text = " "
dcModified.tail = "\n\t"
dublinCore.append(dcModified)

dcDateAccepted = etree.Element(dcterms + "dateAccepted", nsmap=NSMAP) 
dcDateAccepted.text = " "
dcDateAccepted.tail = "\n\t"
dublinCore.append(dcDateAccepted)

dcDateCopyrighted = etree.Element(dcterms + "dateCopyrighted", nsmap=NSMAP) 
dcDateCopyrighted.text = " "
dcDateCopyrighted.tail = "\n\t"
dublinCore.append(dcDateCopyrighted)

dcDateSubmitted = etree.Element(dcterms + "dateSubmitted", nsmap=NSMAP) 
dcDateSubmitted.text = " "
dcDateSubmitted.tail = "\n\t"
dublinCore.append(dcDateSubmitted)

dcExtent = etree.Element(dcterms + "extent", nsmap=NSMAP) 
dcExtent.text = " "
dcExtent.tail = "\n\t"
dublinCore.append(dcExtent)

dcMedium = etree.Element(dcterms + "medium", nsmap=NSMAP) 
dcMedium.text = " "
dcMedium.tail = "\n\t"
dublinCore.append(dcMedium)

dcIsVersionOf = etree.Element(dcterms + "isVersionOf", nsmap=NSMAP) 
dcIsVersionOf.text = " "
dcIsVersionOf.tail = "\n\t"
dublinCore.append(dcIsVersionOf)

dcHasVersion = etree.Element(dcterms + "hasVersion", nsmap=NSMAP) 
dcHasVersion.text = " "
dcHasVersion.tail = "\n\t"
dublinCore.append(dcHasVersion)

dcIsReplacedBy = etree.Element(dcterms + "isReplacedBy", nsmap=NSMAP) 
dcIsReplacedBy.text = " "
dcIsReplacedBy.tail = "\n\t"
dublinCore.append(dcIsReplacedBy)

dcReplaces = etree.Element(dcterms + "replaces", nsmap=NSMAP) 
dcReplaces.text = " "
dcReplaces.tail = "\n\t"
dublinCore.append(dcReplaces)

dcIsRequiredBy = etree.Element(dcterms + "isRequiredBy", nsmap=NSMAP) 
dcIsRequiredBy.text = " "
dcIsRequiredBy.tail = "\n\t"
dublinCore.append(dcIsRequiredBy)

dcRequires = etree.Element(dcterms + "requires", nsmap=NSMAP) 
dcRequires.text = " "
dcRequires.tail = "\n\t"
dublinCore.append(dcRequires)

dcIsPartOf = etree.Element(dcterms + "isPartOf", nsmap=NSMAP) 
dcIsPartOf.text = " "
dcIsPartOf.tail = "\n\t"
dublinCore.append(dcIsPartOf)

dcHasPart = etree.Element(dcterms + "hasPart", nsmap=NSMAP) 
dcHasPart.text = " "
dcHasPart.tail = "\n\t"
dublinCore.append(dcHasPart)

dcIsReferencedBy = etree.Element(dcterms + "isReferencedBy", nsmap=NSMAP) 
dcIsReferencedBy.text = " "
dcIsReferencedBy.tail = "\n\t"
dublinCore.append(dcIsReferencedBy)

dcReferences = etree.Element(dcterms + "references", nsmap=NSMAP) 
dcReferences.text = " "
dcReferences.tail = "\n\t"
dublinCore.append(dcReferences)

dcIsFormatOf = etree.Element(dcterms + "isFormatOf", nsmap=NSMAP) 
dcIsFormatOf.text = " "
dcIsFormatOf.tail = "\n\t"
dublinCore.append(dcIsFormatOf)

dcConformsTo = etree.Element(dcterms + "conformsTo", nsmap=NSMAP) 
dcConformsTo.text = " "
dcConformsTo.tail = "\n\t"
dublinCore.append(dcConformsTo)

dcSpatial = etree.Element(dcterms + "spatial", nsmap=NSMAP) 
dcSpatial.text = " "
dcSpatial.tail = "\n\t"
dublinCore.append(dcSpatial)

dcTemporal = etree.Element(dcterms + "temporal", nsmap=NSMAP) 
dcTemporal.text = " "
dcTemporal.tail = "\n\t"
dublinCore.append(dcTemporal)

dcAudience = etree.Element(dcterms + "audience", nsmap=NSMAP) 
dcAudience.text = " "
dcAudience.tail = "\n\t"
dublinCore.append(dcAudience)

dcAccrualMethod = etree.Element(dcterms + "accrualMethod", nsmap=NSMAP) 
dcAccrualMethod.text = " "
dcAccrualMethod.tail = "\n\t"
dublinCore.append(dcAccrualMethod)

dcAccrualPeriodicity = etree.Element(dcterms + "accrualPeriodicity", nsmap=NSMAP) 
dcAccrualPeriodicity.text = " "
dcAccrualPeriodicity.tail = "\n\t"
dublinCore.append(dcAccrualPeriodicity)

dcAccrualPolicy = etree.Element(dcterms + "accrualPolicy", nsmap=NSMAP) 
dcAccrualPolicy.text = " "
dcAccrualPolicy.tail = "\n\t"
dublinCore.append(dcAccrualPolicy)

dcInstructionalMethod = etree.Element(dcterms + "instructionalMethod", nsmap=NSMAP) 
dcInstructionalMethod.text = " "
dcInstructionalMethod.tail = "\n\t"
dublinCore.append(dcInstructionalMethod)

dcProvenance = etree.Element(dcterms + "Provenance", nsmap=NSMAP) 
dcProvenance.text = " "
dcProvenance.tail = "\n\t"
dublinCore.append(dcProvenance)

dcRightsHolder = etree.Element(dcterms + "rightsHolder", nsmap=NSMAP) 
dcRightsHolder.text = " "
dcRightsHolder.tail = "\n\t"
dublinCore.append(dcRightsHolder)

dcMediator = etree.Element(dcterms + "mediator", nsmap=NSMAP) 
dcMediator.text = " "
dcMediator.tail = "\n\t"
dublinCore.append(dcMediator)

dcEducationLevel = etree.Element(dcterms + "educationLevel", nsmap=NSMAP) 
dcEducationLevel.text = " "
dcEducationLevel.tail = "\n\t"
dublinCore.append(dcEducationLevel)

dcAccessRights = etree.Element(dcterms + "accessRights", nsmap=NSMAP) 
dcAccessRights.text = " "
dcAccessRights.tail = "\n\t"
dublinCore.append(dcAccessRights)

dcLicense = etree.Element(dcterms + "license", nsmap=NSMAP) 
dcLicense.text = " "
dcLicense.tail = "\n\t"
dublinCore.append(dcLicense)

dcBibliographicCitation = etree.Element(dcterms + "bibliographicCitation", nsmap=NSMAP) 
dcBibliographicCitation.text = " "
dcBibliographicCitation.tail = "\n"
dublinCore.append(dcBibliographicCitation)

tree = etree.ElementTree(dublinCore)
tree.write("dublincore.xml") 
print(etree.tostring(dublinCore, pretty_print=True))
