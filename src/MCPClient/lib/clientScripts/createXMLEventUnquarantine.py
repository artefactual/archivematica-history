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
from archivematicaFunctions import appendEventToFile2

#etree.Element("root", interesting="totally")
#SubElement(root, "child").text = "Child 1"



if __name__ == '__main__':
    """This prints the contents for an Archivematica Unquarantine Event xml file"""
    eIDValue = sys.argv[1]
    date = sys.argv[2]
    xmlFile = sys.argv[3]
    
    event = createEvent( eIDValue, "unquarantine", eventDateTime=date)
    appendEventToFile2(xmlFile, event)
    #print etree.tostring(event, pretty_print=True)
