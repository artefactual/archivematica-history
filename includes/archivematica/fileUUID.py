#!/usr/bin/python
#
# This file is part of Archivematica.
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
# @author Peter Van Garderen <peter@artefactual.com>
# @version svn: $Id$

import os
import sys
import string

UUIDsDic={}

def loadFileUUIDsDic(sipUUID):
  FileUUIDs_fh = open("/home/demo/ingestLogs/" + sipUUID +"/FileUUIDs.log", "r")
  line = FileUUIDs_fh.readline()
  while line:
    detoxfiles = line.split(" -> ",1)
    if len(detoxfiles) > 1 :
      fileUUID = detoxfiles[0]
      fileName = detoxfiles[1]
      fileName = string.replace(fileName, "\n", "", 1)
      UUIDsDic[fileName] = fileUUID
    line = FileUUIDs_fh.readline()
  return UUIDsDic

def getUUIDOfFile( sipUUID, basepath, fullFileName):
  if not UUIDsDic:
    loadFileUUIDsDic(sipUUID)
  if not UUIDsDic:
    return ""
  
  filename = string.replace( fullFileName, basepath, "objects", 1 )    
  if filename in UUIDsDic:
    return UUIDsDic[filename]
  else :
    return "UUID not found for: " + filename

   
if __name__ == '__main__':
  function =  sys.argv[1]

  if function == "Logline" :
    basepath = sys.argv[2]
    fullFileName = sys.argv[3]
    filename = string.replace( fullFileName, basepath, "objects", 1 )    
    print filename

  elif function == "getFileUUID":
    sipUUID = sys.argv[2]
    basepath = sys.argv[3]
    fullFileName = sys.argv[4]
    print getUUIDOfFile( sipUUID, basepath, fullFileName)

