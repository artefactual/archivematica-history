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

import lxml.etree as etree
from datetime import datetime
from archivematicaXMLNamesSpace import *

dublinCore = etree.Element( "dublincore", \
    nsmap = NSMAP, \
    attrib = { "{" + xsiNS + "}schemaLocation" : "http://purl.org/dc/terms/ http://dublincore.org/schemas/xmls/qdc/2008/02/11/dcterms.xsd" }) 
dublinCore.text = "\n\t"
dublinCore.tail = "\n"

dcTitle = etree.Element(dctermsBNS + "title", nsmap=NSMAP) 
dcTitle.text = " "
dcTitle.tail = "\n\t"
dublinCore.append(dcTitle)

dcCreator = etree.Element(dctermsBNS + "creator", nsmap=NSMAP) 
dcCreator.text = " "
dcCreator.tail = "\n\t"
dublinCore.append(dcCreator)

dcSubject = etree.Element(dctermsBNS + "subject", nsmap=NSMAP) 
dcSubject.text = " "
dcSubject.tail = "\n\t"
dublinCore.append(dcSubject)

dcDescription = etree.Element(dctermsBNS + "description", nsmap=NSMAP) 
dcDescription.text = " "
dcDescription.tail = "\n\t"
dublinCore.append(dcDescription)

dcPublisher = etree.Element(dctermsBNS + "publisher", nsmap=NSMAP) 
dcPublisher.text = " "
dcPublisher.tail = "\n\t"
dublinCore.append(dcPublisher)

dcContributor = etree.Element(dctermsBNS + "contributor", nsmap=NSMAP) 
dcContributor.text = " "
dcContributor.tail = "\n\t"
dublinCore.append(dcContributor)

dcDate = etree.Element(dctermsBNS + "date", nsmap=NSMAP) 
dcDate.text = " "
dcDate.tail = "\n\t"
dublinCore.append(dcDate)

dcType = etree.Element(dctermsBNS + "type", nsmap=NSMAP) 
dcType.text = " "
dcType.tail = "\n\t"
dublinCore.append(dcType)

dcFormat = etree.Element(dctermsBNS + "format", nsmap=NSMAP) 
dcFormat.text = " "
dcFormat.tail = "\n\t"
dublinCore.append(dcFormat)

dcIdentifier = etree.Element(dctermsBNS + "identifier", nsmap=NSMAP) 
dcIdentifier.text = " "
dcIdentifier.tail = "\n\t"
dublinCore.append(dcIdentifier)

dcSource = etree.Element(dctermsBNS + "source", nsmap=NSMAP) 
dcSource.text = " "
dcSource.tail = "\n\t"
dublinCore.append(dcSource)

dcLanguage = etree.Element(dctermsBNS + "language", nsmap=NSMAP) 
dcLanguage.text = " "
dcLanguage.tail = "\n\t"
dublinCore.append(dcLanguage)

dcRelation = etree.Element(dctermsBNS + "relation", nsmap=NSMAP) 
dcRelation.text = " "
dcRelation.tail = "\n\t"
dublinCore.append(dcRelation)

dcCoverage = etree.Element(dctermsBNS + "coverage", nsmap=NSMAP) 
dcCoverage.text = " "
dcCoverage.tail = "\n\t"
dublinCore.append(dcCoverage)

dcRights = etree.Element(dctermsBNS + "rights", nsmap=NSMAP) 
dcRights.text = " "
dcRights.tail = "\n\t"
dublinCore.append(dcRights)

dcAlternative = etree.Element(dctermsBNS + "alternative", nsmap=NSMAP) 
dcAlternative.text = " "
dcAlternative.tail = "\n\t"
dublinCore.append(dcAlternative)

dcTOC = etree.Element(dctermsBNS + "tableOfContents", nsmap=NSMAP) 
dcTOC.text = " "
dcTOC.tail = "\n\t"
dublinCore.append(dcTOC)

dcAbstract = etree.Element(dctermsBNS + "abstract", nsmap=NSMAP) 
dcAbstract.text = " "
dcAbstract.tail = "\n\t"
dublinCore.append(dcAbstract)

