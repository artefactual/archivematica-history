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
sys.path.append("/usr/lib/archivematica/archivematicaCommon")
import databaseInterface
import databaseFunctions
from externals.checksummingTools import sha_for_file

def verifyChecksum(fileUUID, filePath, date, eventIdentifierUUID):
    sql = """SELECT checksum FROM Files WHERE fileUUID = '""" + fileUUID + "'"
    c, sqlLock = databaseInterface.querySQL(sql) 
    row = c.fetchone()
    checksumDB = ""
    while row != None:
        checksumDB = row[0]
        row = c.fetchone()
    sqlLock.release()
    if checksumDB == None or checksumDB == "" or checksumDB == "None":
        print >>sys.stderr, "No checksum found in database for file:", fileUUID, filePath
        exit(1)
    checksumFile = sha_for_file(filePath)
    
    eventOutcome=""
    eventOutcomeDetailNote=""
    exitCode = 0
    if checksumFile != checksumDB:
        eventOutcomeDetailNote = checksumFile.__str__() + " != " + checksumDB.__str__()
        eventOutcome="Fail"
        exitCode = 2
        print >>sys.stderr, "Checksums do not match:", fileUUID, filePath
        print >>sys.stderr, eventOutcomeDetailNote
    else:
        eventOutcomeDetailNote = checksumFile.__str__() + "verified"
        eventOutcome="Pass"
        exitCode = 0  
        
    #insertIntoEvents(fileUUID="", eventIdentifierUUID="", eventType="", eventDateTime=databaseInterface.getUTCDate(), eventDetail="", eventOutcome="", eventOutcomeDetailNote="")
    databaseFunctions.insertIntoEvents(fileUUID=fileUUID, \
                 eventIdentifierUUID=eventIdentifierUUID, \
                 eventType="verify checksum", \
                 eventDateTime=date, \
                 eventOutcome=eventOutcome, \
                 eventOutcomeDetailNote=eventOutcomeDetailNote, \
                 eventDetail="program=\"python\"; module=\"hashlib.sha256()\"")
    
    exit(exitCode) 
    
    
if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-i",  "--fileUUID",          action="store", dest="fileUUID", default="")
    parser.add_option("-p",  "--filePath",          action="store", dest="filePath", default="")
    parser.add_option("-d",  "--date",              action="store", dest="date", default="")
    parser.add_option("-u",  "--eventIdentifierUUID", action="store", dest="eventIdentifierUUID", default="")
    (opts, args) = parser.parse_args()
    
    verifyChecksum(opts.fileUUID, \
                     opts.filePath, \
                     opts.date, \
                     opts.eventIdentifierUUID)  


    
    