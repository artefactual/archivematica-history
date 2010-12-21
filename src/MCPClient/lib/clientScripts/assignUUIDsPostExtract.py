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

from fileAddedToSIP import addFileToSIP
import sys

if __name__ == '__main__':
    """This creates an Archivematica Quarantine Event xml file"""
    objectsDirectory = sys.argv[1]
    logsDirectory = sys.argv[2]
    filePath = sys.argv[3]
    fileUUID = sys.argv[4]
    eIDValue = sys.argv[5]
    date = sys.argv[6]
    taskUUID = sys.argv[7]
    
    fileUUIDNotFound = "No UUID for file:"
    
    if fileUUIDNotFound in fileUUID:
        objects = "objects/"
        relativeFilePath = filePath.replace(objectsDirectory, objects, 1)
        addFileToSIP( objectsDirectory, logsDirectory, filePath, taskUUID, eIDValue, date, date, eventOutcomeDetailNote="extracted " + relativeFilePath)
