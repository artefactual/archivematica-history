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
import shlex
import subprocess
import os
from archivematicaFunctions import archivematicaRenameFile
from createXmlEventsAssist import createEvent 
from createXmlEventsAssist import createOutcomeInformation
from createXmlEventsAssist import createLinkingAgentIdentifier

DetoxDic={}


#Duplicate from archivematica CLient
def writeToFile(output, fileName):
    if fileName and output:
        print "writing to: " + fileName
        try:
            f = open(fileName, 'a')
            f.write(output.__str__())
            f.close()
        except OSError, ose:
            print >>sys.stderr, "output Error", ose
            return -2
        except IOError as (errno, strerror):
            print "I/O error({0}): {1}".format(errno, strerror)
            return -3
    else:
        print "No output or file specified"
    return 0
        
if __name__ == '__main__':
    """This prints the contents for an Archivematica Clamscan Event xml file"""
    SIPDirectory = sys.argv[1]
    date = sys.argv[2]

    command = "sanitizeNames \"" + SIPDirectory + "\""
    lines = []
    try:
        p = subprocess.Popen(shlex.split(command), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	
        p.wait()
        output = p.communicate()
        retcode = p.returncode
        
        #print output

        #it executes check for errors
        if retcode != 0:
            print >>sys.stderr, "error code:" + retcode.__str__()
            print output[1]# sError
            quit(retcode)
        lines = output[0].split("\n")
    except OSError, ose:
        print >>sys.stderr, "Execution failed:", ose
        quit(2)

    for line in lines:
        detoxfiles = line.split(" -> ")
        if len(detoxfiles) > 1 :
            oldfile = detoxfiles[0].split('\n',1)[0]
            newfile = detoxfiles[1]
            #print "oldfile: " + oldfile
            #print "newfile: " + newfile
            if os.path.isdir(newfile):
                oldfileBase = os.path.basename(oldfile)
                newfileBase = os.path.basename(newfile)
                output = oldfileBase + " -> " + newfileBase
                output += "\nDate: " + date
                writeToFile(output, newfile + "/logs/SIPNameSanitization.log") 

