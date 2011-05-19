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
from archivematicaFunctions import getTagged
from archivematicaFunctions import fileNoLongerExists
from createXmlEventsAssist import createEvent
from fileAddedToSIP import sha_for_file


if __name__ == '__main__':
    
    objectsDir = sys.argv[1]
    xmlFile = sys.argv[2]
    date = sys.argv[3]
    eIDValue = sys.argv[4]
    
    eventDetailText = ""
    
    if not xmlFile.endswith(".xml"):
        print >>sys.stderr, "Warning: Non xml file in /logs/fileMeta/ {" + xmlFile + "}"
        quit(0)
    
    tree = etree.parse( xmlFile )
    root = tree.getroot()
    currentLogName = getTagged(root, "currentFileName")[0].text
    currentName = currentLogName.replace("objects/", objectsDir, 1)
    
    fileNoLongerExistsCode = fileNoLongerExists(root, objectsDir)
    if  fileNoLongerExistsCode != 0:
        if fileNoLongerExistsCode == -1:
            print >>sys.stderr, '{', currentLogName, '}', " was removed."
            quit(0)
        elif fileNoLongerExistsCode == 1:
            print >>sys.stderr, '{', currentLogName, '}', " was removed."
            quit(1)
        print >>sys.stderr, "Unhandled fileNolongerExists Exception"
        quit(3)
    
    objectCharacteristics = getTagged( getTagged(root,"object")[0], "objectCharacteristics")[0]
    fixity = getTagged( objectCharacteristics, "fixity")[0] 
    premisChecksum = getTagged(fixity, "messageDigest")[0].text
    
    fileChecsum = sha_for_file(currentName).__str__()
    if premisChecksum != fileChecsum:
        print >>sys.stderr, '{', currentLogName, '}',  " did not pass integrity check!"     
        quit(2)