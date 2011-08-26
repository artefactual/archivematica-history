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
import sys
import uuid
sys.path.append("/usr/lib/archivematica/archivematicaCommon")
from fileOperations import addFileToTransfer


if __name__ == '__main__':
    sipDirectory = sys.argv[1]
    filePath = sys.argv[2]
    fileUUID = sys.argv[3]
    sipUUID = sys.argv[4]
    taskUUID = sys.argv[5]
    date = sys.argv[6]
    
    if not fileUUID or fileUUID == "None":
        fileUUID = uuid.uuid4().__str__()     
    
    filePathRelativeToSIP = filePath.replace(sipDirectory,"%transferDirectory%", 1)
    addFileToTransfer(filePathRelativeToSIP, fileUUID, sipUUID, taskUUID, date)

    

    
    
