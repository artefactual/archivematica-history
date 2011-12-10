#!/usr/bin/python -OO

# This file is part of Archivematica.
#
# Copyright 2010-2011 Artefactual Systems Inc. <http://artefactual.com>
#
# Archivematica is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
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

import os
import sys
from optparse import OptionParser
sys.path.append("/usr/lib/archivematica/archivematicaCommon")
import databaseInterface
from fileOperations import updateFileLocation
from fileOperations import renameAsSudo
   
def something(SIPDirectory, accessDirectory, objectsDirectory, DIPDirectory, SIPUUID, date, copy=False):
    #exitCode = 435
    exitCode = 179
    print SIPDirectory
    #For every file, & directory Try to find the matching file & directory in the objects directory
    for (path, dirs, files) in os.walk(accessDirectory):
        for file in files:
            accessPath = os.path.join(path, file)
            objectPath = accessPath.replace(accessDirectory, objectsDirectory, 1)
            objectName = os.path.basename(objectPath)
            objectNameExtensionIndex = objectName.rfind(".")
            
            if objectNameExtensionIndex != -1:
                objectName = objectName[:objectNameExtensionIndex + 1]
                objectNameLike = os.path.join( os.path.dirname(objectPath), objectName).replace(SIPDirectory, "%SIPDirectory%", 1)
                #sql = "SELECT fileUUID, currentLocation FROM Files WHERE currentLocation LIKE  '%s%' AND removedTime = 0 AND SIPUUID = '%s'" % (objectNameLike, SIPUUID)
                #ValueError: unsupported format character ''' (0x27) at index 76
                sql = "SELECT fileUUID, currentLocation FROM Files WHERE currentLocation LIKE  '" + objectNameLike + "%' AND removedTime = 0 AND SIPUUID = '"+ SIPUUID + "'" 
                c, sqlLock = databaseInterface.querySQL(sql) 
                row = c.fetchone()
                if not row:
                    print >>sys.stderr, "No corresponding object for:", accessPath.replace(SIPDirectory, "%SIPDirectory%", 1)
                    exitCode = 1
                update = []
                while row != None:
                    print row
                    objectUUID = row[0]
                    objectPath = row[1]
                    dipPath = os.path.join(DIPDirectory,  "objects", "%s-%s" % (objectUUID, os.path.basename(accessPath))) 
                    if copy:
                        print "TODO - copy not supported yet"
                    else:
                        #
                        dest = dipPath
                        renameAsSudo(accessPath, dest)
                        
                        src = accessPath.replace(SIPDirectory, "%SIPDirectory%") 
                        dst = dest.replace(SIPDirectory, "%SIPDirectory%")
                        update.append((src, dst))
                        
                        #                            
                    row = c.fetchone()
                sqlLock.release()
                for src, dst in update:
                    eventDetail = ""
                    eventOutcomeDetailNote = "moved from=\"" + src + "\"; moved to=\"" + dst + "\""
                    updateFileLocation(src, dst, "movement", date, eventDetail, sipUUID=SIPUUID, eventOutcomeDetailNote = eventOutcomeDetailNote)
    return exitCode
    


if __name__ == '__main__':
    parser = OptionParser()
    #'--SIPDirectory "%SIPDirectory%" --accessDirectory "objects/access/" --objectsDirectory "objects" --DIPDirectory "DIP" -c'
    parser.add_option("-s",  "--SIPDirectory", action="store", dest="SIPDirectory", default="")
    parser.add_option("-u",  "--SIPUUID", action="store", dest="SIPUUID", default="")
    parser.add_option("-a",  "--accessDirectory", action="store", dest="accessDirectory", default="")
    parser.add_option("-o",  "--objectsDirectory", action="store", dest="objectsDirectory", default="")
    parser.add_option("-d",  "--DIPDirectory", action="store", dest="DIPDirectory", default="")
    parser.add_option("-t",  "--date", action="store", dest="date", default="")
    parser.add_option('-c', '--copy', dest='copy', action='store_true')

    (opts, args) = parser.parse_args()
    
    SIPDirectory = opts.SIPDirectory
    accessDirectory = os.path.join(SIPDirectory, opts.accessDirectory)
    objectsDirectory = os.path.join(SIPDirectory, opts.objectsDirectory)
    DIPDirectory = os.path.join(SIPDirectory, opts.DIPDirectory)
    SIPUUID = opts.SIPUUID
    date = opts.date
    copy = opts.copy
    
    if not os.path.isdir(accessDirectory):
        print "no access directory in this sip"
        exit(0)
    
            
    try:
        if not os.path.isdir(DIPDirectory):
            os.mkdir(DIPDirectory)
        if not os.path.isdir(os.path.join(DIPDirectory, "objects")):
            os.mkdir(os.path.join(DIPDirectory, "objects"))
    except:
        print "error creating DIP directory"
    
    exitCode = something(SIPDirectory, accessDirectory, objectsDirectory, DIPDirectory, SIPUUID, date, copy)
    exit(exitCode)
      