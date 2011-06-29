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
# @subpackage MCP
# @author Joseph Perry <joseph@artefactual.com>
# @version svn: $Id$


import os
import time
from shutil import move 
import sys
import xmlrpclib
import lxml.etree as etree
import string



currentTime = time.time()
proxy = xmlrpclib.ServerProxy("http://localhost:8000/")


def updateJobsAwaitingApproval(jobsAwaitingApproval):
    del jobsAwaitingApproval
    ret = proxy.getJobsAwaitingApproval()
    jobsAwaitingApproval = etree.XML(ret)
    return jobsAwaitingApproval

def unquarantine(f):
    jobsAwaitingApproval = etree.Element("jobsAwaitingApproval")
    jobsAwaitingApproval = updateJobsAwaitingApproval(jobsAwaitingApproval)
    for job in jobsAwaitingApproval:
        directory = ""
        uuid = ""
        for element in job:
            if element.tag == "directory":
                directory = element.text
            if element.tag == "UUID":
                uuid = element.text
                
        if directory == f:
            print "Approving: " + uuid
            proxy.approveJob(uuid)
    
if __name__ == '__main__':
    quarantineTime = sys.argv[1]
    quarantined = sys.argv[2]
    if 0:
        print "quarantineTime:", quarantineTime
        print "quarantined:", quarantined  
    if os.path.isdir(quarantined):
            for f in os.listdir(quarantined):
                f = quarantined + "/" + f
                if (currentTime - os.path.getmtime(f)) > string.atoi(quarantineTime):
                    #print "unquarantine:", f
                    unquarantine(f)
            