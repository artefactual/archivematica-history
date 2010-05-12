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

#import xml.etree.cElementTree as etree
import xml.etree.ElementTree as etree



from datetime import datetime


root = etree.Element("SIP")
root.text = "\n\t"
dc = etree.Element("dublincore")
dc.text = "\n\t\t"
dc.tail = "\n"
root.append(dc)

dc.set("xmlns", "http://archivematica.org/")
dc.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
dc.set("xsi:schemaLocation", "http://dublincore.org")
#dc.set("xmlns:dc", "http://purl.org/dc/elements/1.1/")
dc.set("xmlns:dcterms", "http://purl.org/dc/elements/1.1/")

title = etree.Element("dcterms:title")
dc.append(title)
title.text = " "
title.tail = "\n\t\t"

provenance = etree.Element("dcterms:provenance")
dc.append(provenance)
provenance.text = " "
provenance.tail = "\n\t\t"

partOf = etree.Element("dcterms:partOf")
dc.append(partOf)
partOf.text = " "
partOf.tail = "\n\t\t"

description = etree.Element("dcterms:description")
dc.append(description)
description.text = " "
description.tail = "\n\t\t"

dateReceived = etree.Element("dcterms:dateReceived")
dc.append(dateReceived)
dateReceived.text = (datetime.utcnow()).__str__()
dateReceived.tail = "\n\t"

# identifier added by addUUIDasDCidentifier.py

#print(etree.tostring(root, None, "xml", None, True, True, None))
#print(etree.tostring(root))
tree = etree.ElementTree(root)
#tree.write(sys.argv[1]+"/SIP.xml")
tree.write("SIP.xml")