dcCreated = etree.Element(dctermsBNS + "created", nsmap=NSMAP) 
dcCreated.text = " "
dcCreated.tail = "\n\t"
dublinCore.append(dcCreated)

dcValid = etree.Element(dctermsBNS + "valid", nsmap=NSMAP) 
dcValid.text = " "
dcValid.tail = "\n\t"
dublinCore.append(dcValid)

dcAvailable = etree.Element(dctermsBNS + "available", nsmap=NSMAP) 
dcAvailable.text = " "
dcAvailable.tail = "\n\t"
dublinCore.append(dcAvailable)

dcIssued = etree.Element(dctermsBNS + "issued", nsmap=NSMAP) 
dcIssued.text = " "
dcIssued.tail = "\n\t"
dublinCore.append(dcIssued)

dcModified = etree.Element(dctermsBNS + "modified", nsmap=NSMAP) 
dcModified.text = " "
dcModified.tail = "\n\t"
dublinCore.append(dcModified)

dcDateAccepted = etree.Element(dctermsBNS + "dateAccepted", nsmap=NSMAP) 
dcDateAccepted.text = " "
dcDateAccepted.tail = "\n\t"
dublinCore.append(dcDateAccepted)

dcDateCopyrighted = etree.Element(dctermsBNS + "dateCopyrighted", nsmap=NSMAP) 
dcDateCopyrighted.text = " "
dcDateCopyrighted.tail = "\n\t"
dublinCore.append(dcDateCopyrighted)

dcDateSubmitted = etree.Element(dctermsBNS + "dateSubmitted", nsmap=NSMAP) 
dcDateSubmitted.text = " "
dcDateSubmitted.tail = "\n\t"
dublinCore.append(dcDateSubmitted)

dcExtent = etree.Element(dctermsBNS + "extent", nsmap=NSMAP) 
dcExtent.text = " "
dcExtent.tail = "\n\t"
dublinCore.append(dcExtent)

dcMedium = etree.Element(dctermsBNS + "medium", nsmap=NSMAP) 
dcMedium.text = " "
dcMedium.tail = "\n\t"
dublinCore.append(dcMedium)

dcIsVersionOf = etree.Element(dctermsBNS + "isVersionOf", nsmap=NSMAP) 
dcIsVersionOf.text = " "
dcIsVersionOf.tail = "\n\t"
dublinCore.append(dcIsVersionOf)

dcHasVersion = etree.Element(dctermsBNS + "hasVersion", nsmap=NSMAP) 
dcHasVersion.text = " "
dcHasVersion.tail = "\n\t"
dublinCore.append(dcHasVersion)

dcIsReplacedBy = etree.Element(dctermsBNS + "isReplacedBy", nsmap=NSMAP) 
dcIsReplacedBy.text = " "
dcIsReplacedBy.tail = "\n\t"
dublinCore.append(dcIsReplacedBy)

dcReplaces = etree.Element(dctermsBNS + "replaces", nsmap=NSMAP) 
dcReplaces.text = " "
dcReplaces.tail = "\n\t"
dublinCore.append(dcReplaces)

dcIsRequiredBy = etree.Element(dctermsBNS + "isRequiredBy", nsmap=NSMAP) 
dcIsRequiredBy.text = " "
dcIsRequiredBy.tail = "\n\t"
dublinCore.append(dcIsRequiredBy)

dcRequires = etree.Element(dctermsBNS + "requires", nsmap=NSMAP) 
dcRequires.text = " "
dcRequires.tail = "\n\t"
dublinCore.append(dcRequires)

dcIsPartOf = etree.Element(dctermsBNS + "isPartOf", nsmap=NSMAP) 
dcIsPartOf.text = " "
dcIsPartOf.tail = "\n\t"
dublinCore.append(dcIsPartOf)

dcHasPart = etree.Element(dctermsBNS + "hasPart", nsmap=NSMAP) 
dcHasPart.text = " "
dcHasPart.tail = "\n\t"
dublinCore.append(dcHasPart)

dcIsReferencedBy = etree.Element(dctermsBNS + "isReferencedBy", nsmap=NSMAP) 
dcIsReferencedBy.text = " "
dcIsReferencedBy.tail = "\n\t"
dublinCore.append(dcIsReferencedBy)

