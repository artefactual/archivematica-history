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
import sys
import lxml.etree as etree
from createXmlEventsAssist import createEvent 
from createXmlEventsAssist import createOutcomeInformation
from createXmlEventsAssist import createLinkingAgentIdentifier


if __name__ == '__main__':
    """This prints the contents for an Archivematica Clamscan Event xml file"""
    eIDValue = sys.argv[1]
    date = sys.argv[2]
    vers = sys.argv[3]
    uuid = sys.argv[4] #UUID
    eventDetailText = "program=\"UUID\"; version=\"" + vers + "\""
    eventDetail = etree.Element("eventDetail")
    eventDetail.text = eventDetailText
    eventOutcome = createOutcomeInformation( eventOutcomeDetailNote = uuid)
    event = createEvent( eIDValue, "unique identifier assignments", eventDateTime=date, eventDetail=eventDetail, eOutcomeInformation=eventOutcome)
    print etree.tostring(event, pretty_print=True)
