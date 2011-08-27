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
import sys
import uuid
from optparse import OptionParser
sys.path.append("/usr/lib/archivematica/archivematicaCommon")
from externals.checksummingTools import sha_for_file
from databaseFunctions import insertIntoEvents
import databaseInterface


def updateSizeAndChecksum(fileUUID, filePath, date, eventIdentifierUUID):   
    fileSize = os.path.getsize(filePath).__str__()
    checksum = sha_for_file(filePath).__str__()
    
    sql = "UPDATE Files " + \
        "SET fileSize='" + fileSize +"', checksum='" + checksum +  "' " + \
        "WHERE fileUUID='" + fileUUID + "'"
    databaseInterface.runSQL(sql)

    insertIntoEvents(fileUUID=fileUUID, \
                     eventIdentifierUUID=eventIdentifierUUID, \
                     eventType="message digest calculation", \
                     eventDateTime=date, \
                     eventDetail="program=\"python\"; module=\"hashlib.sha256()\"", \
                     eventOutcomeDetailNote=checksum)  
    
    insertIntoEvents(fileUUID=fileUUID, \
                 eventIdentifierUUID=uuid.uuid4().__str__(), \
                 eventType="file size calculation", \
                 eventDateTime=date, \
                 eventDetail="program=\"python\"; module=\"os.path.getsize()\"", \
                 eventOutcomeDetailNote=fileSize)  
    
if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-i",  "--fileUUID",          action="store", dest="fileUUID", default="")
    parser.add_option("-p",  "--filePath",          action="store", dest="filePath", default="")
    parser.add_option("-d",  "--date",              action="store", dest="date", default="")
    parser.add_option("-u",  "--eventIdentifierUUID", action="store", dest="eventIdentifierUUID", default="")
    (opts, args) = parser.parse_args()
    
    updateSizeAndChecksum(opts.fileUUID, \
                     opts.filePath, \
                     opts.date, \
                     opts.eventIdentifierUUID)  

    

    
    
