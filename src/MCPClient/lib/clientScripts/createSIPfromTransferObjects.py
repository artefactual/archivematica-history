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
import uuid
import shutil
import MySQLdb
import os
import sys
sys.path.append("/usr/lib/archivematica/archivematicaCommon")
import databaseInterface
import databaseFunctions
from archivematicaCreateStructuredDirectory import createStructuredDirectory

#def updateDB(dst, transferUUID):
#    sql =  """UPDATE Transfers SET currentLocation='""" + dst + """' WHERE transferUUID='""" + transferUUID + """';"""
#    databaseInterface.runSQL(sql)
    
#moveSIP(src, dst, transferUUID, sharedDirectoryPath)

if __name__ == '__main__':
    objectsDirectory = sys.argv[1]
    transferName = sys.argv[2]
    transferUUID = sys.argv[3]
    processingDirectory = sys.argv[4]
    autoProcessSIPDirectory = sys.argv[5]
    sharedPath = sys.argv[6]
    sipName = transferName
    sipUUID = uuid.uuid4().__str__()
    
    
    tmpSIPDir = os.path.join(processingDirectory, sipName) + "/"
    destSIPDir =  os.path.join(autoProcessSIPDirectory, sipName) + "/"
    createStructuredDirectory(tmpSIPDir)
    databaseFunctions.createSIP(destSIPDir.replace(sharedPath, '%sharedPath%'), sipUUID)
    
    #move the objects to the SIPDir
    for item in os.listdir(objectsDirectory):
        shutil.move(os.path.join(objectsDirectory, item), os.path.join(tmpSIPDir, "objects", item))
        
    #get the database list of files in the objects directory
    #for each file, confirm it's in the SIP objects directory, and update the current location/ owning SIP'
    sql = """SELECT  fileUUID, currentLocation FROM Files WHERE removedTime = 0 AND currentLocation LIKE '%%transferDirectory%%objects%' AND transferUUID =  '""" + transferUUID + "'" 
    for row in databaseInterface.queryAllSQL(sql):
        fileUUID = row[0]
        currentPath = row[1]
        currentSIPFilePath = currentPath.replace("%transferDirectory%", tmpSIPDir)
        if os.path.isfile(currentSIPFilePath):
            sql = """UPDATE Files SET currentLocation='%s', sipUUID='%s' WHERE fileUUID='%s'""" % (MySQLdb.escape_string(currentPath.replace("%transferDirectory%", "%SIPDirectory%")), sipUUID, fileUUID)
            databaseInterface.runSQL(sql)
        else:
            print >>sys.stderr, "file not found: ", currentSIPFilePath
        
    
    #moveSIPTo autoProcessSIPDirectory
    shutil.move(tmpSIPDir, destSIPDir)

