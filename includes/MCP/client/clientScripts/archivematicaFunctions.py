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


def getTagged(root, tag):
    ret = []
    for element in root:
        if element.tag == tag:
            ret.append(element)
            return ret #only return the first encounter
    return ret  
    
def appendEventToFile(SIPLogsDirectory, fileUUID, eventXML):
    xmlFile = SIPLogsDirectory + "fileMeta/" + fileUUID + ".xml"
    tree = etree.parse( xmlFile )
    root = tree.getroot()

    events = getTagged(root, "events")
    events.append(eventXML)
    
    tree = etree.ElementTree(root)
    tree.write(xmlFile)
    
def archivematicaRenameFile(SIPLogsDirectory, fileUUID, newName, eventXML):
    xmlFile = SIPLogsDirectory + "fileMeta/" + fileUUID + ".xml"
    tree = etree.parse( xmlFile )
    root = tree.getroot()
    xmlFileName = getTagged(root, "currentFileName")
    xmlFileName.text = newName

    events = getTagged(root, "events")
    events.append(eventXML)
    
    tree = etree.ElementTree(root)
    tree.write(xmlFile)
    
    

