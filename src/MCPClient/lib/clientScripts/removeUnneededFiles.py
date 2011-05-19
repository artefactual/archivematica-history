#!/usr/bin/python

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
import os
from scanForRemovedFiles import addRemovedEvent

removeIfFileNameIs = ["Thumbs.db"]
   
def removableFile(target):
    global eventDetailText
    basename = os.path.basename(target)
    if basename in removeIfFileNameIs:     
        eventDetailText = basename + " is noted as a removable file."
        return True
    return False

if __name__ == '__main__':
    target = sys.argv[1] 
    fileUUID = sys.argv[2]
    logsDirectory = sys.argv[3]
    date = sys.argv[4]
    eIDValue = sys.argv[5]
    
    xmlFile = logsDirectory + "fileMeta/" + fileUUID + ".xml" 
    global eventDetailText  
    eventDetailText = "fileRemoved"   
    if removableFile(target):
        print fileUUID + " -> " + os.path.basename(target)
        os.remove(target)
        tree = etree.parse( xmlFile )
        root = tree.getroot()
        addRemovedEvent(root, eventDetailText, date, eIDValue)
        tree = etree.ElementTree(root)
        tree.write(xmlFile)