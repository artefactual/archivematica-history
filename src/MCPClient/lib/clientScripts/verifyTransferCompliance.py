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
import os
import sys
from verifySIPCompliance import checkDirectory

requiredDirectories = ["objects", \
                       "logs", \
                       "metadata",\
                       "metadata/submissionDocumentation"]
allowableFiles = ["processingMCP.xml"]

def verifyDirectoriesExist(SIPDir, ret=0):
    for directory in requiredDirectories:
        if not os.path.isdir(os.path.join(SIPDir, directory)):
            print >>sys.stderr, "Required Directory Does Not Exist: " + directory
            ret += 1
    return ret

def verifyNothingElseAtTopLevel(SIPDir, ret=0):
    for entry in os.listdir(SIPDir):
        if os.path.isdir(os.path.join(SIPDir, entry)):
            if entry not in requiredDirectories:
                print >>sys.stderr, "Error, directory exists: " + entry
                ret += 1
        else:
            if entry not in allowableFiles:
                print >>sys.stderr, "Error, file exists: " + entry
                ret += 1
    return ret

if __name__ == '__main__':
    SIPDir = sys.argv[1] 
    ret = verifyDirectoriesExist(SIPDir)
    ret = verifyNothingElseAtTopLevel(SIPDir, ret)
    ret = checkDirectory(SIPDir, ret)
    if ret != 0:
        import time
        time.sleep(10)
    quit(ret)
