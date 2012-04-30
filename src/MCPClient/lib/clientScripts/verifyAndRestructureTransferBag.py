#!/usr/bin/python -OO

# This file is part of Archivematica.
#
# Copyright 2010-2012 Artefactual Systems Inc. <http://artefactual.com>
#
# Archivematica is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
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
sys.path.append("/usr/lib/archivematica/archivematicaCommon")
from executeOrRunSubProcess import executeOrRun
from restructureForCompliance import restructureBagForComplianceFileUUIDsAssigned

printSubProcessOutput=False
exitCode = 0
verificationCommands = []
verificationCommandsOutputs = []

def verifyBag(bag):
    verificationCommands = [
        "/usr/share/bagit/bin/bag verifyvalid " + bag, 
        "/usr/share/bagit/bin/bag checkpayloadoxum " + bag, 
        "/usr/share/bagit/bin/bag verifycomplete " + bag, 
        "/usr/share/bagit/bin/bag verifypayloadmanifests " + bag, 
        "/usr/share/bagit/bin/bag verifytagmanifests " + bag ]
    for command in verificationCommands:
        ret = executeOrRun("command", command, printing=printSubProcessOutput)
        verificationCommandsOutputs.append(ret)
        exit, stdOut, stdErr = ret
        if exit != 0:
            print >>sys.stderr, "Failed test: ", command
            exitCode += 1
        else:
            print >>sys.stderr, "Passed test: ", command
    


if __name__ == '__main__':
    target = sys.argv[1]
    transferUUID =  sys.argv[2]
    verifyBag(target)
    if exitCode != 0:
        print >>sys.stderr, "Failed bagit compliance. Not restructuring."
        for i in range(len(verificationCommands)):
            print verificationCommands[i]
            exitC, stdOut, stdErr = verificationCommandsOutputs
            print exitC, stdOut 
            print >>sys.stderr, stdErr
        exit(exitCode) 
    restructureBagForComplianceFileUUIDsAssigned(target, transferUUID, "transferUUID")
    for i in range(len(verificationCommands)):
        print verificationCommands[i]
        print verificationCommandsOutputs[i]
        print
    exit(exitCode)
