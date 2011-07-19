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
# @subpackage MCPServer
# @author Joseph Perry <joseph@artefactual.com>
# @version svn: $Id$

from unit import unit
import archivematicaMCP
import os
import sys
sys.path.append("/usr/lib/archivematica/archivematicaCommon")
import databaseInterface


class unitSIP(unit):

        
    def reloadFileList(self):
        print "todo"
        exit(1)
        
    def reload(self):
        sql = """SELECT * FROM SIP WHERE sipUUID =  '""" + self.UUID + "'" 
        c, sqlLock = databaseInterface.querySQL(sql) 
        row = c.fetchone()
        while row != None:
            print row
            #self.UUID = row[0]
            self.createdTime = row[1] 
            self.currentPath = row[2]
            row = c.fetchone()
        sqlLock.release()
             
        
    def getReplacementDic(self, target):
        # self.currentPath = currentPath.__str__()
        # self.UUID = uuid.uuid4().__str__()
        #Pre do some variables, that other variables rely on, because dictionaries don't maintain order
        SIPUUID = self.UUID
        SIPName = os.path.basename(self.currentPath).replace("-" + SIPUUID, "")
        SIPDirectory = self.currentPath.replace(archivematicaMCP.config.get('MCPServer', "sharedDirectory"), "%sharedPath%")
        relativeDirectoryLocation = target.replace(archivematicaMCP.config.get('MCPServer', "sharedDirectory"), "%sharedPath%")
      
        
        ret = { \
        "%SIPLogsDirectory%": SIPDirectory + "logs/", \
        "%SIPObjectsDirectory%": SIPDirectory + "objects/", \
        "%SIPDirectory%": SIPDirectory, \
        "%relativeLocation%": target.replace(self.currentPath, relativeDirectoryLocation, 1), \
        "%processingDirectory%": archivematicaMCP.config.get('MCPServer', "processingDirectory"), \
        "%checksumsNoExtention%":archivematicaMCP.config.get('MCPServer', "checksumsNoExtention"), \
        "%AIPsStore%":archivematicaMCP.config.get('MCPServer', "AIPsStore"), \
        "%SIPUUID%":SIPUUID, \
        "%SIPName%":SIPName \
        }
        return ret