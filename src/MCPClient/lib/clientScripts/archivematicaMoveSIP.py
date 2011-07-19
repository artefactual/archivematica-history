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
import os
import subprocess
import shlex
import sys
sys.path.append("/usr/lib/archivematica/archivematicaCommon")
import databaseInterface
from executeOrRunSubProcess import executeOrRun

def renameAsSudo(source, destination):
    """Used to move/rename Directories that the archivematica user may or may not have writes to move"""
    command = "sudo mv \"" + source + "\"   \"" + destination + "\""
    exitCode, stdOut, stdError = executeOrRun("command", command, "", printing=False)
    if exitCode:
        print stdOut
        print >>sys.stderr, stdError
        exit(exitCode)
    


def updateDB(dst, sipUUID):
    sql =  """UPDATE SIP SET currentPath='""" + dst + """' WHERE sipUUID='""" + sipUUID + """';"""
    databaseInterface.runSQL(sql)
    
def moveSIP(src, dst, sipUUID, sharedDirectoryPath):
    # os.rename(src, dst)
    renameAsSudo(src, dst)
    
    dest = dst.replace(sharedDirectoryPath, "%sharedPath%", 1)
    if dest.endswith("/"):
        dest = os.path.join(dest, os.path.basename(src))
    if dest.endswith("/."):
        dest = os.path.join(dest[:-1], os.path.basename(src))
    updateDB(dest, sipUUID)

if __name__ == '__main__':
    src = sys.argv[1]
    dst = sys.argv[2]
    sipUUID = sys.argv[3]
    sharedDirectoryPath = sys.argv[4]
    moveSIP(src, dst, sipUUID, sharedDirectoryPath)

