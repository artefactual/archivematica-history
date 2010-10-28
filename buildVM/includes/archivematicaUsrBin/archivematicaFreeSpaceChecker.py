#!/usr/bin/python

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
# @version svn: $Id$

import os
import sys

def checkSpace(drive = "/", space ="1024"):
  hd=os.statvfs(drive)
  freeSpace = (hd.f_bsize * hd.f_bavail)
  # print "freespace: " + freeSpace.__str__() + "\nspace: " + long(space).__str__()
  if freeSpace < long(space):
    return True
  else:
    return False


if __name__ == '__main__':
  function =  sys.argv[1]

  if function == "checkIfSpaceBelow" :
    disk = sys.argv[2]
    space = sys.argv[3]
    tf = checkSpace(disk, space)
    if tf == True:
      print "true"
    else:
      print "false"

  elif function == "checkCurrentSpace":
    #drive = sys.argv[2]
    drive = "/"
    hd=os.statvfs(drive)
    freeSpace = (hd.f_bsize * hd.f_bavail)  
    print freeSpace.__str__() + " Bytes"


  else:
    print "Usage Error"

