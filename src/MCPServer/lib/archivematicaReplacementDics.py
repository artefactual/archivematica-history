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
#
# @package Archivematica
# @subpackage Ingest
# @author Joseph Perry <joseph@artefactual.com>
# @version svn: $Id$
import os
import sys
sys.path.append("/usr/lib/archivematica/archivematicaCommon")
from archivematicaMCPFileUUID import getUUIDOfFile



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
    

def getSIPUUID(sipDir):
    """Looks at the end of a directory name, to retrieve the UUID on the name"""
    uuidLen = 36
    sip = ""
    if sipDir.endswith("/"):
        sip = os.path.basename(os.path.dirname(sipDir))
    else:
        sip = os.path.basename(sipDir)
    if len(sip) > uuidLen:
        if isUUID(sip[-uuidLen:]):
            return sip[-uuidLen:]
        else:
            return "None"
    else:
        return "None" 

class replacementDics:
    def __init__(self, archivematicaVars):
        self.config = archivematicaVars
        
    def commandReplacementDic(self, task, job, target, command):
        
        #Pre do some variables, that other variables rely on, because dictionarys don't maintain order
        sipDir = job.config.processingDirectory.__str__() + job.UUID.__str__() + "/" + os.path.basename(job.directory).__str__() + "/"
        SIPUUID = getSIPUUID(sipDir)
        SIPName = os.path.basename(job.directory).replace("-" + SIPUUID, "")
        SIPDirectory = sipDir.replace(self.config.get('MCPServer', "sharedDirectory"), "%sharedPath%")
        processingDirectory = job.config.processingDirectory.replace(self.config.get('MCPServer', "sharedDirectory"), "")
        relativeDirectoryLocationNoTrailingSlash = "%sharedPath%" + processingDirectory + job.UUID.__str__()
        relativeDirectoryLocation = relativeDirectoryLocationNoTrailingSlash + "/"
        
        
        ret = { \
        "%jobUUID%": job.UUID.__str__(), \
        "%taskUUID%": task.UUID.__str__(), \
        "%SIPLogsDirectory%": SIPDirectory + "logs/", \
        "%SIPObjectsDirectory%": SIPDirectory + "objects/", \
        "%SIPDirectory%": SIPDirectory, \
        "%fileUUID%": getUUIDOfFile( sipDir + "logs/" +  self.config.get('MCPServer', "fileUUIDSHumanReadable"), sipDir + "objects/", target,  sipDir + "logs/fileMeta/" ), \
        "%relativeLocation%": target.replace(job.config.watchDirectory, relativeDirectoryLocation).replace("\"", ("\\\"")), \
        "%relativeDirectoryLocation%": relativeDirectoryLocation, \
        "%relativeDirectoryLocationNoTrailingSlash%":relativeDirectoryLocationNoTrailingSlash, \
        "%processingDirectory%": processingDirectory, \
        "%checksumsNoExtention%":self.config.get('MCPServer', "checksumsNoExtention"), \
        "%AIPsStore%":self.config.get('MCPServer', "AIPsStore"), \
        "%SIPUUID%":SIPUUID, \
        "%SIPName%":SIPName, \
        }
        return ret

    def jobReplacementDic(self, job, config, directory, step):       
        ret ={ \
        "%watchDirectoryPath%": self.config.get('MCPServer', "watchDirectoryPath"), \
        "%processingDirectory%": self.config.get('MCPServer', "processingDirectory") \
        }
        return ret
        
    def watchFolderRepacementDic(self):
        ret ={ \
        "%watchDirectoryPath%": self.config.get('MCPServer', "watchDirectoryPath"), \
        }
        return ret
    
