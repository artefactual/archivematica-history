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


def createLinkingAgentIdentifier(IDType="preservation system", IDValue="Archivematica-0.7"):
    ret = etree.Element("linkingAgentIdentifier")
    etree.SubElement(ret, "linkingAgentIdentifierType").text = IDType
    etree.SubElement(ret, "linkingAgentIdentifierValue").text = IDValue
    return ret

def createOutcomeInformation( eventOutcomeDetailNote = None):
    ret = etree.Element("eventOutcomeInformation")
    etree.SubElement(ret, "eventOutcome")
    eventOutcomeDetail = etree.SubElement(ret, "eventOutcomeDetail")
    etree.SubElement(eventOutcomeDetail, "eventOutcomeDetailNote").text = eventOutcomeDetailNote
    return ret

def createEvent( eIDValue, eType, eIDType="Archivematica ID", \
eventDateTime = "now", \
eventDetailText = "", \
eOutcomeInformation = createOutcomeInformation(), \
linkingAgentIdentifier = None):
    ret = etree.Element("event")
    eventIdentifier = etree.SubElement(ret, "eventIdentifier")
    etree.SubElement(eventIdentifier, "eventIdentifierType").text = eIDType
    etree.SubElement(eventIdentifier, "eventIdentifierValue").text = eIDValue
    etree.SubElement(ret, "eventType").text = eType
    etree.SubElement(ret, "eventDateTime").text = eventDateTime
    eDetail = etree.SubElement(ret, "eventDetail")
    eDetail.text = eventDetailText
    if eOutcomeInformation != None:
        ret.append(eOutcomeInformation)
    if not linkingAgentIdentifier:
        linkingAgentIdentifier = createLinkingAgentIdentifier()
    ret.append(linkingAgentIdentifier)
    return ret

if __name__ == '__main__':
    print "This is a support file."
    print "testing..."
    event = createEvent("test", "test")
    print etree.tostring(event, pretty_print=True)

