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
import string

DetoxDic={}
DetoxFile = sys.argv[1]
originalSIPName = sys.argv[2]

def loadDetoxDic(sfile):
    detox_fh = open(sfile, "r")
 
    line = detox_fh.readline()
    while line:
        detoxfiles = line.split(" -> ")
        if len(detoxfiles) > 1 :
            oldfile = detoxfiles[0]
            newfile = detoxfiles[1]
            newfile = string.replace(newfile, "\n", "", 1)
            oldfile = oldfile + "/" #Hack
            DetoxDic[oldfile] = newfile
        line = detox_fh.readline()
        
if __name__ == '__main__':
    loadDetoxDic(DetoxFile)
    destDir = ""
    if originalSIPName in DetoxDic:
        destDir = DetoxDic[originalSIPName] + "/logs/" + os.path.basename(DetoxFile)
    else:
        destDir = originalSIPName + "/logs/" + os.path.basename(DetoxFile)
    print "moving: " + DetoxFile + " TO: " + destDir
    os.rename(DetoxFile, destDir)

    