dcReferences = etree.Element(dctermsBNS + "references", nsmap=NSMAP) 
dcReferences.text = " "
dcReferences.tail = "\n\t"
dublinCore.append(dcReferences)

dcIsFormatOf = etree.Element(dctermsBNS + "isFormatOf", nsmap=NSMAP) 
dcIsFormatOf.text = " "
dcIsFormatOf.tail = "\n\t"
dublinCore.append(dcIsFormatOf)

dcConformsTo = etree.Element(dctermsBNS + "conformsTo", nsmap=NSMAP) 
dcConformsTo.text = " "
dcConformsTo.tail = "\n\t"
dublinCore.append(dcConformsTo)

dcSpatial = etree.Element(dctermsBNS + "spatial", nsmap=NSMAP) 
dcSpatial.text = " "
dcSpatial.tail = "\n\t"
dublinCore.append(dcSpatial)

dcTemporal = etree.Element(dctermsBNS + "temporal", nsmap=NSMAP) 
dcTemporal.text = " "
dcTemporal.tail = "\n\t"
dublinCore.append(dcTemporal)

dcAudience = etree.Element(dctermsBNS + "audience", nsmap=NSMAP) 
dcAudience.text = " "
dcAudience.tail = "\n\t"
dublinCore.append(dcAudience)

dcAccrualMethod = etree.Element(dctermsBNS + "accrualMethod", nsmap=NSMAP) 
dcAccrualMethod.text = " "
dcAccrualMethod.tail = "\n\t"
dublinCore.append(dcAccrualMethod)

dcAccrualPeriodicity = etree.Element(dctermsBNS + "accrualPeriodicity", nsmap=NSMAP) 
dcAccrualPeriodicity.text = " "
dcAccrualPeriodicity.tail = "\n\t"
dublinCore.append(dcAccrualPeriodicity)

dcAccrualPolicy = etree.Element(dctermsBNS + "accrualPolicy", nsmap=NSMAP) 
dcAccrualPolicy.text = " "
dcAccrualPolicy.tail = "\n\t"
dublinCore.append(dcAccrualPolicy)

dcInstructionalMethod = etree.Element(dctermsBNS + "instructionalMethod", nsmap=NSMAP) 
dcInstructionalMethod.text = " "
dcInstructionalMethod.tail = "\n\t"
dublinCore.append(dcInstructionalMethod)

dcProvenance = etree.Element(dctermsBNS + "Provenance", nsmap=NSMAP) 
dcProvenance.text = " "
dcProvenance.tail = "\n\t"
dublinCore.append(dcProvenance)

dcRightsHolder = etree.Element(dctermsBNS + "rightsHolder", nsmap=NSMAP) 
dcRightsHolder.text = " "
dcRightsHolder.tail = "\n\t"
dublinCore.append(dcRightsHolder)

dcMediator = etree.Element(dctermsBNS + "mediator", nsmap=NSMAP) 
dcMediator.text = " "
dcMediator.tail = "\n\t"
dublinCore.append(dcMediator)

dcEducationLevel = etree.Element(dctermsBNS + "educationLevel", nsmap=NSMAP) 
dcEducationLevel.text = " "
dcEducationLevel.tail = "\n\t"
dublinCore.append(dcEducationLevel)

dcAccessRights = etree.Element(dctermsBNS + "accessRights", nsmap=NSMAP) 
dcAccessRights.text = " "
dcAccessRights.tail = "\n\t"
dublinCore.append(dcAccessRights)

dcLicense = etree.Element(dctermsBNS + "license", nsmap=NSMAP) 
dcLicense.text = " "
dcLicense.tail = "\n\t"
dublinCore.append(dcLicense)

dcBibliographicCitation = etree.Element(dctermsBNS + "bibliographicCitation", nsmap=NSMAP) 
dcBibliographicCitation.text = " "
dcBibliographicCitation.tail = "\n"
dublinCore.append(dcBibliographicCitation)

tree = etree.ElementTree(dublinCore)
tree.write("dublincore.xml") 
print(etree.tostring(dublinCore, pretty_print=True))
