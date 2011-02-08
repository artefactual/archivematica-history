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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.    See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Archivematica.    If not, see <http://www.gnu.org/licenses/>.

# @package Archivematica
# @subpackage MCPrpcCLI
# @author Joseph Perry <joseph@artefactual.com>
# @version svn: $Id$

import xmlrpclib
import lxml.etree as etree
import os

proxy = xmlrpclib.ServerProxy("http://localhost:8000/")

def getTagged(root, tag): #bad, I use this elsewhere, should be imported
    ret = []
    for element in root:
        if element.tag == tag:
            ret.append(element)
            return ret #only return the first encounter
    return ret 

def updateJobsAwaitingApproval(jobsAwaitingApproval):
    del jobsAwaitingApproval
    ret = proxy.getJobsAwaitingApproval()
    jobsAwaitingApproval = etree.XML(ret)
    return jobsAwaitingApproval

def printJobsAwaitingApproval(jobsAwaitingApproval):
    i = 0
    #print len(jobsAwaitingApproval)
    for job in jobsAwaitingApproval:
        print i
        i += 1
        print etree.tostring(job, pretty_print=True)
        
def approveJob(jobsAwaitingApproval, choice):
    try:
        index = int(choice)
        if index >= len(jobsAwaitingApproval):
            print "index out of range"
            return
        uuid = getTagged(jobsAwaitingApproval[index], "UUID")[0].text
        print "Approving: " + uuid
        proxy.approveJob(uuid)
        del jobsAwaitingApproval[index]
    except ValueError:
        return    
    

if __name__ == '__main__':
    os.system("clear")
    jobsAwaitingApproval = etree.Element("jobsAwaitingApproval")
    jobsAwaitingApproval = updateJobsAwaitingApproval(jobsAwaitingApproval)
    #print etree.tostring(jobsAwaitingApproval)
    choice = "No-op"
    while choice != "q":
        printJobsAwaitingApproval(jobsAwaitingApproval)
        print "q to quit"
        print "u to update List"
        print "number to approve Job"
        choice = raw_input('Please enter a value:')
        os.system("clear")
        print "choice: " + choice
        if choice == "u":
            jobsAwaitingApproval = updateJobsAwaitingApproval(jobsAwaitingApproval)
        else:
             approveJob(jobsAwaitingApproval, choice)
            
    
    



