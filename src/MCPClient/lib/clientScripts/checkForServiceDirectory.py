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
import uuid
from optparse import OptionParser
sys.path.append("/usr/lib/archivematica/archivematicaCommon")
import databaseInterface
from databaseFunctions import insertIntoDerivations

    
def something(SIPDirectory, serviceDirectory, objectsDirectory, SIPUUID, date):
    #exitCode = 435
    exitCode = 0
    print SIPDirectory
    #For every file, & directory Try to find the matching file & directory in the objects directory
    for (path, dirs, files) in os.walk(serviceDirectory):
        for file in files:
            accessPath = os.path.join(path, file)
            sql = "UPDATE Files SET fileGrpUse='service' WHERE currentLocation =  '" + accessPath.replace(SIPDirectory, "%SIPDirectory%", 1) + "' AND removedTime = 0 AND SIPUUID = '"+ SIPUUID + "'"
            #print sql
            rows = databaseInterface.runSQL(sql)           
    return exitCode
    


if __name__ == '__main__':
    parser = OptionParser()
    #'--SIPDirectory "%SIPDirectory%" --serviceDirectory "objects/service/" --objectsDirectory "objects/" --SIPUUID "%SIPUUID%" --date "%date%"' );
    parser.add_option("-s",  "--SIPDirectory", action="store", dest="SIPDirectory", default="")
    parser.add_option("-u",  "--SIPUUID", action="store", dest="SIPUUID", default="")
    parser.add_option("-a",  "--serviceDirectory", action="store", dest="serviceDirectory", default="")
    parser.add_option("-o",  "--objectsDirectory", action="store", dest="objectsDirectory", default="")
    parser.add_option("-t",  "--date", action="store", dest="date", default="")

    (opts, args) = parser.parse_args()
    
    SIPDirectory = opts.SIPDirectory
    serviceDirectory = os.path.join(SIPDirectory, opts.serviceDirectory)
    objectsDirectory = os.path.join(SIPDirectory, opts.objectsDirectory)
    SIPUUID = opts.SIPUUID
    date = opts.date
    
    if not os.path.isdir(serviceDirectory):
        print "no service directory in this sip"
        exit(0)
    
    exitCode = something(SIPDirectory, serviceDirectory, objectsDirectory, SIPUUID, date)
    exit(exitCode)
      