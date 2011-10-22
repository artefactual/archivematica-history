#!/usr/bin/python -OO

# This file is part of Archivematica.
#
# Copyright 2010-2011 Artefactual Systems Inc. <http://artefactual.com>
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
import sys
from archivematicaFunctions import fileNoLongerExists
from archivematicaFunctions import getTagged
from createXmlEventsAssist import createEvent

def addRemovedEvent(root, eventDetailText, date, eIDValue):    
    eventXML = createEvent( eIDValue, "fileRemoved", \
    eventDateTime=date,  eventDetailText=eventDetailText)
    
    events = getTagged(root, "events")[0]
    events.append(eventXML)
   


if __name__ == '__main__':
    
    objectsDir = sys.argv[1]
    xmlFile = sys.argv[2]
    eventDetailText = sys.argv[3] 
    date = sys.argv[4]
    eIDValue = sys.argv[5]
    
    if not xmlFile.endswith(".xml"):
        print "Warning: Non xml file in /logs/fileMeta/ {" + xmlFile + "}"
        quit(0)
    
    tree = etree.parse( xmlFile )
    root = tree.getroot()
    
    if fileNoLongerExists(root, objectsDir) == 1:
        addRemovedEvent(root, eventDetailText, date, eIDValue)
        tree = etree.ElementTree(root)
        tree.write(xmlFile)