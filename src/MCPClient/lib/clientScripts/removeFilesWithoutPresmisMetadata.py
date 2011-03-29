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
import os
from optparse import OptionParser

# DUPLICATE CODE IN MCP Server - archivematica Replacement Dics 
def isUUID(uuid):
    split = uuid.split("-")
    if len(split) != 5 \
    or len(split[0]) != 8 \
    or len(split[1]) != 4 \
    or len(split[2]) != 4 \
    or len(split[3]) != 4 \
    or len(split[4]) != 12 :
        return False
    return True


def verifyFileHasUUID(uuid, filePath, objectsDirectory):
    uuid = uuid.__str__()
    if isUUID(uuid):
        #print uuid + " -> " + filePath
        uuid = uuid #no-op
    else:
        if objectsDirectory:
            print >>sys.stderr, filePath.replace(objectsDirectory, "objects/")
        if os.path.isfile(filePath):
            os.remove(filePath)
        quit(0)


if __name__ == '__main__':
    
    parser = OptionParser()
    #--inputFile "%relativeLocation%" --commandClassifications "normalize" --fileUUID "%fileUUID%" --taskUUID "%taskUUID%" --objectsDirectory "%SIPObjectsDirectory%" --logsDirectory "%SIPLogsDirectory%" --date "%date%"
    parser.add_option("-f",  "--inputFile",          action="store", dest="inputFile", default="")
    parser.add_option("-o",  "--objectsDirectory",  action="store", dest="objectsDirectory", default="")
    parser.add_option("-i",  "--fileUUID",           action="store", dest="fileUUID", default="")
    
    (opts, args) = parser.parse_args()
     
    verifyFileHasUUID(opts.fileUUID, opts.inputFile, opts.objectsDirectory)
    
    
