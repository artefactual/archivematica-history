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

dmdSec = etree.Element("dmdSec")
dmdSec.text = "\n\t\t"
dmdSec.tail = "\n"
root.append(dmdSec)

dmdSecMdWrap = etree.Element("mdWrap")
dmdSec.text = "\n\t\t"
dmdSec.tail = "\n"
dmdSec.append(dmdSecMdWrap)

dmdSecXmlData = etree.Element("xmlData")
dmdSec.text = "\n\t\t"
dmdSec.tail = "\n"
dmdSecMdWrap.append(dmdSecXmlData)

dcTitle = etree.Element("dcterms:title")
dcTitle.text = " "
dcTitle.tail = "\n\t\t"
dmdSecXmlData.append(dcTitle)

dcProvenance = etree.Element("dcterms:provenance")
dcProvenance.text = " "
dcProvenance.tail = "\n\t\t"
dmdSecXmlData.append(dcProvenance)

dcPartOf = etree.Element("dcterms:partOf")
dcPartOf.text = " "
dcPartOf.tail = "\n\t\t"
dmdSecXmlData.append(dcPartOf)

dcDescription = etree.Element("dcterms:description")
dcDescription.text = " "
dcDescription.tail = "\n\t\t"
dmdSecXmlData.append(dcDescription)

dcDateReceived = etree.Element("dcterms:dateReceived")
dcDateReceived.text = (datetime.utcnow()).__str__()
dcDateReceived.tail = "\n\t"
dmdSecXmlData.append(dcDateReceived)

amdSec = etree.Element("amdSec")
amdSec.text = "\n\t\t"
amdSec.tail = "\n"
root.append(amdSec)

techMD = etree.Element("techMD")
techMD.text = "\n\t\t"
techMD.tail = "\n"
amdSec.append(techMD)

digiprovMD = etree.Element("digiprovMD")
digiprovMD.text = "\n\t\t"
digiprovMD.tail = "\n"
amdSec.append(digiprovMD)

fileSec = etree.Element("fileSec")
amdSec.text = "\n\t\t"
amdSec.tail = "\n"
root.append(fileSec)

structMap = etree.Element("structMap")
amdSec.text = "\n\t\t"
amdSec.tail = "\n"
root.append(structMap)

tree = etree.ElementTree(root)
tree.write("METS.xml")