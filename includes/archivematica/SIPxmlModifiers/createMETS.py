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

dcProvenance = etree.Element("dcterms:provenance")
dcProvenance.text = " "
dcProvenance.tail = "\n\t\t"
dublinCore.append(dcProvenance)

dcPartOf = etree.Element("dcterms:partOf")
dcPartOf.text = " "
dcPartOf.tail = "\n\t\t"
dublinCore.append(dcPartOf)

dcDescription = etree.Element("dcterms:description")
dcDescription.text = " "
dcDescription.tail = "\n\t\t"
dublinCore.append(dcDescription)

dcDateReceived = etree.Element("dcterms:dateReceived")
dcDateReceived.text = (datetime.utcnow()).__str__()
dcDateReceived.tail = "\n\t"
dublinCore.append(dcDateReceived)

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
